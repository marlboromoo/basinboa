#!/usr/bin/env python
"""
admin commands.
"""
from basinboa import status
from basinboa.decorator import command
from basinboa.message import invalid_args

@command
def shutdown(player, args):
    """docstring for shutdown"""
    status.SERVER_RUN = False

@command
def rooms(player, args):
    """
    admin only. list rooms in the map.
    useage: rooms
    """
    rooms = status.WORLD.locate_player_map(player).get_rooms()
    for room in rooms:
        player.send("%s\n" % repr(room))

@command
def maps(player, args):
    """
    admin only. list map in the world.
    useage: maps
    """
    maps = status.WORLD.get_maps()
    for map_ in maps:
        player.send("%s\n" % repr(map_))

@command
def mobs(player, args):
    """
    admin only. list mob in the world.
    useage: mobs
    """
    maps = status.WORLD.get_maps()
    for map_ in maps:
        for mob in map_.get_mobs():
            player.send("%s\n" % repr(mob))

@command
def goto(player, args):
    """
    admin only. goto any room.
    useage: goto <x> <y> <map_name>
    """
    if len(args) == 3:
        x, y, map_name = args
    elif len(args) == 2:
        x, y = args
        map_name = player.character.map_name
    else:
        return invalid_args(player)
    try:
        x, y = int(x), int(y)
    except Exception:
        return invalid_args(player)
    return status.WORLD.move_to(player.character, (x, y), map_name)

@command
def restore(player, args):
    """docstring for retore"""
    player.character.increase_hp(to_max=True)
    player.character.increase_hp(to_max=True)
    player.send('You feels so good!\n')

