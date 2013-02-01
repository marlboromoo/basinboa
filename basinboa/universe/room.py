#!/usr/bin/env python
"""
room
"""

class Room(object):
    """docstring for Room"""
    def __init__(self, id_, xy, exits, paths):
        super(Room, self).__init__()
        self.xy = xy
        self.id_ = id_
        self.exits = exits
        self.paths = paths
        self.texts = None
        self.mobs = [] #. Mob objects
        self.players = []
        self.links = [] 
        self.items = {} #. key is item_name, value is Item Object

    def __repr__(self):
        return "Room%s%s - %s, %s mobs/%s players/%s items, links: %s" % (
            str(self.id_), str(self.xy), str('/'.join(self.exits)), 
            str(len(self.mobs)), str(len(self.players)), str(len(self.items)), str(self.links))

    def add_link(self, map_, xy, exit):
        """docstring for add_link"""
        if exit in self.exits or self.has_link(exit):
            print "!! Link error, exit: '%s' alreay exist." % (exit)
            return False
        self.links.append({'exit' : exit, 'map' : map_, 'xy' : xy})
        return True

    def remove_link(self, exit):
        """docstring for remove_link"""
        for link in self.links:
            if link['exit'] == exit:
                self.links.remove(link)
                break

    def get_link(self, exit):
        """docstring for get_link"""
        for link in self.links:
            if link['exit'] == exit:
                return link
        return None

    def get_links(self):
        """docstring for get_links"""
        return self.links

    def has_link(self, exit):
        """docstring for has_link"""
        for link in self.links:
            if link['exit'] == exit:
                return True
        return False

    def get_exits(self):
        """docstring for get_exits"""
        if len(self.links) > 0:
            exits = []
            exits.extend(self.exits)
            for link in self.links:
                exits.append(link['exit'])
            return exits
        else:
            return self.exits

#------------------------------------------------------------------------------
#       Player
#------------------------------------------------------------------------------

    def add_player(self, player):
        """docstring for add_player"""
        self.players.append(player)

    def remove_player(self, player):
        """docstring for remove_player"""
        self.players.remove(player) if player in self.players else None

    def get_players(self):
        """docstring for get_players"""
        return self.players

    def get_player_by_name(self, name):
        """docstring for get_player_by_name"""
        for player in self.players:
            if player.character.name == name:
                return player
        return None

#------------------------------------------------------------------------------
#       Mob
#------------------------------------------------------------------------------

    def add_mob(self, mob):
        """docstring for add_mob"""
        self.mobs.append(mob)

    def get_mobs(self):
        """docstring for get_mobs"""
        return self.mobs

    def remove_mob(self, mob):
        """docstring for add_client"""
        if mob in self.mobs:
            self.mobs.remove(mob)

    def remove_mobs(self):
        """docstring for remove_mobs"""
        self.mobs = []

    def get_mob_by_name(self, name):
        """return mob object by name else None"""
        for mob in self.mobs:
            if name == mob.name:
                return mob
        return None

#------------------------------------------------------------------------------
#       Item
#------------------------------------------------------------------------------

    def add_item(self, item):
        """add Item object."""
        self.items[item.get_name()] = item

    def remove_item(self, item):
        """remove Item object"""
        if self.items.has_key(item.get_name()):
            self.items.pop(item)

    def remove_items(self):
        """docstring for remove_items"""
        self.items = {}

    def get_item(self, item_name):
        """docstring for get_item_by_name"""
        if self.items.has_key(item_name):
            return self.items[item_name]
        return None

    def get_items(self):
        """docstring for get_items"""
        return self.items.values()

    def pop_item(self, item_name):
        """docstring for checkout"""
        if self.items.has_key(item_name):
            return self.items.pop(item_name)
        return None

    def list_items(self):
        """docstring for list_items"""
        return self.items.values()

    def has_item(self, item_name):
        """docstring for has_item"""
        return True if self.item.has_key(item_name) else False

