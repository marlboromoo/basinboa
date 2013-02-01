#!/usr/bin/env python
"""
Useage commands.
"""

from basinboa import status
from basinboa.system.decorator import command

@command
def get(player, args):
    """docstring for get"""
    item_name = args[0]
    room = status.WORLD.locate_player_room(player)
    item = room.pop_item(item_name)
    if item:
        player.character.checkin(item)
        player.send_cc_encode("You get %s(%s).\n" % (item.get_nickname(), item.get_name()))
    else:
        player.send_cc_encode('No such item!\n')

@command
def drop(player, args):
    """docstring for drop"""
    item_name = args[0]
    room = status.WORLD.locate_player_room(player)
    item = player.character.checkout(item_name)
    if item:
        room.add_item(item)
        player.send_cc_encode("You drop %s(%s).\n" % (item.get_nickname(), item.get_name()))
    else:
        player.send_cc_encode("You don't have such item!\n")

