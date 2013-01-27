#!/usr/bin/env python
"""
base actions of character/mob
"""
from basinboa import status
from basinboa.world import north_xy, south_xy, west_xy, east_xy, NORTH, SOUTH, EAST, WEST, UP, DOWN
from basinboa.world import NORTH_NAME, SOUTH_NAME, EAST_NAME, WEST_NAME, UP_NAME, DOWN_NAME
from basinboa.command.cmds.inspect import look

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
        self.prev_xy = None
        self.map_name = None
        self.prev_map_name = None
        #. combat status
        self.combat_targets = []
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
        """docstring for __look"""
        return look(self.client, None) if self.is_player() else None

    def go_west(self):
        """docstring for west"""
        status.WORLD.move(self, WEST, west_xy, WEST_NAME)
        self.notice_follwers(WEST)
        return self.__look()

    def go_east(self):
        """docstring for east"""
        status.WORLD.move(self, EAST, east_xy, EAST_NAME)
        self.notice_follwers(EAST)
        return self.__look()

    def go_north(self):
        """docstring for north"""
        status.WORLD.move(self, NORTH, north_xy, NORTH_NAME)
        self.notice_follwers(NORTH)
        return self.__look()

    def go_south(self):
        """docstring for south"""
        status.WORLD.move(self, SOUTH, south_xy, SOUTH_NAME)
        self.notice_follwers(SOUTH)
        return self.__look()

    def go_up(self):
        """docstring for go_up"""
        status.WORLD.move(self, UP, None, UP_NAME)
        self.notice_follwers(UP)
        return self.__look()

    def go_down(self):
        """docstring for go_down"""
        status.WORLD.move(self, DOWN, None, DOWN_NAME)
        self.notice_follwers(DOWN)
        return self.__look()

    def notice_follwers(self, direction):
        """notice all followers to move in the same room"""
        for follower in self.followers:
            #. follower must be in the same room
            if follower.xy == self.prev_xy and follower.map_name == self.prev_map_name:
                if follower.is_player():
                    follower.client.send("You follow the %s's steps!\n" % (self.get_name()))
                if direction == UP:
                    follower.go_up()
                if direction == DOWN:
                    follower.go_down()
                if direction == WEST:
                    follower.go_west()
                if direction == EAST:
                    follower.go_east()
                if direction == NORTH:
                    follower.go_north()
                if direction == SOUTH:
                    follower.go_south()

    def add_follower(self, object_):
        """add mob/character object to followers list"""
        self.followers.append(object_)

    def remove_follower(self, object_):
        """remove mob/character object from followers list"""
        self.followers.remove(object_) if object_ in self.followers else None

    def get_followers(self):
        """docstring for get_followers"""
        return self.followers

    def has_follower(self, object_):
        """docstring for has_follower"""
        return True if object_ in self.followers else False

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
        self.combat_targets.append(object_)

    def remove_combat_target(self, object_):
        """docstring for remove_combat_target"""
        self.combat_targets.remove(object_)

    def remove_all_combat_targets(self):
        """docstring for remove_all_combat_targets"""
        self.combat_targets = []

    def get_combat_targets(self):
        """docstring for get_combat_target"""
        return self.combat_targets

    def increase_hp(self, value):
        """docstring for increase_hp"""
        self.hp += value

    def decrease_hp(self, value):
        """docstring for increase_hp"""
        self.hp -= value
        if self.hp <= 0:
            self.client.send_cc('^RYou Dead!^~\n')
            self.hp = 1
            for target in self.get_combat_targets():
                target.remove_combat_target(self)
            self.remove_all_combat_targets()

    def hurt(self, _object):
        """docstring for hurt"""
        damage = 10
        _object.decrease_hp(damage)
        return damage

    def hit(self, _object):
        """docstring for hit"""
        damage = 10
        _object.decrease_hp(damage)
        return damage

    def is_player(self):
        """docstring for is_player"""
        return True if hasattr(self, 'client') else False

    def get_hp(self):
        """docstring for get_hp"""
        return self.hp

    def get_mp(self):
        """docstring for get_mp"""
        return self.mp

    def set_location(self, xy, map_name=None):
        """docstring for set_location"""
        map_name = map_name if map_name else self.map_name
        self.xy = xy
        self.map_name = map_name

    def set_prev_location(self, xy, map_name=None):
        """docstring for set_location"""
        map_name = map_name if map_name else self.map_name
        self.prev_xy = xy
        self.prev_map_name = map_name

    def init_prev_location(self):
        """docstring for set_location"""
        self.prev_xy = self.xy
        self.prev_map_name = self.map_name
