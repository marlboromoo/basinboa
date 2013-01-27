#!/usr/bin/env python
"""
Start the server of basinboa.
reference: http://code.google.com/p/bogboa/source/browse/trunk/server_start.py
"""

import sys
import pprint
sys.path.append('./miniboa')
from miniboa import TelnetServer
from basinboa import status
from basinboa.system import on_connect, on_disconnect, login_clients, kick_idle, kick_quit, process_clients, SettingsLoader
from basinboa.world import WorldLoader
from basinboa.character import CharacterLoader
from basinboa.event import Cycle
from basinboa.ai import MobLoader, mob_actions
from basinboa.combat import fight
from basinboa.command.base import register_cmds
#from basinboa.debug import dump_status

if __name__ == '__main__':
    print(status.ASCII_ART)

#------------------------------------------------------------------------------
#       Loading settings
#------------------------------------------------------------------------------
    sl = SettingsLoader('config/')
    status.SERVER_CONFIG = sl.get_server_config()
    print ">> Server settings:"
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(status.SERVER_CONFIG)

#------------------------------------------------------------------------------
#       Loading data
#------------------------------------------------------------------------------
    status.CHARACTER_LOADER = CharacterLoader('data/character')
    status.MOB_LOADER = MobLoader('data/mob')
    wl = WorldLoader('data/map')
    wl.load_all()
    status.WORLD = wl.get()
    status.WORLD.check_links()
    print ">> Maps: " % (status.WORLD.get_maps())
    register_cmds()
    print ">> Register commands: %s" % (status.COMMANDS.keys())

#------------------------------------------------------------------------------
#       Initial Cycle
#------------------------------------------------------------------------------
    login_cycle = Cycle(.3)
    kick_cycle = Cycle(2)
    quit_cycle = Cycle(.2)
    process_cycle = Cycle(.1)
    combat_cycle = Cycle(5)
    walk_cycle = Cycle(10)
    debug_cycle = Cycle(2)

#------------------------------------------------------------------------------
#       Main
#------------------------------------------------------------------------------
    telnet_server = TelnetServer(
        port=status.SERVER_CONFIG.get('port'),
        address=status.SERVER_CONFIG.get('address'),
        on_connect=on_connect,
        on_disconnect=on_disconnect,
        timeout=status.SERVER_CONFIG.get('timeout')
        )
    print(">> Listening for connections on port %d.  CTRL-C to break."
        % telnet_server.port)

    ## Server Loop
    while status.SERVER_RUN:
        telnet_server.poll()
        login_cycle.fire(login_clients)
        kick_cycle.fire(kick_idle)
        quit_cycle.fire(kick_quit)
        process_cycle.fire(process_clients)
        combat_cycle.fire(fight)
        walk_cycle.fire(mob_actions)
        #debug_cycle.fire(dump_status)

    print(">> Server shutdown.")
