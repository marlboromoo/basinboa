#!/usr/bin/env python
"""
Start the server of basinboa.
reference: http://code.google.com/p/bogboa/source/browse/trunk/server_start.py
"""

import sys
sys.path.append('./miniboa')
from miniboa import TelnetServer
from basinboa import status
from basinboa.system.scheduler import SCHEDULER, Cycle
from basinboa.universe.world import WorldLoader
from basinboa.mobile.character import CharacterLoader
from basinboa.system.config import ConfigLoader
from basinboa.system.language import LanguageLoader
from basinboa.mobile.mob import MobLoader, mob_actions
from basinboa.combat.fight import fight
from basinboa.command.base import register_cmds
from basinboa.system.debug import dump_status
from basinboa.system.monitor import on_connect, on_disconnect, kick_idle, process_lobby, process_players

if __name__ == '__main__':
    print(status.ASCII_ART)

#------------------------------------------------------------------------------
#       Load Settings
#------------------------------------------------------------------------------
    status.SERVER_CONFIG = ConfigLoader('config/').get_server_config()

#------------------------------------------------------------------------------
#       Load datas
#------------------------------------------------------------------------------
    status.CHARACTER_LOADER = CharacterLoader('data/character/')
    status.MOB_LOADER = MobLoader('data/mob/')
    wl = WorldLoader('data/map/')
    wl.load_all()
    status.WORLD = wl.get()
    status.WORLD.check_links()
    print ">> Maps: " % (status.WORLD.get_maps())
    register_cmds()
    print ">> Register commands: %s" % (status.COMMANDS.keys())
    status.LANG = LanguageLoader('data/language/').get()

#------------------------------------------------------------------------------
#       Initial Cycles
#------------------------------------------------------------------------------
    Cycle(.1, process_lobby)
    Cycle(.1, process_players)
    Cycle(2, kick_idle)
    Cycle(5, fight)
    Cycle(10, mob_actions)
    Cycle(2, dump_status)

#------------------------------------------------------------------------------
#       Initial Telnet Server
#------------------------------------------------------------------------------
    telnet_server = TelnetServer(
        port=status.SERVER_CONFIG.port,
        address=status.SERVER_CONFIG.address,
        on_connect=on_connect,
        on_disconnect=on_disconnect,
        timeout=status.SERVER_CONFIG.timeout,
        )
    print(">> Listening for connections on port %d.  CTRL-C to break."
        % telnet_server.port)

#------------------------------------------------------------------------------
#       Main Server Loop
#------------------------------------------------------------------------------
    while status.SERVER_RUN:
        telnet_server.poll()
        SCHEDULER.tick()

    print(">> Server shutdown.")
