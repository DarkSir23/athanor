from django.conf import settings
from collections import defaultdict

from evennia.utils.logger import log_trace
from evennia.utils.utils import class_from_module, make_iter

from athanor.gamedb.objects import AthanorObject
from athanor.controllers.base import AthanorController
from athanor.datamodule import AthanorDataModule

MIXINS = [class_from_module(mixin) for mixin in settings.CONTROLLER_MIXINS["GAMEDATA"]]
MIXINS.sort(key=lambda x: getattr(x, "mixin_priority", 0))


class AthanorGameDataController(*MIXINS, AthanorController):
    system_name = 'GAMEDATA'

    def __init__(self, key, manager):
        AthanorController.__init__(self, key, manager)
        self.plugins = dict()
        self.plugins_sorted = list()
        self.plugin_class = None

    def do_load(self):
        try:
            self.plugin_class = class_from_module(settings.GAMEDATA_MODULE_CLASS)
        except Exception:
            log_trace()
            self.plugin_class = AthanorDataModule

        self.load_plugins()

    def load_plugins(self):
        for plugin_module in settings.ATHANOR_PLUGINS_LOADED:
            use_class = self.plugin_class
            if hasattr(plugin_module, "PLUGIN_CLASS"):
                use_class = class_from_module(plugin_module.PLUGIN_CLASS)
            loaded_plugin = use_class(plugin_module)
            loaded_plugin.initialize()
            self.plugins[loaded_plugin.key] = loaded_plugin
            self.plugins_sorted.append(loaded_plugin)

    def resolve_path(self, path, plugin, kind):
        split_path = path.split('/')
        if len(split_path) == 1:
            plugin_path = plugin
            kind_path = kind
            key_path = split_path[0]
        if len(split_path) == 2:
            plugin_path = plugin
            kind_path, key_path = split_path
        if len(split_path) == 3:
            plugin_path, kind_path, key_path = split_path
        return plugin_path, kind_path, key_path

    def get_class(self, kind, path):
        if path and not isinstance(path, str):
            return path
        if not path:
            return class_from_module(settings.DEFAULT_ENTITY_CLASSES[kind])
        if not (found := self.class_cache[kind].get(path, None)):
            found = class_from_module(path)
            self.class_cache[kind][path] = found
        return found

    def resolve_room_path(self, path):
        if '/' not in path:
            raise ValueError(f"Path is malformed. Must be in format of OBJ/ROOM_KEY")
        obj, room_key = path.split('/', 1)
        if obj.startswith('#'):
            obj = obj[1:]
            if obj.isdigit():
                if not (found := AthanorObject.objects.filter(id=int(obj)).first()):
                    raise ValueError(f"Cannot find an object for #{obj}!")
                if not hasattr(found, 'map_bridge'):
                    raise ValueError(f"Must target objects with internal maps.")
            else:
                raise ValueError(f"Path is malformed. Must be in format of OBJ/ROOM_KEY")
        else:
            if not (found := self.regions.get(obj, None)):
                raise ValueError(f"Cannot find a region for {obj}!")
        if not room_key:
            raise ValueError(f"Path is malformed. Must be in format of OBJ/ROOM_KEY")
        if not (room := found.map.get_room(room_key)):
            raise ValueError(f"Cannot find that room_key in {found}!")
        return room

    def prepare_templates(self):
        templates_raw = dict()

        for plugin in self.plugins.values():
            for template_type, templates in plugin.data.pop("templates", dict()).items():
                for template_key, template_data in templates.items():
                    templates_raw[(plugin.key, template_type, template_key)] = template_data

        templates_left = set(templates_raw.keys())
        loaded_set = set()
        current_count = 0
        while len(templates_left) > 0:
            start_count = current_count
            for template in templates_left:
                template_data = templates_raw[template]
                template_list = make_iter(template_data.get('templates', list()))
                resolved = [self.resolve_path(template_par, template[0], template[1]) for template_par in template_list]
                if len(set(resolved) - loaded_set) > 0:
                    continue
                final_data = dict()
                for template_par in resolved:
                    final_data.update(templates_raw[template_par])
                final_data.update(templates_raw[template])
                if "templates" in final_data:
                    del final_data['templates']
                final_data['class'] = self.get_class(template[1], final_data.get('class', None))
                self.plugins[template[0]].templates[template[1]][template[2]] = final_data
                loaded_set.add(template)
                current_count += 1
            templates_left -= loaded_set
            if start_count == current_count:
                raise ValueError(
                    f"Unresolveable old_templates detected! Error for template {template} ! Potential endless loop broken! old_templates left: {templates_left}")

    def get_template(self, plugin_key, kind, key):
        if not (plugin := self.plugins.get(plugin_key, None)):
            raise ValueError(f"No such Plugin: {plugin_key}")
        if not (ki := plugin.templates.get(kind, None)):
            raise ValueError(f"No Template Kind: {plugin_key}/{kind}")
        if not (k := ki.get(key, None)):
            raise ValueError(f"No Template Key: {plugin_key}/{kind}/{key}")
        return k

    def prepare_data(self, kind, start_data, plugin, no_class=False):
        data = dict()
        if (templates := start_data.get('templates', None)):
            for template in make_iter(templates):
                data.update(self.get_template(plugin, kind, template))
            start_data.pop('templates')
        data.update(start_data)
        if not no_class:
            data['class'] = self.get_class(kind, start_data.pop('class', None))
        return data

    def prepare_maps(self):
        for plugin_key, plugin in self.plugins.items():
            for key, data in plugin.data.pop("maps", dict()).items():
                map_data = defaultdict(dict)
                map_data['map'] = self.prepare_data('maps', data.get('map', dict()), plugin_key, no_class=True)
                for kind in ('areas', 'rooms', 'gateways'):
                    for thing_key, thing_data in data.get(kind, dict()).items():
                        map_data[kind][thing_key] = self.prepare_data(kind, thing_data, plugin_key)

                for room_key, room_exits in data.get('exits', dict()).items():
                    map_data['rooms'][room_key]['exits'] = dict()
                    if not room_exits:
                        continue
                    for dest_key, exit_data in room_exits.items():
                        map_data['rooms'][room_key]['exits'][dest_key] = self.prepare_data('exits', exit_data,
                                                                                           plugin_key)

                plugin.maps[key] = map_data

    def load_regions(self):
        for plugin_key, plugin in self.plugins.items():
            for key, data in plugin.data.pop('regions', dict()).items():
                if not (found := AthanorRegion.objects.filter_family(region_bridge__system_key=key).first()):
                    region_class = self.get_class("regions", data.pop('class', None))
                    found = region_class.create_region(plugin_key, key, data)
                else:
                    found.update_data(data)
                self.regions[key] = found
