#!/usr/bin/env python
"""
combat commands
"""

from scratchmud import status

def kill(self, args):
    """docstring for kill"""
    target_name = args[0] if len(args) > 0 else None
    return status.CHARACTERS[self.client].kill(target_name) \
            if target_name else self.client.send('Huh?\n')

