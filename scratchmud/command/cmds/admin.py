#!/usr/bin/env python
"""
admin commands.
"""
from scratchmud import status
from scratchmud.message import invalid_args

def rooms(client, args):
    """docstring for rooms"""
    rooms = status.WORLD.locate_client_map(client).get_rooms()
    for room in rooms:
        client.send("%s\n" % repr(room))

def maps(client, args):
    """docstring for maps"""
    maps = status.WORLD.get_maps()
    for map_ in maps:
        client.send("%s\n" % repr(map_))

def mobs(client, args):
    """docstring for mobs"""
    maps = status.WORLD.get_maps()
    for map_ in maps:
        for mob in map_.get_mobs():
            client.send("%s\n" % repr(mob))

def goto(client, args):
    """docstring for goto"""
    if len(args) == 3:
        x, y, map_ = args
    elif len(args) == 2:
        x, y = args
        map_ = status.CHARACTERS[client].map_name
    else:
        return invalid_args(client)
    try:
        x, y = int(x), int(y)
    except Exception:
        return invalid_args(client)
    return status.CHARACTERS[client].goto((x, y), map_)
