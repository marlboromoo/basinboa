#!/usr/bin/env python
"""
informations command.
"""

from basinboa import status
from basinboa.system.decorator import command

@command
def inventory(player, args):
    """docstring for inventoryfname"""
    items = player.character.list_items() 
    if items:
        for item in items:
            player.send_cc_encode("%s(%s)\n" % (item.get_nickname(), item.get_name()))
    else:
        player.send_cc_encode("Nothings.\n")

