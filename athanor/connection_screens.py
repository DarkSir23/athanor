# -*- coding: utf-8 -*-
"""
Connection screen

This is the text to show the user when they first connect to the game (before
they log in).

To change the login screen in this module, do one of the following:

- Define a function `connection_screen()`, taking no arguments. This will be
  called first and must return the full string to act as the connection screen.
  This can be used to produce more dynamic screens.
- Alternatively, define a string variable in the outermost scope of this module
  with the connection string that should be displayed. If more than one such
  variable is given, Evennia will pick one of them at random.

The commands available to the user when the connection screen is shown
are defined in evennia.default_cmds.UnloggedinCmdSet. The parsing and display
of the screen is done by the unlogged-in "look" command.

"""

from django.conf import settings
from evennia import utils
from athanor.utils.styling import Styler

_STYLER = Styler(None)

CONNECTION_SCREEN = f"""
{_STYLER.styled_header("Welcome!")}
 Welcome to |g{settings.SERVERNAME}|n, version {utils.get_evennia_version("short")}!

 You may login by typin (without the <>'s):
      |wconnect <username> <password>|n
        If you have spaces in your username, enclose it in quotes.

 To create an account, type (without the <>'s):
      |wcreate <username>,<email>,<password>|n
        Please pick something human-pronounceable and appropriate.
        Your account name is not your character name, but it may be
        shown to players.

 Enter |whelp|n for more info. |wlook|n will re-show this screen.
{_STYLER.blank_footer}"""