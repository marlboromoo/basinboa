#!/usr/bin/env python
"""
message commands
"""

from scratchmud import status

def chat(client, args):
    """
    Echo whatever client types to everyone.
    """
    msg = ' '.join(args)
    print '%s says, "%s"' % (status.CHARACTERS[client].get_name(), msg)

    for guest in status.CLIENTS:
        if guest != client:
            guest.send('%s says: %s\n' % (status.CHARACTERS[client].get_name(), msg))
        else:
            guest.send('You say: %s\n' % msg)

