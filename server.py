#!/usr/bin/env python
"""
Start the server of scratchmud.
reference: http://code.google.com/p/bogboa/source/browse/trunk/server_start.py
"""

import sys
sys.path.append('./miniboa')
from miniboa import TelnetServer
from scratchmud import status
from scratchmud.system import on_connect, on_disconnect, login_clients, kick_idle, kick_quit, process_clients
from scratchmud.world import WorldLoader
from scratchmud.character import CharacterLoader
from scratchmud.event import Cycle
from scratchmud.ai import MobLoader, mob_actions
#from scratchmud.debug import dump_status

ASCII_ART = '''
 ___ __ _ _ __ _| |_ __| |_  _ __ _  _ __| |
(_-</ _| '_/ _` |  _/ _| ' \| '  \ || / _` |
/__/\__|_| \__,_|\__\__|_||_|_|_|_\_,_\__,_|

'''

if __name__ == '__main__':
    print(ASCII_ART)
#------------------------------------------------------------------------------
#       Loading data
#------------------------------------------------------------------------------
    status.CHARACTER_LOADER = CharacterLoader('data/character')
    status.MOB_LOADER = MobLoader('data/mob')
    wl = WorldLoader('data/map')
    wl.load_all()
    status.WORLD = wl.get()
    status.WORLD.check_links()

#------------------------------------------------------------------------------
#       Initial Cycle
#------------------------------------------------------------------------------
    login_cycle = Cycle(.3)
    kick_cycle = Cycle(2)
    quit_cycle = Cycle(.2)
    process_cycle = Cycle(.1)
    walk_cycle = Cycle(10)
    debug_cycle = Cycle(2)

#------------------------------------------------------------------------------
#       Main
#------------------------------------------------------------------------------
    telnet_server = TelnetServer(
        port=7777,
        address='',
        on_connect=on_connect,
        on_disconnect=on_disconnect,
        timeout = .05
        )
    print ">> Maps: %s " % (str(status.WORLD.get_maps()))
    print(">> Listening for connections on port %d.  CTRL-C to break."
        % telnet_server.port)

    ## Server Loop
    while status.SERVER_RUN:
        telnet_server.poll()
        login_cycle.fire(login_clients)
        kick_cycle.fire(kick_idle)
        quit_cycle.fire(kick_quit)
        process_cycle.fire(process_clients)
        walk_cycle.fire(mob_actions)
        #debug_cycle.fire(dump_status)

    print(">> Server shutdown.")
