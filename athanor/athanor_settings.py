r"""
Athanor settings file.

The available options are found in the default settings file found
here:

evennia/settings_default.py

Remember:

This is for settings that Athanor assumes. For your own server's
settings, adjust <mygame>/server/conf/settings.py. See the instructions there for more
information.

"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "Athanor: Advent of Awesome"

# Server ports. If enabled and marked as "visible", the port
# should be visible to the outside world on a production server.
# Note that there are many more options available beyond these.

# Telnet ports. Visible.
TELNET_ENABLED = True
TELNET_PORTS = [4000]
# (proxy, internal). Only proxy should be visible.
WEBSERVER_ENABLED = True
WEBSERVER_PORTS = [(4001, 4002)]
# Telnet+SSL ports, for supporting clients. Visible.
SSL_ENABLED = False
SSL_PORTS = [4003]
# SSH client ports. Requires crypto lib. Visible.
SSH_ENABLED = False
SSH_PORTS = [4004]
# Websocket-client port. Visible.
WEBSOCKET_CLIENT_ENABLED = True
WEBSOCKET_CLIENT_PORT = 4005
# Internal Server-Portal port. Not visible.
AMP_PORT = 4006

# Of course we want these on!
IRC_ENABLED = True
RSS_ENABLED = True

# Let's disable that annoying timeout by default!
IDLE_TIMEOUT = -1

# A lot of MUD-styles may want to change this to 2. Athanor's not really meant for 0 or 1 style, though.
MULTISESSION_MODE = 3

USE_TZ = True
TELNET_OOB_ENABLED = True
WEBSOCKET_ENABLED = True
INLINEFUNC_ENABLED = True

AT_INITIAL_SETUP_HOOK_MODULE = "athanor.at_initial_setup"


SERVER_SESSION_CLASS = "athanor.core.sessions.AthanorSession"


# Command set used on session before account has logged in
CMDSET_UNLOGGEDIN = "athanor.commands.cmdsets.login.AthanorUnloggedinCmdSet"
# Command set used on the logged-in session
CMDSET_SESSION = "athanor.commands.cmdsets.session.AthanorSessionCmdSet"


######################################################################
# Plugin Options
######################################################################



# KINDS CLASSES
DEFAULT_ENTITY_CLASSES = {
    'areas': "athanor.entities.areas.AthanorArea",
    'exits': "athanor.entities.exits.AthanorExit",
    "gateway": "athanor.entities.gateways.AthanorGateway",
    "rooms": "athanor.entities.rooms.AthanorRoom",
    "mobiles": "athanor.entities.mobiles.AthanorMobile",
    "items": "athanor.entities.items.AthanorItem",
    "structures": "athanor.gamedb.structures.AthanorStructure",
    "alliances": "athanor.gamedb.factions.AthanorAlliance",
    "factions": "athanor.gamedb.factions.AthanorFaction",
    "regions": "athanor.gamedb.regions.AthanorRegion",
}


######################################################################
# Account Options
######################################################################
GLOBAL_SCRIPTS['account'] = {
    'typeclass': 'athanor.controllers.account.AthanorAccountController',
    'repeats': -1, 'interval': 50, 'desc': 'Controller for Account System'
}

BASE_ACCOUNT_TYPECLASS = "athanor.gamedb.accounts.AthanorAccount"

# Command set for accounts without a character (ooc)
CMDSET_ACCOUNT = "athanor.commands.cmdsets.account.AthanorAccountCmdSet"


OPTIONS_ACCOUNT_DEFAULT['sys_msg_border'] = ('For -=<>=-', 'Color', 'm')
OPTIONS_ACCOUNT_DEFAULT['sys_msg_text'] = ('For text in sys_msg', 'Color', 'w')
OPTIONS_ACCOUNT_DEFAULT['border_color'] = ("Headers, footers, table borders, etc.", "Color", "M")
OPTIONS_ACCOUNT_DEFAULT['header_star_color'] = ("* inside Header lines.", "Color", "m")
OPTIONS_ACCOUNT_DEFAULT['column_names_color'] = ("Table column header text.", "Color", "G")


######################################################################
# Command Settings
######################################################################

# Turn this on if your game uses North, Northeast, South, Southeast, In, Out, Up, Down, etc.
# It will add default errors for when these directions are attempted but no exit
# exists.
DIRECTIONAL_EXIT_ERRORS = False

######################################################################
# Channel Settings
######################################################################
#BASE_CHANNEL_TYPECLASS = "typeclasses.channels.Channel"

#CHANNEL_COMMAND_CLASS = "evennia.comms.channelhandler.ChannelCommand"

######################################################################
# Character Settings
######################################################################
GLOBAL_SCRIPTS['characters'] = {
    'typeclass': 'athanor.controllers.character.AthanorCharacterController',
    'repeats': -1, 'interval': 50, 'desc': 'Controller for Character System'
}

# Default set for logged in account with characters (fallback)
CMDSET_CHARACTER = "athanor.commands.cmdsets.character.AthanorCharacterCmdSet"

BASE_CHARACTER_TYPECLASS = "athanor.gamedb.characters.AthanorPlayerCharacter"

# If this is enabled, characters will not see each other's true names.
# Instead, they'll see something generic.
NAME_DUB_SYSTEM = False


#DEFAULT_HOME = "limbo/limbo"
START_LOCATION = "limbo/limbo_room"


MAX_NR_CHARACTERS = 10000

GENDER_SUBSTITUTIONS = {
        'male': {
            'gender': 'male',
            'child': 'boy',
            'young': 'young man',
            'adult': 'man',
            'elder': 'old man',
            'prefix': 'Mr. ',
            'prefix_married': 'Mr.',
            'polite': 'sir',
            'subjective': 'he',
            'objective': 'him',
            'possessive': 'his',
        },
        'female': {
            'gender': 'female',
            'child': 'girl',
            'young': 'young woman',
            'adult': 'woman',
            'elder': 'old woman',
            'prefix': 'Ms. ',
            'prefix_married': 'Mrs.',
            'polite': 'miss',
            'subjective': 'she',
            'objective': 'her',
            'possessive': 'hers',
        },
        'neuter': {
            'gender': 'neuter',
            'child': 'being',
            'young': 'young being',
            'adult': 'being',
            'elder': 'old being',
            'prefix': 'Mr. ',
            'prefix_married': 'Mr.',
            'polite': 'sir',
            'subjective': 'it',
            'objective': 'it',
            'possessive': 'its',
        },
        'self': {
            'subjective': 'you',
            'objective': 'you',
            'possessive': 'your',
        }
}

######################################################################
# Entity Settings
######################################################################
# The following Inventory class is the general/fallback for if an inventory type is requested
# that isn't defined in SPECIAL_INVENTORY_CLASSES.
BASE_INVENTORY_CLASS = "athanor.entities.inventory.Inventory"

SPECIAL_INVENTORY_CLASSES = dict()


######################################################################
# RP Event Settings
######################################################################
GLOBAL_SCRIPTS['roleplay'] = {
    'typeclass': 'athanor.controller.rplogger.AthanorRoleplayController',
    'repeats': -1, 'interval': 50, 'desc': 'Event Controller for RP Logger System'
}

######################################################################
# Misc Settings
######################################################################
# Definitely want these OFF in Production.
DEBUG = True
IN_GAME_ERRORS = True


######################################################################
# Plugins
######################################################################

GLOBAL_SCRIPTS['plugin'] = {
    'typeclass': 'athanor.controllers.plugin.AthanorPluginController',
    'repeats': -1, 'interval': 50, 'desc': 'Controller for Plugin System'
}

PLUGIN_CLASS = "athanor.gamedb.plugins.AthanorPlugin"

# This basic plugin is provided to grant a starting area if nothing else is installed.
ATHANOR_PLUGINS = ['athanor.base_plugin']

try:
    from server.conf.plugin_settings import *
except ImportError:
    pass

INSTALLED_APPS = list(INSTALLED_APPS)
INSTALLED_APPS.extend(['athanor.gamedb', 'athanor.traits'])

import athanor
athanor._init(ATHANOR_PLUGINS)

LOCK_FUNC_MODULES = list(LOCK_FUNC_MODULES)

SERVER_SERVICES_PLUGIN_MODULES.extend(athanor.SETTINGS.get("SERVER_SERVICES_PLUGIN_MODULES", list()))
PORTAL_SERVICES_PLUGIN_MODULES.extend(athanor.SETTINGS.get("PORTAL_SERVICES_PLUGIN_MODULES", list()))
INSTALLED_APPS.extend(athanor.SETTINGS.get("INSTALLED_APPS", list()))
LOCK_FUNC_MODULES.extend(athanor.SETTINGS.get("LOCK_FUNC_MODULES", list()))
INPUT_FUNC_MODULES.extend(athanor.SETTINGS.get("INPUT_FUNC_MODULES", list()))
INLINEFUNC_MODULES.extend(athanor.SETTINGS.get("INLINEFUNC_MODULES", list()))
PROTOTYPE_MODULES.extend(athanor.SETTINGS.get("PROTOTYPE_MODULES", list()))
PROTOTYPEFUNC_MODULES.extend(athanor.SETTINGS.get("PROTOTYPEFUNC_MODULES", list()))
PROT_FUNC_MODULES.extend(athanor.SETTINGS.get("PROT_FUNC_MODULES", list()))
CMDSET_PATHS.extend(athanor.SETTINGS.get("CMDSET_PATHS", list()))
TYPECLASS_PATHS.extend(athanor.SETTINGS.get("TYPECLASS_PATHS", list()))
OPTION_CLASS_MODULES.extend(athanor.SETTINGS.get("OPTION_CLASS_MODULES", list()))
VALIDATOR_FUNC_MODULES.extend(athanor.SETTINGS.get("VALIDATOR_FUNC_MODULES", list()))
BASE_BATCHPROCESS_PATHS.extend(athanor.SETTINGS.get("BASE_BATCHPROCESS_PATHS", list()))
STATICFILES_DIRS.extend(athanor.SETTINGS.get("STATICFILES_DIRS", list()))

GLOBAL_SCRIPTS.update(athanor.SETTINGS.get("GLOBAL_SCRIPTS", dict()))
OPTIONS_ACCOUNT_DEFAULT.update(athanor.SETTINGS.get("OPTIONS_ACCOUNT_DEFAULT", dict()))

INSTALLED_APPS = tuple(INSTALLED_APPS)
LOCK_FUNC_MODULES = tuple(LOCK_FUNC_MODULES)
