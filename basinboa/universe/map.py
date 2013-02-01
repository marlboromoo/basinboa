#!/usr/bin/env python
"""
map contain rooms.
"""

class Map(object):
    """docstring for Map"""
    def __init__(self, name, desc, rooms, coordinates):
        super(Map, self).__init__()
        self.name = name
        self.coordinates = coordinates
        self.desc = desc
        self.players = []
        self.items = []
        self.init_rooms(rooms) #. key is (x,y), value is Room object
        self.init_mobs()

    def __repr__(self):
        return "Map(%s) - %s rooms/%s mobs/%s players" % (
            str(self.name), str(len(self.rooms)), str(len(self.mobs)), str(len(self.players)))

    def get_desc(self):
        """docstring for get_desc"""
        return self.desc

    def get_name(self):
        """docstring for get_name"""
        return self.name

    def has_coordinates(self, xy):
        """docstring for check_coordinates"""
        return True if xy in self.coordinates else False

#------------------------------------------------------------------------------
#       Room
#------------------------------------------------------------------------------

    def init_rooms(self, rooms):
        """docstring for init_rooms"""
        self.rooms = {}
        for room in rooms:
            self.rooms[room.xy] = room

    def get_rooms(self):
        """docstring for get_rooms"""
        return self.rooms.values()

    def get_room(self, xy):
        """docstring for get_room"""
        return self.rooms[xy] if self.rooms.has_key(xy) else None

#------------------------------------------------------------------------------
#       Player
#------------------------------------------------------------------------------

    def add_player(self, player):
        """docstring for add_player"""
        #. add to map
        self.players.append(player)
        #. add to room
        self.get_room(player.character.xy).add_player(player)

    def remove_player(self, player):
        """docstring for remove_player"""
        if player in self.players:
            #. remove from room
            room = self.get_room(player.character.xy)
            if room:
                room.remove_player(player)
            #. remove from map
            self.players.remove(player)

    def get_players(self):
        """docstring for get_players"""
        return self.players


#------------------------------------------------------------------------------
#       Mob
#------------------------------------------------------------------------------

    def init_mobs(self):
        """docstring for init_mobs"""
        self.mobs = []
        for room in self.rooms.values():
            for mob in room.get_mobs():
                self.mobs.append(mob)

    def get_mobs(self):
        """docstring for get_mobs"""
        return self.mobs

    def add_mob(self, mob):
        """add mob to map"""
        #. add to map
        self.mobs.append(mob)
        #. add to room 
        self.get_room(mob.xy).add_mob(mob)

    def remove_mob(self, mob):
        """remove mob from map"""
        #. remove from room
        room = self.get_room(mob.xy)
        if room:
            room.remove_mob(mob)
        #. remove from map
        self.mobs.remove(mob)

#------------------------------------------------------------------------------
#       Item
#------------------------------------------------------------------------------

    def add_item(self, item):
        """add Item object."""
        self.items.append(item)

    def remove_item(self, item):
        """remove Item object"""
        if item in self.items:
            self.items.remove(item)

    def get_items(self):
        """docstring for get_item"""
        return self.items


