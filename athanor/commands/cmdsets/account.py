from django.conf import settings

from evennia import default_cmds


USE_COMMANDS = []

USE_LISTS = [USE_COMMANDS]


class AthanorAccountCmdSet(default_cmds.AccountCmdSet):
    """
    This is the cmdset available to the Account at all times. It is
    combined with the `CharacterCmdSet` when the Account puppets a
    Character. It holds game-account-specific commands, channel
    commands, etc.
    """
    key = "DefaultAccount"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
        for cmdlist in USE_LISTS:
            for cmd in cmdlist:
                self.add(cmd)
