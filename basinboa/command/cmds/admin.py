#!/usr/bin/env python
"""
admin commands.
"""
from basinboa import status
from basinboa.decorator import command
from basinboa.message import invalid_args

@command
def shutdown(client, args):
    """docstring for shutdown"""
    status.SERVER_RUN = False

@command
def rooms(client, args):
    """
    admin only. list rooms in the map.
    useage: rooms
    """
    rooms = status.WORLD.locate_client_map(client).get_rooms()
    for room in rooms:
        client.send("%s\n" % repr(room))

@command
def maps(client, args):
    """
    admin only. list map in the world.
    useage: maps
    """
    maps = status.WORLD.get_maps()
    for map_ in maps:
        client.send("%s\n" % repr(map_))

@command
def mobs(client, args):
    """
    admin only. list mob in the world.
    useage: mobs
    """
    maps = status.WORLD.get_maps()
    for map_ in maps:
        for mob in map_.get_mobs():
            client.send("%s\n" % repr(mob))

@command
def goto(client, args):
    """
    admin only. goto any room.
    useage: goto <x> <y> <map_name>
    """
    if len(args) == 3:
        x, y, map_name = args
    elif len(args) == 2:
        x, y = args
        map_name = status.CHARACTERS[client].map_name
    else:
        return invalid_args(client)
    try:
        x, y = int(x), int(y)
    except Exception:
        return invalid_args(client)
    return status.WORLD.move_to(status.CHARACTERS[client], (x, y), map_name)

@command
def restore(client, args):
    """docstring for retore"""
    character = status.CHARACTERS.get(client)
    character.increase_hp(to_max=True)
    character.increase_hp(to_max=True)
    client.send('You feels so good!\n')

