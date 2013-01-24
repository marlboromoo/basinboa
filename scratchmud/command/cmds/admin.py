#!/usr/bin/env python
"""
admin commands.
"""
from scratchmud import status

def rooms(self, args):
    """docstring for rooms"""
    rooms = status.WORLD.locate_client_map(self.client).get_rooms()
    for room in rooms:
        self.client.send("%s\n" % repr(room))

def maps(self, args):
    """docstring for maps"""
    maps = status.WORLD.get_maps()
    for map_ in maps:
        self.client.send("%s\n" % repr(map_))

def mobs(self, args):
    """docstring for mobs"""
    maps = status.WORLD.get_maps()
    for map_ in maps:
        for mob in map_.get_mobs():
            self.client.send("%s\n" % repr(mob))
