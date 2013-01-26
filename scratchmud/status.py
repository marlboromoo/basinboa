#!/usr/bin/env python
"""
Global status of scratchmud.
reference: http://code.google.com/p/bogboa/source/browse/trunk/mudlib/gvar.py
"""

#------------------------------------------------------------------------------
#       ASCII
#------------------------------------------------------------------------------
ASCII_ART = '''
 ___ __ _ _ __ _| |_ __| |_  _ __ _  _ __| |
(_-</ _| '_/ _` |  _/ _| ' \| '  \ || / _` |
/__/\__|_| \__,_|\__\__|_||_|_|_|_\_,_\__,_|

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





