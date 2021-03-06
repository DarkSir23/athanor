import re
from django.conf import settings

from evennia.utils.utils import class_from_module
from evennia.utils.logger import log_trace
from evennia.utils.search import object_search

from athanor.controllers.base import AthanorController
from athanor.gamedb.characters import AthanorPlayerCharacter

from athanor.messages import character as cmsg

MIXINS = [class_from_module(mixin) for mixin in settings.CONTROLLER_MIXINS["CHARACTER"]]
MIXINS.sort(key=lambda x: getattr(x, "mixin_priority", 0))


class AthanorCharacterController(*MIXINS, AthanorController):
    system_name = 'CHARACTERS'

    def __init__(self, key, manager):
        AthanorController.__init__(self, key, manager)
        self.character_typeclass = None
        self.id_map = dict()
        self.name_map = dict()
        self.online = set()
        self.on_global("character_online", self.at_character_online)
        self.on_global("character_offline", self.at_character_offline)
        self.reg_names = None
        self.load()

    def do_load(self):
        try:
            self.character_typeclass = class_from_module(settings.BASE_CHARACTER_TYPECLASS,
                                                           defaultpaths=settings.TYPECLASS_PATHS)
        except Exception:
            log_trace()
            self.character_typeclass = AthanorPlayerCharacter

        self.update_cache()

    def update_regex(self):
        escape_names = [re.escape(name) for name in self.name_map.keys()]
        self.reg_names = re.compile(r"(?i)\b(?P<found>%s)\b" % '|'.join(escape_names))

    def at_character_online(self, sender, **kwargs):
        self.online.add(sender)

    def at_character_offline(self, sender, **kwargs):
        self.online.remove(sender)

    def update_cache(self):
        chars = AthanorPlayerCharacter.objects.filter_family(character_bridge__db_namespace=0)
        self.id_map = {char.id: char for char in chars}
        self.name_map = {char.key.upper(): char for char in chars}
        self.online = set(chars.exclude(db_account=None))

    def all(self):
        return AthanorPlayerCharacter.objects.filter_family()

    def search_all(self, name, exact=False, candidates=None):
        if candidates is None:
            candidates = self.all()
        return object_search(name, exact=exact, candidates=self.all())

    def archived(self):
        return self.all().filter(character_bridge__db_namespace=None)

    def search_archived(self, name, exact=False):
        return self.search_all(name, exact, candidates=self.archived())

    def find_character(self, character, archived=False):
        if isinstance(character, AthanorPlayerCharacter):
            return character
        results = self.search_all(character) if not archived else self.search_archived(character)
        if not results:
            raise ValueError(f"Cannot locate character named {character}!")
        if len(results) == 1:
            return results[0]
        raise ValueError(f"That matched: {results}")

    find_user = find_character

    def create_character(self, session, account, character_name, namespace=0, ignore_priv=False):
        if not (enactor := session.get_account()) or (not ignore_priv and not enactor.check_lock("oper(character_create)")):
            raise ValueError("Permission denied.")
        account = self.manager.get('account').find_account(account)
        new_character = self.character_typeclass.create_character(character_name, account, namespace=namespace)
        new_character.db.account = account
        if namespace == 0:
            self.id_map[new_character.id] = new_character
            self.name_map[new_character.key.upper()] = new_character
        entities = {'enactor': enactor, 'character': new_character, 'account': account}
        cmsg.CreateMessage(entities).send()
        return new_character

    def archive_character(self, session, character, verify_name):
        if not (enactor := session.get_account()) or not enactor.check_lock("pperm(Admin)"):
            raise ValueError("Permission denied.")
        character = self.find_character(character)
        account = character.character_bridge.account
        character.archive()
        entities = {'enactor': enactor, 'character': character, 'account': account}
        cmsg.ArchiveMessage(entities).send()
        character.force_disconnect(reason="Character has been archived!")

    def restore_character(self, session, character, replace_name):
        if not (enactor := session.get_account()) or not enactor.check_lock("pperm(Admin)"):
            raise ValueError("Permission denied.")
        character = self.find_character(character)
        account = character.character_bridge.account
        character.restore(replace_name)
        entities = {'enactor': enactor, 'character': character, 'account': account}
        cmsg.RestoreMessage(entities).send()

    def rename_character(self, session, character, new_name, ignore_priv=False):
        if not (enactor := session.get_account()) or (
                not ignore_priv and not enactor.check_lock("pperm(Admin)")):
            raise ValueError("Permission denied.")
        character = self.find_character(character)
        account = character.character_bridge.account
        old_name = character.key
        new_name = character.rename(new_name)
        entities = {'enactor': enactor, 'character': character, 'account': account}
        cmsg.RenameMessage(entities, old_name=old_name).send()

    def transfer_character(self, session, character, new_account, ignore_priv=False):
        if not (enactor := session.get_account()) or (
                not ignore_priv and not enactor.check_lock("pperm(Admin)")):
            raise ValueError("Permission denied.")
        character = self.find_character(character)
        account = character.character_bridge.account
        new_account = self.manager.get('account').find_account(new_account)
        character.force_disconnect(reason="This character has been transferred to a different account!")
        character.set_account(new_account)
        entities = {'enactor': enactor, 'character': character, 'account_from': account, 'account_to': new_account}
        cmsg.TransferMessage(entities).send()

    def examine_character(self, session, character):
        if not (enactor := session.get_account()) or not enactor.check_lock("pperm(Admin)"):
            raise ValueError("Permission denied.")
        character = self.find_character(character)
        return character.render_examine(enactor)

    def list_characters(self, session, archived=False):
        if not (enactor := session.get_account()) or not enactor.check_lock("pperm(Admin)"):
            raise ValueError("Permission denied.")
        if not (characters := self.all() if not archived else self.archived()):
            raise ValueError("No characters to list!")
        styling = enactor.styler
        message = [
            styling.styled_header(f"{'Character' if not archived else 'Archived Character'} Listing")
        ]
        for char in characters:
            message.extend(char.render_list_section(enactor, styling))
        message.append(styling.blank_footer)
        return '\n'.join(str(l) for l in message)