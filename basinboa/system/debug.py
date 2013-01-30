#!/usr/bin/env python
"""
debug utils.
"""
from basinboa import status
from basinboa.system.monitor import disconnect

def dump_status():
    """docstring for dump_status"""
    print ""
    print "DEBUG - LOBBY:%s" % (status.LOBBY)
    print "DEBUG - _PLAYERS:%s" % (status._PLAYERS)
    print "DEBUG - PLAYERS:%s" % (status.PLAYERS)
    print "DEBUG - QUIT_CLIENTS:%s" % (status.QUIT_CLIENTS)
    for map_ in status.WORLD.get_maps():
        print "DEBUG - %s" % (repr(map_))
    print ""

def test_quit():
    for client in status.CLIENTS:
        if client.active and client.cmd_ready:
            if client.get_command() == 'quit':
                disconnect(client) 
                status.CLIENTS.remove(client)
                status.UNLOGIN_CLIENTS.pop(client)
            else:
                client.send('Huh?\n')


