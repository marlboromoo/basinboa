#!/usr/bin/env python
"""
Global status of basinboa.
reference: http://code.google.com/p/bogboa/source/browse/trunk/mudlib/gvar.py
"""

#------------------------------------------------------------------------------
#       ASCII
#------------------------------------------------------------------------------
ASCII_ART = '''
 ____            _       ____              
| __ )  __ _ ___(_)_ __ | __ )  ___   __ _ 
|  _ \ / _` / __| | '_ \|  _ \ / _ \ / _` |
| |_) | (_| \__ \ | | | | |_) | (_) | (_| |
|____/ \__,_|___/_|_| |_|____/ \___/ \__,_|
                            Testing Server
'''

#------------------------------------------------------------------------------
#       Server
#------------------------------------------------------------------------------
SERVER_CONFIG = None
SERVER_RUN = True
IDLE_TIMEOUT = 300
CLIENTS = []
QUIT_CLIENTS = []
UNLOGIN_CLIENTS = {}

#------------------------------------------------------------------------------
#       World
#------------------------------------------------------------------------------
WORLD = None
CHARACTER_LOADER = None
MOB_LOADER = None
CHARACTERS = {}
COMMANDS = {} #. key is functin(command) name value is function(command)





