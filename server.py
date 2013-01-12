#!/usr/bin/env python
"""
Startup script for scratchmud.
"""

import sys
sys.path.append('./miniboa')
from miniboa import TelnetServer
from mudlibs import system

SERVER_RUN = True
ASCII_ART = '''
 ___ __ _ _ __ _| |_ __| |_  _ __ _  _ __| |
(_-</ _| '_/ _` |  _/ _| ' \| '  \ || / _` |
/__/\__|_| \__,_|\__\__|_||_|_|_|_\_,_\__,_|

'''

#------------------------------------------------------------------------------
#       Main
#------------------------------------------------------------------------------

if __name__ == '__main__':

    telnet_server = TelnetServer(
        port=7777,
        address='',
        on_connect=system.on_connect,
        on_disconnect=system.on_disconnect,
        timeout = .05
        )
    print(ASCII_ART)
    print(">> Listening for connections on port %d.  CTRL-C to break."
        % telnet_server.port)

    ## Server Loop
    while SERVER_RUN:
        telnet_server.poll()               ## Send, Recv, and look for new connections
        system.kick_idle()                 ## Check for idle clients
        system.process_clients()           ## Check for client input

    print(">> Server shutdown.")
