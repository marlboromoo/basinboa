#!/usr/bin/env python
"""
robot !
"""
import copy
import random
import status
from puppet import Puppet
from world import NORTH, SOUTH, EAST, WEST
from message import mob_message_to_room
from uid import Uid
from loader import YamlLoader


class Mob(Puppet, Uid):
    """docstring for Mob"""
    def __init__(self, data):
        super(Mob, self).__init__()
        #. mob type
        self.skeleton = None
        #. status
        self.name = None
        self.nickname = None
        self.xy = None
        self.map_name = None
        self.skills = None
        self.spells = None
        self.race = None
        self.job = None
        self.desc = None
        #. talk
        self.gossip = None
        #. here we go
        self.reborn(data)

    def __repr__(self):
        return "Mob:%s, skeleton:%s, xy:%s, map:%s, uuid:%s" % (
            str(self.name), str(self.skeleton), 
            str(self.xy), str(self.map_name), str(self.uuid))

    def reborn(self, data):
        """docstring for reborn"""
        return self.load(data)

    def dump(self):
        """docstring for dump"""
        return {
            'skeleton' : self.skeleton,
            #. status
            'name' : self.name,
            'nickname' : self.nickname,
            'xy' : self.xy,
            'map_name' : self.map_name,
            'skills' : self.skills,
            'spells' : self.spells,
            'race' : self.race,
            'desc' : self.desc,
            #. combat status
            'hp' : self.hp,
            'mp' : self.mp,
            'status' : self.status,
            #.talk
            'gossip' : self.gossip,
        }

    def load(self, data):
        """docstring for load"""
        self.skeleton = data['skeleton']
        #. status
        self.name = data['name']
        self.nickname = data['nickname']
        self.xy = data['xy']
        self.map_name = data['map_name']
        self.skills = data['skills']
        self.spells = data['spells']
        self.race = data['race']
        self.desc = data['desc']
        #. combat status
        self.hp = data['hp']
        self.mp = data['mp']
        self.status = data['status']
        #. talk
        self.gossip = data['gossip']

    def go(self, symbol, function, message):
        """docstring for go"""
        room = status.WORLD.locate_mob_room(self)
        x, y = self.xy
        if symbol in room.exits:
            dst_xy = function(x, y)
            if dst_xy in room.paths:
                #. message to all the characters in room
                mob_message_to_room(self, '%s go to %s!\n' % (self.name, message))
                #. move mob to room
                self.xy = dst_xy
                #. remove mob from source room
                room.remove_mob(self)
                #. add mob to target room
                status.WORLD.locate_mob_room(self).add_mob(self)
                #. send message to all the characters in target room
                mob_message_to_room(self, '%s come to here!\n' % (self.name))

    def random_walk(self):
        """random go to room exits"""
        if random.choice([True, False, False]):
            room = status.WORLD.locate_mob_room(self)
            exit = random.choice(room.exits)
            if exit == NORTH:
                self.go_north()
            if exit == SOUTH:
                self.go_south()
            if exit == WEST:
                self.go_west()
            if exit == EAST:
                self.go_east()

    def random_say(self):
        """docstring for random_say"""
        if random.choice([True, False]) and self.gossip and type(self.gossip) == list:
            mob_message_to_room(self, '%s say: %s\n' % 
                                (self.name, random.choice(self.gossip)))

def mob_actions():
    """docstring for mob_walking"""
    maps = status.WORLD.get_maps()
    for map_ in maps:
        mobs = map_.get_mobs()
        for mob in mobs:
            mob.random_walk()
            mob.random_say()
        
class MobLoader(YamlLoader):
    """docstring for MobLoader"""
    def __init__(self, data_dir):
        super(MobLoader, self).__init__(data_dir)
        self.skeletons = {}
        self.load_skeletons()

    def load_skeletons(self):
        """docstring for load_skeletons"""
        datas = self.load_all()
        for data in datas:
            self.skeletons[data.get('skeleton')] = Mob(data)

    def get(self, skeleton):
        """docstring for get"""
        if self.skeletons.has_key(skeleton):
            mob = copy.deepcopy(self.skeletons.get(skeleton))
            mob.generate_uuid()
            return mob

