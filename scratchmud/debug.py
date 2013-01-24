#!/usr/bin/env python
"""
debug utils.
"""
from scratchmud import status

def dump_status():
    """docstring for dump_status"""
    print ""
    print "DEBUG - CLIENTS:%s" % (status.CLIENTS)
    print "DEBUG - UNLOGIN_CLIENTS:%s" % (status.UNLOGIN_CLIENTS)
    print "DEBUG - QUIT_CLIENTS:%s" % (status.QUIT_CLIENTS)
    print "DEBUG - CHARACTERS:%s" % (status.CHARACTERS)
    print ""

