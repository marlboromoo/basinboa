#!/usr/bin/env python
"""
combat commands
"""

from scratchmud import status

def kill(client, args):
    """docstring for kill"""
    target_name = args[0] if len(args) > 0 else None
    return status.CHARACTERS[client].kill(target_name) \
            if target_name else client.send('Huh?\n')

