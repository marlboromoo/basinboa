#!/usr/bin/env python
"""
Useage commands.
"""

from basinboa import status
from basinboa.system.decorator import command
from basinboa.mobile.equipment import SLOT_LEFTHAND, SLOT_RIGHTHAND

@command
def get(player, args):
    """docstring for get"""
    item_name = args[0]
    room = status.WORLD.locate_player_room(player)
    item = room.pop_item(item_name)
    if item:
        player.character.bag.checkin(item)
        player.send_cc_encode("You get %s(%s).\n" % (item.get_nickname(), item.get_name()))
    else:
        player.send_cc_encode('No such item!\n')

@command
def drop(player, args):
    """docstring for drop"""
    item_name = args[0]
    room = status.WORLD.locate_player_room(player)
    item = player.character.bag.checkout(item_name)
    if item:
        room.add_item(item)
        player.send_cc_encode("You drop %s(%s).\n" % (item.get_nickname(), item.get_name()))
    else:
        player.send_cc_encode("You don't have such item!\n")

@command
def wear(player, args):
    """docstring for wear"""
    item_name = args[0]
    item = player.character.bag.checkout(item_name)
    origin_item = None
    if item:
        #. remove equipment first
        origin_item = player.character.equipment.pop_equipment_by_slot(item.slot)
        if origin_item:
            player.character.bag.checkin(origin_item)
        #. try to wear it
        if player.character.equipment.wear(item):
            player.send_cc_encode("You wear %s(%s).\n" % (item.get_nickname(), item.get_name()))
        else:
            player.character.bag.checkin(item)
            player.send_cc_encode("You can't wear %s(%s).\n" % (item.get_nickname(), item.get_name()))
    else:
        player.send_cc_encode("You don't have such item!\n")

@command
def wield(player, args):
    """docstring for wield"""
    #. check args
    item_name = args[0]
    hand = args[1] if len(args) >= 2 else None
    if hand and hand not in ['right', 'left']:
        player.send_cc_encode("You can choose 'right' or 'left' only!\n")
        return
    #. let's go
    character = player.character
    equipment = character.equipment
    item = character.bag.checkout(item_name)
    origin_item = None
    if item:
        auto = True if not hand else False
        right = True if hand == 'right' else False
        #. remove equipment first
        if auto:
            empty_right = equipment.slot_empty(SLOT_RIGHTHAND)
            empty_left = equipment.slot_empty(SLOT_LEFTHAND)
            #. wield weapon on both hand already
            if not empty_right and not empty_left:
                origin_item = equipment.pop_equipment_by_slot(SLOT_RIGHTHAND)
            #. do nothing if one on hand empty
            else:
                pass
        else:
            if right:
                origin_item = equipment.pop_equipment_by_slot(SLOT_RIGHTHAND)
            else:
                origin_item = equipment.pop_equipment_by_slot(SLOT_LEFTHAND)
        if origin_item:
            character.bag.checkin(origin_item)
        #. try to wield it
        if equipment.wield(item, auto=auto, right=right):
            player.send_cc_encode("You wield %s(%s).\n" % (item.get_nickname(), item.get_name()))
        else:
            character.bag.checkin(item)
            player.send_cc_encode("You can't wield %s(%s).\n" % (item.get_nickname(), item.get_name()))
    else:
        player.send_cc_encode("You don't have such item!\n")

@command
def remove(player, args):
    """docstring for remove"""
    item_name = args[0]
    item = player.character.equipment.pop_equipment(item_name)
    if item:
        player.character.bag.checkin(item)
        player.send_cc_encode("You remove %s(%s).\n" % (item.get_nickname(), item.get_name()))
    else:
        player.send_cc_encode("You don't have such equipment!\n")

