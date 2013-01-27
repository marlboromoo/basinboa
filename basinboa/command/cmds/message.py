#!/usr/bin/env python
"""
message commands
"""

from basinboa import status
from basinboa.decorator import command

@command
def chat(client, args):
    """
    talk with players in the world.
    useage: chat <MESSAGES..>
    """
    msg = ' '.join(args)
    print '%s says, "%s"' % (status.CHARACTERS[client].get_name(), msg)

    for guest in status.CLIENTS:
        if guest != client:
            guest.send('%s says: %s\n' % (status.CHARACTERS[client].get_name(), msg))
        else:
            guest.send('You say: %s\n' % msg)

