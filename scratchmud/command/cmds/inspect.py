#!/usr/bin/env python
"""
inspect commands.
"""

from scratchmud import status

def look(self, args):
    """docstring for look"""
    target_name = args[0] if args else None
    return status.CHARACTERS[self.client].look(target_name)
