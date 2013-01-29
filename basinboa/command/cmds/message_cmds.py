#!/usr/bin/env python
"""
message commands
"""

from basinboa import status
from basinboa.decorator import command

@command
def chat(player, args):
    """
    talk with players in the world.
    useage: chat <MESSAGES..>
    """
    msg = ' '.join(args)
    for player_ in status.PLAYERS:
        if player_ != player:
            player_.send('%s says: %s\n' % (player.get_name(), msg))
        else:
            player.send('You say: %s\n' % msg)

