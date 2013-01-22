#!/usr/bin/env python
"""
player is puppet, because player control by client
mob is puppet, because mob control by computer
"""

from world import north_xy, south_xy, west_xy, east_xy, NORTH, SOUTH, EAST, WEST

class Puppet(object):
    """docstring for Puppet"""
    def __init__(self):
        super(Puppet, self).__init__()
        #. combat status
        self.hp = 100
        self.mp = 100
        self.status = None
        #. other status
        self.follow_target = None
        self.followers = []

    def __look(self):
        """if have function look then fire it"""
        return self.look() if hasattr(self, 'look') else None

    def go_west(self):
        """docstring for west"""
        self.go(WEST, west_xy, 'west')
        #. notice follower
        for follower in self.followers:
            follower.go_west()
        return self.__look()

    def go_east(self):
        """docstring for east"""
        self.go(EAST, east_xy, 'east')
        #. notice follower
        for follower in self.followers:
            follower.go_east()
        return self.__look()

    def go_north(self):
        """docstring for north"""
        self.go(NORTH, north_xy, 'north')
        #. notice follower
        for follower in self.followers:
            follower.go_north()
        return self.__look()

    def go_south(self):
        """docstring for south"""
        self.go(SOUTH, south_xy, 'south')
        #. notice follower
        for follower in self.followers:
            follower.go_south()
        return self.__look()

    def add_follower(self, object_):
        """add mob/player object to followers list"""
        self.followers.append(object_)

    def remove_follower(self, object_):
        """remove mob/player object from followers list"""
        self.followers.remove(object_)

    def follow(self, object_):
        """follow mob/player"""
        self.follow_target = object_
         

