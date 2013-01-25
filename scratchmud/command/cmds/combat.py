#!/usr/bin/env python
"""
combat commands
"""

from scratchmud import status
from scratchmud.decorator import command

@command
def kill(client, args):
    """
    kill the mob, but can't kill player.
    useage: kill <MOB_NAME>
    """
    target_name = args[0] if len(args) > 0 else None
    return status.CHARACTERS[client].kill(target_name) \
            if target_name else client.send('Huh?\n')

