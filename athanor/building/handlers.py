class InstanceHandler(object):

    def __init__(self, owner):
        self.owner = owner
        self.rooms = dict()
        self.gateways = dict()
        self.areas = dict()
        self.loaded = False

    def get_room(self, room_key):
        if not self.loaded:
            self.load()
        return self.rooms.get(room_key, None)

    def load(self):
        from athanor.core.engine import ATHANOR_WORLD
        if self.loaded:
            return
        if not hasattr(self.owner, 'instance_bridge'):
            raise ValueError(f"{self.owner} does not support an internal map!")
        bri = self.owner.instance_bridge
        if not (ex := ATHANOR_WORLD.data_manager.extensions.get(bri.extension, None)):
            raise ValueError(f"Cannot load {self.owner} map data: {bri.extension} extension not found.")
        if not (inst := ex.instances.get(bri.instance_key, None)):
            raise ValueError(f"Cannot load {self.owner} map data: {bri.extension}/{bri.instance_key} instance not found.")

        inst_data = inst.get('instance', dict())

        for area_key, area_data in inst.get('areas', dict()).items():
            area_class = area_data.get('class')
            self.areas[area_key] = area_class(area_key, self, area_data)

        for room_key, room_data in inst.get('rooms', dict()).items():
            room_class = room_data.get('class')
            self.rooms[room_key] = room_class(room_key, self, room_data)

        for gateway_key, gateway_data in inst.get('gateways', dict()).items():
            gateway_class = gateway_data.get('class')
            self.gateways[gateway_key] = gateway_class(gateway_key, self, gateway_data)

        for room in self.rooms.values():
            room.load_exits()

        self.loaded = True

    def save(self):
        pass


class LocationHandler(object):
    
    def __init__(self, owner):
        self.owner = owner
        self.room = None
        self.x = None
        self.y = None
        self.z = None

    @property
    def instance(self):
        if not self.room:
            return None
        return self.room.instance

    def set(self, room, save=True):
        if room and not hasattr(room, 'instance'):
            return
            # raise ValueError(f"{room} is not a valid location for a game entity.")
        if room and room == self.room:
            return
        old_room = self.room
        if old_room:
            old_room.entities.remove(self.owner)
            old_room.at_unregister_entity(self.owner)
            if not room or room.instance != old_room.instance:
                old_room.instance.entities.remove(self.owner)
                old_room.instance.at_unregister_entity(self.owner)
        self.room = room
        if room:
            if not old_room or old_room.instance != room.instance:
                room.instance.entities.add(self.owner)
                room.instance.at_register_entity(self.owner)
            room.entities.add(self.owner)
            room.at_register_entity(self.owner)
        if room and save and room.fixed:
            self.save()

    def save(self, name="logout"):
        if not self.owner.persistent:
            return
        if not self.room:
            return
        if not self.room.fixed:
            raise ValueError("Cannot save to a non-fixed room.")
        if (loc := self.owner.saved_locations.filter(name=name).first()):
            loc.instance = self.instance
            loc.room_key = self.room.unique_key
            loc.x_coordinate = self.x
            loc.y_coordinate = self.y
            loc.z_coordinate = self.z
            loc.save()
        else:
            self.owner.saved_locations.create(name=name, instance=self.instance, room_key=self.room.unique_key,
                                              x_coordinate=self.x, y_coordinate=self.y, z_coordinate=self.z)

    def recall(self, name="logout"):
        if not self.owner.persistent:
            return
        if not (loc := self.owner.saved_locations.filter(name=name).first()):
            raise ValueError(f"No saved location for {name}")
        self.owner.move_to(loc.instance.instance.get_room(loc.room_key))