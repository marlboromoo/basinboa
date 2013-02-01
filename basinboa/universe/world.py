#!/usr/bin/env python
"""
world
"""
from basinboa import status

class World(object):
    """docstring for World"""
    def __init__(self):
        super(World, self).__init__()
        self.maps = {}

    def check_links(self):
        """check links in whole world."""
        print ">> Checking links in whole world .."
        for map_ in self.get_maps():
            for room in map_.get_rooms():
                for link in room.get_links():
                    if not self.has_map(link['map']):
                        print "!! Invalid link: %s, remove it!" % (str(link))
                        room.remove_link(link['exit'])
                        continue
                    else:
                        if not self.get_map(link['map']).has_coordinates(link['xy']):
                            print "!! Invalid link: %s, remove it!" % (str(link))
                            room.remove_link(link['exit'])
                            continue

#------------------------------------------------------------------------------
#       Room
#------------------------------------------------------------------------------

    def locate_player_room(self, player):
        """docstring for locate_player_room"""
        return self.get_map(player.character.map_name).get_room(player.character.xy)

    def locate_player_map(self, player):
        """docstring for locate_player_map"""
        return self.get_map(player.character.map_name)

    def locate_mob_room(self, mob):
        """find room by mob object"""
        return self.get_map(mob.map_name).get_room(mob.xy)

    def locate_mob_map(self, mob):
        """find map by mob object"""
        return self.get_map(mob.map_name)

#------------------------------------------------------------------------------
#       Map
#------------------------------------------------------------------------------

    def add_map(self, map_):
        """docstring for add_map"""
        self.maps[map_.get_name()] = map_

    def get_map(self, map_name):
        """docstring for get_map"""
        return self.maps[map_name] if self.maps.has_key(map_name) else None

    def get_maps(self):
        """docstring for get_maps"""
        return self.maps.values()

    def has_map(self, map_name):
        """docstring for has_map"""
        return True if self.maps.has_key(map_name) else False

#------------------------------------------------------------------------------
#       Player/Character
#------------------------------------------------------------------------------

    def move_character(self, character, symbol, function):
        """move character object between rooms if rooms connected"""
        player = status.PLAYERS[character.name]
        src_room = self.locate_player_room(player)
        x, y = character.xy
        #. check n,s,w,e
        if symbol in src_room.exits:
            dst_xy = function(x, y)
            if dst_xy in src_room.paths:
                #. move character to room
                character.set_prev_location(character.xy, character.map_name)
                character.xy = dst_xy
                #. remove character from source room
                src_room.remove_player(player)
                #. add character to target room
                dst_room = self.locate_player_room(player)
                dst_room.add_player(player)
                return (src_room, dst_room)
        #. check link
        elif src_room.has_link(symbol):
            link = src_room.get_link(symbol)
            return self.move_character_to(character, link['xy'], link['map'])
        else:
            return (None, None)

    def move_character_to(self, character, xy, map_name):
        """move character object between rooms even if rooms not connected"""
        try:
            dst_map = self.get_map(map_name)
            dst_room = dst_map.get_room(xy)
        except Exception:
            dst_map, dst_room = None, None
        if dst_map and dst_room:
            # remove character from origin map & room
            player = status.PLAYERS[character.name]
            src_map = self.locate_player_map(player)
            src_room = src_map.get_room(character.xy)
            src_map.remove_player(player)
            #. move character to destation
            character.set_prev_location(character.xy, character.map_name)
            character.set_location(xy, dst_map.get_name())
            dst_map.add_player(player)
            #return((src_map, src_room), (dst_map, dst_room))
            return (src_room, dst_room)
        else:
            #return ((None, None), (None, None))
            return (None, None)

    def remove_player(self, player):
        """docstring for remove_client"""
        for map_ in self.get_maps():
            map_.remove_player(player)

#------------------------------------------------------------------------------
#       Mob
#------------------------------------------------------------------------------

    def move_mob(self, mob, symbol, function):
        """move mob object between rooms if rooms connected"""
        src_room = self.locate_mob_room(mob)
        x, y = mob.xy
        #. check n,s,w,e
        if symbol in src_room.exits:
            dst_xy = function(x, y)
            if dst_xy in src_room.paths:
                #. move mob to room
                mob.set_prev_location(mob.xy, mob.map_name)
                mob.xy = dst_xy
                #. remove mob from source room
                src_room.remove_mob(mob)
                #. add mob to target room
                dst_room = self.locate_mob_room(mob)
                dst_room.add_mob(mob)
                return (src_room, dst_room)
        #. check link
        elif src_room.has_link(symbol):
            link = src_room.get_link(symbol)
            return self.move_mob_to(mob, link['xy'], link['map'])
        else:
            return (None, None)


    def move_mob_to(self, mob, xy, map_name):
        """move mob object between rooms even if rooms not connected"""
        try:
            dst_map = self.get_map(map_name)
            dst_room = dst_map.get_room(xy)
        except Exception:
            dst_map, dst_room = None, None
        if dst_map and dst_room:
            # remove mob from origin map & room
            src_map = self.locate_mob_map(mob)
            src_room = src_map.get_room(mob.xy)
            src_map.remove_mob(mob)
            #. move mob to destation
            mob.set_prev_location(mob.xy, mob.map_name)
            mob.set_location(xy, dst_map.get_name())
            dst_map.add_mob(mob)
            #return((src_map, src_room), (dst_map, dst_room))
            return (src_room, dst_room)
        else:
            #return ((None, None), (None, None))
            return (None, None)


