# Use the defaults from Evennia unless explicitly overridden
import os
from evennia.settings_default import *

# ATHANOR SETTINGS

MULTISESSION_MODE = 3
USE_TZ = True
MAX_NR_CHARACTERS = 4
TELNET_OOB_ENABLED = True

DEFAULT_HOME = "#2"
START_LOCATION = "#2"

# Determines whether non-admin can create characters at all.
PLAYER_CREATE = True

# Let's disable that annoying timeout by default!
IDLE_TIMEOUT = -1

# Enabling some extra Django apps!
INSTALLED_APPS = INSTALLED_APPS + ('timezone_field',
                                   'athanor.bbs.apps.BBS',
                                   'athanor.jobs.apps.Jobs',
                                   'athanor.fclist.apps.FCList',
                                   'athanor.grid.apps.Grid',
                                   'athanor.groups.apps.Group',
                                   'athanor.info.apps.Info',
                                   'athanor.core.apps.Core',
                                   'athanor.mushimport.apps.Mushimport',
                                   'athanor.radio.apps.Radio',
                                   'athanor.scenes.apps.Scenes',)


LOCK_FUNC_MODULES = LOCK_FUNC_MODULES + ("athanor.groups.locks",)


# TYPECLASS STUFF
# Typeclass for player objects (linked to a character) (fallback)
BASE_PLAYER_TYPECLASS = "athanor.typeclasses.players.Player"
# Typeclass and base for all objects (fallback)
#BASE_OBJECT_TYPECLASS = "typeclasses.objects.Object"
# Typeclass for character objects linked to a player (fallback)
BASE_CHARACTER_TYPECLASS = "athanor.typeclasses.characters.Character"
# Typeclass for rooms (fallback)
BASE_ROOM_TYPECLASS = "athanor.typeclasses.rooms.Room"
# Typeclass for Exit objects (fallback).
BASE_EXIT_TYPECLASS = "athanor.typeclasses.exits.Exit"
# Typeclass for Channel (fallback).
BASE_CHANNEL_TYPECLASS = "athanor.typeclasses.channels.PublicChannel"
# Typeclass for Scripts (fallback). You usually don't need to change this
# but create custom variations of scripts on a per-case basis instead.
#BASE_SCRIPT_TYPECLASS = "typeclasses.scripts.Script"

WEBSOCKET_ENABLED = True
WEBSOCKET_PORTS = [8021]

CMDSET_UNLOGGEDIN = "athanor.commands.default_cmdsets.UnloggedinCmdSet"
CMDSET_SESSION = "athanor.commands.default_cmdsets.SessionCmdSet"
CMDSET_CHARACTER = "athanor.commands.default_cmdsets.CharacterCmdSet"
CMDSET_PLAYER = "athanor.commands.default_cmdsets.PlayerCmdSet"

INLINEFUNC_ENABLED = True
#INLINEFUNC_MODULES += []