#!/usr/bin/env python
"""
inspect commands.
"""

from scratchmud import status
from scratchmud.decorator import command

@command
def look(client, args):
    """
    see you want to see.
    useage: look [NAME]
    """
    target_name = args[0] if args else None
    return status.CHARACTERS[client].look(target_name)
