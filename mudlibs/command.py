#!/usr/bin/env python
"""
commands !
"""

def chat(client, clients):
    """
    Echo whatever client types to everyone.
    """
    global SERVER_RUN
    msg = client.get_command()
    print '%s says, "%s"' % (client.addrport(), msg)

    for guest in clients:
        if guest != client:
            guest.send('%s says, %s\n' % (client.soul.get_name(), msg))
        else:
            guest.send('You say, %s\n' % msg)

    cmd = msg.lower()
    ## bye = disconnect
    if cmd == 'bye':
        client.active = False
    ## shutdown == stop the server
    elif cmd == 'shutdown':
        SERVER_RUN = False
