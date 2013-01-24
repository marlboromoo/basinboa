#!/usr/bin/env python
"""
message commands
"""

from scratchmud import status

def chat(self, args):
    """
    Echo whatever client types to everyone.
    """
    msg = ' '.join(args)
    print '%s says, "%s"' % (self.character.get_name(), msg)

    for guest in status.CLIENTS:
        if guest != self.client:
            guest.send('%s says: %s\n' % (self.character.get_name(), msg))
        else:
            guest.send('You say: %s\n' % msg)

