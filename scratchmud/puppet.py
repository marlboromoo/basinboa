#!/usr/bin/env python
"""
base actions of character/mob
"""

from world import north_xy, south_xy, west_xy, east_xy, NORTH, SOUTH, EAST, WEST, UP, DOWN
from world import NORTH_NAME, SOUTH_NAME, EAST_NAME, WEST_NAME, UP_NAME, DOWN_NAME

class Puppet(object):
    """docstring for Puppet"""
    def __init__(self):
        super(Puppet, self).__init__()
        self.name = None
        self.nickname = None
        self.desc = None
        self.skills = None
        self.spells = None
        self.race = None
        self.job = None
        #. geo
        self.xy = None
        self.map_name = None
        #. combat status
        self.combat_target = []
        self.hp = 100
        self.mp = 100
        self.status = None
        #. other status
        self.follow_target = None
        self.followers = []

    def get_name(self):
        """docstring for get_name"""
        return self.name

    def __look(self):
        """if have function look then fire it"""
        return self.look() if hasattr(self, 'look') else None

    def go_west(self):
        """docstring for west"""
        self.go(WEST, west_xy, WEST_NAME)
        #. notice follower
        for follower in self.followers:
            follower.go_west()
        return self.__look()

    def go_east(self):
        """docstring for east"""
        self.go(EAST, east_xy, EAST_NAME)
        #. notice follower
        for follower in self.followers:
            follower.go_east()
        return self.__look()

    def go_north(self):
        """docstring for north"""
        self.go(NORTH, north_xy, NORTH_NAME)
        #. notice follower
        for follower in self.followers:
            follower.go_north()
        return self.__look()

    def go_south(self):
        """docstring for south"""
        self.go(SOUTH, south_xy, SOUTH_NAME)
        #. notice follower
        for follower in self.followers:
            follower.go_south()
        return self.__look()

    def go_up(self):
        """docstring for go_up"""
        self.go(UP, None, UP_NAME)
        for follower in self.followers:
            follower.go_up()
        return self.__look()

    def go_down(self):
        """docstring for go_down"""
        self.go(DOWN, None, DOWN_NAME)
        for follower in self.followers:
            follower.go_down()
        return self.__look()

    def add_follower(self, object_):
        """add mob/character object to followers list"""
        self.followers.append(object_)

    def remove_follower(self, object_):
        """remove mob/character object from followers list"""
        self.followers.remove(object_) if object_ in self.followers else None

    def get_followers(self):
        """docstring for get_followers"""
        return self.followers

    def start_follow(self, object_):
        """follow mob/character"""
        if object_ == self:
            self.stop_follow()
        else:
            self.follow_target = object_

    def stop_follow(self):
        """docstring for stop_follow"""
        if self.follow_target:
            self.follow_target.remove_follower(self)
            self.follow_target = None
        if self in self.followers:
            self.followers.remove(self)

    def get_desc(self):
        """docstring for get_desc"""
        return str(self.desc)

    def add_combat_target(self, object_):
        """docstring for set_combat_target"""
        self.combat_target.append(object_)

    def remove_combat_target(self, object_):
        """docstring for remove_combat_target"""
        self.combat_target.remove(object_)

    def is_player(self):
        """docstring for is_player"""
        return True if hasattr(self, 'client') else False

