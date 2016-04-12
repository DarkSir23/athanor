"""
Evennia settings file.

The full options are found in the default settings file found here:

/home/volund/PycharmProjects/evennia/evennia/settings_default.py

Note: Don't copy more from the default file than you actually intend to
change; this will make sure that you don't overload upstream updates
unnecessarily.

"""

# Use the defaults from Evennia unless explicitly overridden
import os
from evennia.settings_default import *
from server.conf.storyteller_settings import *

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "Athanor"

# Path to the game directory (use EVENNIA_DIR to refer to the
# core evennia library)
GAME_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Place to put log files
LOG_DIR = os.path.join(GAME_DIR, "server", "logs")
SERVER_LOG_FILE = os.path.join(LOG_DIR, 'server.log')
PORTAL_LOG_FILE = os.path.join(LOG_DIR, 'portal.log')
HTTP_LOG_FILE = os.path.join(LOG_DIR, 'http_requests.log')

# Other defaults
PROTOTYPE_MODULES = ("world.prototypes",)

######################################################################
# Evennia Database config
######################################################################

# Database config syntax:
# ENGINE - path to the the database backend. Possible choices are:
#            'django.db.backends.sqlite3', (default)
#            'django.db.backends.mysql',
#            'django.db.backends.postgresql_psycopg2',
#            'django.db.backends.oracle' (untested).
# NAME - database name, or path to the db file for sqlite3
# USER - db admin (unused in sqlite3)
# PASSWORD - db admin password (unused in sqlite3)
# HOST - empty string is localhost (unused in sqlite3)
# PORT - empty string defaults to localhost (unused in sqlite3)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(GAME_DIR, "server", "evennia.db3"),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': ''
        }}

######################################################################
# Django web features
######################################################################

# Absolute path to the directory that holds file uploads from web apps.
# Example: "/home/media/media.lawrence.com"
MEDIA_ROOT = os.path.join(GAME_DIR, "web", "media")

# The master urlconf file that contains all of the sub-branches to the
# applications. Change this to add your own URLs to the website.
ROOT_URLCONF = 'web.urls'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure
# to use a trailing slash. Django1.4+ will look for admin files under
# STATIC_URL/admin.
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(GAME_DIR, "web", "static")

# Directories from which static files will be gathered from.
STATICFILES_DIRS = (
    os.path.join(GAME_DIR, "web", "static_overrides"),
    os.path.join(EVENNIA_DIR, "web", "static"),)

# We setup the location of the website template as well as the admin site.
TEMPLATE_DIRS = (
    os.path.join(GAME_DIR, "web", "template_overrides", ACTIVE_TEMPLATE),
    os.path.join(GAME_DIR, "web", "template_overrides"),
    os.path.join(EVENNIA_DIR, "web", "templates", ACTIVE_TEMPLATE),
    os.path.join(EVENNIA_DIR, "web", "templates"),)

# The secret key is randomly seeded upon creation. It is used to sign
# Django's cookies. Do not share this with anyone. Changing it will
# log out all active web browsing sessions. Game web client sessions
# may survive.
SECRET_KEY = ';i$:`9<A]!a5jnFKG"+JL&S}O1Y3|%vE*Bm{/-(Z'

# ATHANOR SETTINGS

MULTISESSION_MODE = 3
USE_TZ = True
MAX_NR_CHARACTERS = 4
IRC_ENABLED = True
TELNET_OOB_ENABLED = True

DEFAULT_HOME = "#2"
START_LOCATION = "#2"

# Determines whether non-admin can create characters at all.
PLAYER_CREATE = True

# Let's disable that annoying timeout by default!
IDLE_TIMEOUT = -1

# Enabling some extra Django apps!
INSTALLED_APPS = INSTALLED_APPS + ('world.database.communications',
                                   'world.database.info',
                                   'world.database.bbs.apps.BBSConfig',
                                   'world.database.groups.apps.GroupConfig',
                                   'world.database.scenes.apps.SceneConfig',
                                   'world.database.storyteller.apps.StorytellerConfig',
                                   'world.database.grid.apps.GridConfig',
                                   'world.database.mushimport',)

LOCK_FUNC_MODULES = LOCK_FUNC_MODULES + ("world.database.groups.locks",)


# TYPECLASS STUFF
BASE_CHANNEL_TYPECLASS = "typeclasses.channels.PublicChannel"


# PLAYER SETTINGS
PLAYER_SETTING_DEFAULTS = {
    'look_alert': True,
    'finger_alert': True,
    'bbscan_alert': True,
    'mail_alert': True,
    'scenes_alert': True,
    'namelink_channel': True,
    'quotes_channel': 'n',
    'speech_channel': 'n',
    'border_color': 'M',
    'columnname_color': 'G',
    'headerstar_color': 'm',
    'headertext_color': 'w',
    'msgborder_color': 'm',
    'msgtext_color': 'w',
    'oocborder_color': 'x',
    'ooctext_color': 'r',
    'page_color': 'n',
    'outpage_color': 'n',
    'exitname_color': 'n',
    'exitalias_color': 'n',
}