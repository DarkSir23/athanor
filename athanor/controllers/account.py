import re
from collections import defaultdict

from django.conf import settings

from evennia.utils.utils import class_from_module, make_iter
from evennia.utils.logger import log_trace
from evennia.utils.search import search_account

import athanor
from athanor.controllers.base import AthanorController
from athanor.gamedb.accounts import AthanorAccount
from athanor.messages import account as amsg
from athanor.utils.text import partial_match, iter_to_string

from athanor.utils import styling

MIXINS = [class_from_module(mixin) for mixin in settings.CONTROLLER_MIXINS["ACCOUNT"]]
MIXINS.sort(key=lambda x: getattr(x, "mixin_priority", 0))


class AthanorAccountController(*MIXINS, AthanorController):
    system_name = 'ACCOUNTS'

    def __init__(self, key, manager):
        AthanorController.__init__(self, key, manager)
        self.account_typeclass = None
        self.id_map = dict()
        self.name_map = dict()
        self.roles = dict()
        self.reg_names = None
        self.permissions = defaultdict(set)
    
    def do_load(self):
        try:
            self.account_typeclass = class_from_module(settings.BASE_ACCOUNT_TYPECLASS,
                                                         defaultpaths=settings.TYPECLASS_PATHS)
        except Exception:
            log_trace()
            self.account_typeclass = AthanorAccount

        self.update_cache()

    def update_regex(self):
        escape_names = [re.escape(name) for name in self.name_map.keys()]
        self.reg_names = re.compile(r"(?i)\b(?P<found>%s)\b" % '|'.join(escape_names))

    def update_cache(self):
        accounts = AthanorAccount.objects.filter_family()
        self.id_map = {acc.id: acc for acc in accounts}
        self.name_map = {acc.username.upper(): acc for acc in accounts}
        self.update_regex()
        self.permissions = defaultdict(set)
        for acc in accounts:
            for perm in acc.permissions.all():
                self.permissions[perm].add(acc)
            if acc.is_superuser:
                self.permissions["_super"].add(acc)

    def create_account(self, session, username, email, password, login_screen=False, **kwargs):
        if not login_screen:
            if not (enactor := session.get_account()) or not enactor.check_lock("oper(account_create)"):
                raise ValueError("Permission denied.")
        new_account = self.account_typeclass.create_account(username=username, email=email, password=password,
                                                                session=session, ip=session.address)
        self.id_map[new_account.id] = new_account
        self.name_map[new_account.username.upper()] = new_account
        self.update_regex()
        for perm in new_account.permissions.all():
            self.permissions[perm].add(new_account)
        if login_screen:
            amsg.CreateMessage(source=session, target=new_account).send()
        else:
            amsg.CreateMessageAdmin(source=enactor, target=new_account, password=password).send()

        return new_account

    def rename_account(self, session, account, new_name, ignore_priv=False):
        if not (enactor := session.get_account()) or (not ignore_priv and not enactor.check_lock("oper(account_rename)")):
            raise ValueError("Permission denied.")
        account = self.find_account(account)
        old_name = str(account)
        new_name = account.rename(new_name)
        amsg.RenameMessage(source=enactor, target=account, old_name=old_name, account_name=new_name).send()

    def change_email(self, session, account, new_email, ignore_priv=False):
        if not (enactor := session.get_account()) or (not ignore_priv and not enactor.check_lock("oper(account_email)")):
            raise ValueError("Permission denied.")
        account = self.find_account(account)
        old_email = account.email
        new_email = account.set_email(new_email)
        amsg.EmailMessage(source=enactor, target=account, old_email=old_email).send()

    def find_account(self, search_text, exact=False):
        if isinstance(search_text, AthanorAccount):
            return search_text
        if '@' in search_text:
            found = AthanorAccount.objects.get_account_from_email(search_text).first()
            if found:
                return found
            raise ValueError(f"Cannot find a user with email address: {search_text}")
        found = search_account(search_text, exact=exact)
        if len(found) == 1:
            return found[0]
        if not found:
            raise ValueError(f"Cannot find a user named {search_text}!")
        raise ValueError(f"That matched multiple accounts: {found}")

    def disable_account(self, session, account, reason):
        if not (enactor := session.get_account()) or not enactor.check_lock("oper(account_disable)"):
            raise ValueError("Permission denied.")
        account = self.find_account(account)
        account.set_unusable_password()
        amsg.DisableMessage(source=enactor, target=account, reason=reason)

    def enable_account(self, session, account, new_password, reason):
        if not (enactor := session.get_account()) or not enactor.check_lock("oper(account_disable)"):
            raise ValueError("Permission denied.")
        account = self.find_account(account)
        if not new_password:
            raise ValueError("Passwords may not be empty!")
        account.set_password(new_password)
        amsg.EnableMessage(source=enactor, target=account, reason=reason)

    def ban_account(self, session, account, duration, reason):
        if not (enactor := session.get_account()) or not enactor.check_lock("oper(account_ban)"):
            raise ValueError("Permission denied.")
        account = self.find_account(account)
        amsg.BanMessage(source=enactor, target=account, duration=duration, reason=reason)

    def unban_account(self, session, account, reason):
        if not (enactor := session.get_account()) or not enactor.check_lock("oper(account_ban)"):
            raise ValueError("Permission denied.")
        account = self.find_account(account)
        amsg.UnBanMessage(source=enactor, target=account, reason=reason)

    def reset_password(self, session, account, new_password, ignore_priv=False, old_password=None):
        if not (enactor := session.get_account()) or (not ignore_priv and not enactor.check_lock("oper(account_password)")):
            raise ValueError("Permission denied.")
        if ignore_priv and not account.check_password(old_password):
            raise ValueError("Permission denied. Password was incorrect.")
        account = self.find_account(account)
        if not new_password:
            raise ValueError("Passwords may not be empty!")
        account.set_password(new_password)
        if old_password:
            amsg.PasswordMessagePrivate(source=enactor).send()
        else:
            amsg.PasswordMessageAdmin(source=enactor, target=account, password=new_password).send()

    def find_permission(self, perm):
        if not perm:
            raise ValueError("No permission entered!")
        if not (found := partial_match(perm, settings.PERMISSIONS.keys())):
            raise ValueError("Permission not found!")
        return found

    def grant_permission(self, session, account, perm):
        if not (enactor := session.get_account()):
            raise ValueError("Permission denied.")
        account = self.find_account(account)
        perm = self.find_permission(perm)
        perm_data = settings.PERMISSIONS.get(perm, dict())
        perm_lock = perm_data.get("permission", None)
        if not perm_lock:
            if not enactor.is_superuser:
                raise ValueError("Permission denied. Only a Superuser can grant this.")
        if perm_lock:
            passed = False
            for lock in make_iter(perm_lock):
                if (passed := enactor.check_lock(f"pperm({lock})")):
                    break
            if not passed:
                raise ValueError(f"Permission denied. Requires {perm_lock} or better.")
        if perm.lower() in account.permissions.all():
            raise ValueError(f"{account} already has that Permission!")
        account.permissions.add(perm)
        self.permissions[perm.lower()].add(account)
        account.operations.clear_cache()
        amsg.GrantMessage(source=enactor, target=account, perm=perm).send()

    def revoke_permission(self, session, account, perm):
        if not (enactor := session.get_account()):
            raise ValueError("Permission denied.")
        account = self.find_account(account)
        perm = self.find_permission(perm)
        perm_data = settings.PERMISSIONS.get(perm, dict())
        perm_lock = perm_data.get("permission", None)
        if not perm_lock:
            if not enactor.is_superuser:
                raise ValueError("Permission denied. Only a Superuser can grant this.")
        if perm_lock:
            passed = False
            for lock in make_iter(perm_lock):
                if (passed := enactor.check_lock(f"pperm({lock})")):
                    break
            if not passed:
                raise ValueError(f"Permission denied. Requires {perm_lock} or better.")
        if perm.lower() not in account.permissions.all():
            raise ValueError(f"{account} does not have that Permission!")
        account.permissions.remove(perm)
        self.permissions[perm.lower()].remove(account)
        account.operations.clear_cache()
        amsg.RevokeMessage(source=enactor, target=account, perm=perm).send()

    def toggle_super(self, session, account):
        if not (enactor := session.get_account()) or not enactor.is_superuser:
            raise ValueError("Permission denied.")
        account = self.find_account(account)
        acc_super = account.is_superuser
        reverse = not acc_super
        if acc_super:
            amsg.RevokeSuperMessage(source=enactor, target=account).send()
        else:
            amsg.GrantSuperMessage(source=enactor, target=account).send()
        account.is_superuser = reverse
        account.save(update_fields=['is_superuser'])
        if reverse:
            self.permissions["_super"].add(account)
        else:
            self.permissions["_super"].remove(account)
        return reverse
    
    def access_account(self, session, account):
        if not (enactor := session.get_account()) or not enactor.check_lock("oper(account_examine)"):
            raise ValueError("Permission denied.")
        account = self.find_account(account)
        message = list()
        message.append(styling.styled_header(enactor, f"Access Levels: {account}"))
        message.append(f"PERMISSION HIERARCHY: {iter_to_string(settings.PERMISSION_HIERARCHY)} <<<< SUPERUSER")
        message.append(f"HELD PERMISSIONS: {iter_to_string(account.permissions.all())} ; SUPERUSER: {account.is_superuser}")
        message.append(styling.styled_footer(enactor))
        return '\n'.join(str(l) for l in message)

    def permissions_directory(self, session):
        if not (enactor := session.get_account()) or not enactor.check_lock("oper(account_examine)"):
            raise ValueError("Permission denied.")
        # Create a COPY of the permissions since we're going to mutilate it a lot...

        perms = dict(self.permissions)
        message = list()
        message.append(styling.styled_header(enactor, "Permissions Hierarchy"))
        message.append(f"|rSUPERUSERS:|n {iter_to_string(perms.pop('_super', list()))}")
        for perm in reversed(settings.PERMISSION_HIERARCHY):
            if perm.lower() in perms:
                message.append(f"{perm:>10}: {iter_to_string(perms.pop(perm.lower(), list()))}")
        if perms:
            message.append(styling.styled_separator(enactor, "Non-Hierarchial Permissions"))
            for perm, holders in perms.items():
                if not holders:
                    continue
                message.append(f"{perm}: {iter_to_string(holders)}")
        message.append(styling.styled_footer(enactor))
        return '\n'.join(str(l) for l in message)

    def list_permissions(self, session):
        if not (enactor := session.get_account()):
            raise ValueError("Permission denied.")
        message = list()
        message.append(styling.styled_header(enactor, "Grantable Permissions"))
        for perm, data in settings.PERMISSIONS.items():
            message.append(styling.styled_separator(enactor, perm))
            message.append(f"Grantable By: {data.get('permission', 'SUPERUSER')}")
            if (desc := data.get("description", None)):
                message.append(f"Description: {desc}")
        message.append(styling.styled_footer(enactor))
        return '\n'.join(str(l) for l in message)

    def list_accounts(self, session):
        if not (enactor := session.get_account()) or not enactor.check_lock("oper(account_examine)"):
            raise ValueError("Permission denied.")
