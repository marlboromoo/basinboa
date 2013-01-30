#!/usr/bin/env python
"""
base actions of character/mob
"""
from basinboa import status
from basinboa.message.broadcast import message_to_room, player_message_to_room
from basinboa.command.cmds.inspect_cmds import look
from basinboa.universe.direction import north_xy, south_xy, west_xy, east_xy, NORTH, SOUTH, EAST, WEST, UP, DOWN, NORTH_NAME, SOUTH_NAME, EAST_NAME, WEST_NAME, UP_NAME, DOWN_NAME

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
        self.hp = (100, 100) #. current, max
        self.mp = (100, 100) #. current, max
        self.status = None
        #. other status
        self.follow_target = None
        self.followers = []

    def get_name(self):
        """docstring for get_name"""
        return self.name

    #def __look(self):
    #    """docstring for __look"""
    #    return look(status.CHARACTERS[self], None) if not self.is_mob else None

    def _move(self, symbol, func=None):
        """docstring for _move"""
        mfunc = getattr(status.WORLD, 'move_mob') if self.is_mob \
        else getattr(status.WORLD, 'move_character')
        src_room, dst_room = mfunc(self, symbol, func)
        return src_room, dst_room

    def go_west(self):
        """docstring for west"""
        src_room, dst_room = self._move(WEST, west_xy)
        if src_room and dst_room:
            self.notice_players(src_room, dst_room, WEST_NAME)
            self.notice_follwers(WEST)
            return True
        return False

    def go_east(self):
        """docstring for east"""
        src_room, dst_room = self._move(EAST, east_xy) 
        if src_room and dst_room:
            self.notice_players(src_room, dst_room, EAST_NAME)
            self.notice_follwers(EAST)
            return True
        return False

    def go_north(self):
        """docstring for north"""
        src_room, dst_room = self._move(NORTH, north_xy)
        if src_room and dst_room:
            self.notice_players(src_room, dst_room, NORTH_NAME)
            self.notice_follwers(NORTH)
            return True
        return False

    def go_south(self):
        """docstring for south"""
        src_room, dst_room = self._move(SOUTH, south_xy)
        if src_room and dst_room:
            self.notice_players(src_room, dst_room, SOUTH_NAME)
            self.notice_follwers(SOUTH)
            return True
        return False

    def go_up(self):
        """docstring for go_up"""
        src_room, dst_room = self._move(UP)
        if src_room and dst_room:
            self.notice_players(src_room, dst_room, UP_NAME)
            self.notice_follwers(UP)
            return True
        return False

    def go_down(self):
        """docstring for go_down"""
        src_room, dst_room = self._move(DOWN)
        if src_room and dst_room:
            self.notice_players(src_room, dst_room, DOWN_NAME)
            self.notice_follwers(DOWN)
            return True
        return False

    def notice_follwers(self, direction):
        """notice all followers to move in the same room"""
        for follower in self.followers:
            #. follower must be in the same room
            if follower.xy == self.prev_xy and follower.map_name == self.prev_map_name:
                if not follower.is_mob:
                    player = status.PLAYERS[follower.get_name()]
                    player.send("You follow the %s's steps!\n" % (self.get_name()))
                    look(player, None)
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

    def notice_players(self, src_room, dst_room, direction_name):
        """docstring for notice_players"""
        msg_go = "%s go to %s.\n" % (self.name, direction_name)
        msg_come = "%s come to here.\n" % (self.name)
        if self.is_mob:
            message_to_room(src_room, msg_go)
            message_to_room(dst_room, msg_come)
        else:
            player = status.PLAYERS[self.name]
            message_to_room(src_room, msg_go)
            player_message_to_room(player, msg_come)

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

    def increase_point(self, attr, value, to_max):
        """docstring for increase_point"""
        current, max_ = attr
        if to_max:
            attr = (max_, max_)
        else:
            current += value
            attr = (current, max_)
        return attr

    def decrease_point(self, attr, value):
        """docstring for decrease_point"""
        current, max_ = attr
        return (current - value, max_)

    def increase_hp(self, value=1, to_max=False):
        """docstring for increase_hp"""
        self.hp = self.increase_point(self.hp, value, to_max)

    def decrease_hp(self, value=1):
        """docstring for increase_hp"""
        self.hp = self.decrease_point(self.hp, value)
        current, max_ = self.hp
        if current <= 0:
            status.CHARACTERS[self].send_cc('^RYou Dead!^~\n')
            self.hp = (1, max_)
            for target in self.get_combat_targets():
                target.remove_combat_target(self)
            self.remove_all_combat_targets()

    def increase_mp(self, value=1, to_max=False):
        """docstring for increase_mp"""
        self.mp= self.increase_point(self.mp, value, to_max)

    def decrease_mp(self, value=1):
        """docstring for decrease_mp"""
        self.mp = self.decrease_point(self.mp, value)

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
