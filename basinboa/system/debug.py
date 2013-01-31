#!/usr/bin/env python
"""
debug utils.
"""
from basinboa import status
from basinboa.system.scheduler import SCHEDULER

def dump_status():
    """docstring for dump_status"""
    print ""
    print "DEBUG - LOBBY:%s" % (status.LOBBY)
    print "DEBUG - _PLAYERS:%s" % (status._PLAYERS)
    print "DEBUG - PLAYERS:%s" % (status.PLAYERS)
    print "DEBUG - SCHEDULER:%s" % (SCHEDULER.get_events())
    for map_ in status.WORLD.get_maps():
        print "DEBUG - %s" % (repr(map_))
    print "DEBUD - %s" % (status.LANG)
    print ""

