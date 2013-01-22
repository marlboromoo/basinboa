#!/usr/bin/env python
"""
Start the server of scratchmud.
reference: http://code.google.com/p/bogboa/source/browse/trunk/server_start.py
"""

import sys
sys.path.append('./miniboa')
from miniboa import TelnetServer
from scratchmud import status
from scratchmud.system import on_connect, on_disconnect, kick_idle, kick_quit, process_clients
from scratchmud.world import WorldLoader
from scratchmud.player import PlayerLoader
from scratchmud.event import Cycle
from scratchmud.ai import MobLoader, mob_actions

ASCII_ART = '''
 ___ __ _ _ __ _| |_ __| |_  _ __ _  _ __| |
(_-</ _| '_/ _` |  _/ _| ' \| '  \ || / _` |
/__/\__|_| \__,_|\__\__|_||_|_|_|_\_,_\__,_|

'''
#------------------------------------------------------------------------------
#       Loading data
#------------------------------------------------------------------------------
status.PLAYER_LOADER = PlayerLoader('data/player')
status.MOB_LOADER = MobLoader('data/mob')
wc = WorldLoader('data/map')
wc.load_all()
status.WORLD = wc.get()

#------------------------------------------------------------------------------
#       Initial Cycle
#------------------------------------------------------------------------------
kick_cycle = Cycle(2)
quit_cycle = Cycle(.1)
process_cycle = Cycle(.1)
walk_cycle = Cycle(10)


#------------------------------------------------------------------------------
#       Main
#------------------------------------------------------------------------------

if __name__ == '__main__':
    telnet_server = TelnetServer(
        port=7777,
        address='',
        on_connect=on_connect,
        on_disconnect=on_disconnect,
        timeout = .05
        )
    print(ASCII_ART)
    print status.WORLD.get_maps()
    print(">> Listening for connections on port %d.  CTRL-C to break."
        % telnet_server.port)

    ## Server Loop
    while status.SERVER_RUN:
        telnet_server.poll()
        kick_cycle.fire(kick_idle)
        quit_cycle.fire(kick_quit)
        process_cycle.fire(process_clients)
        walk_cycle.fire(mob_actions)

    print(">> Server shutdown.")
