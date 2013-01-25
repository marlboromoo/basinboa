#!/usr/bin/env python
"""
robot !
"""
import copy
import random
import status
from scratchmud.puppet import Puppet
from scratchmud.world import NORTH, SOUTH, EAST, WEST, UP, DOWN 
from scratchmud.message import mob_message_to_room
from scratchmud.uid import Uid
from scratchmud.loader import YamlLoader


class Mob(Puppet, Uid):
    """docstring for Mob"""
    def __init__(self, data):
        super(Mob, self).__init__()
        #. mob type
        self.skeleton = None
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
        #. other
        self.init_prev_location()

    def random_walk(self):
        """random go to room exits"""
        #. not in fight
        if len(self.get_combat_targets()) == 0:
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
                if exit == UP:
                    self.go_up()
                if exit == DOWN:
                    self.go_down()

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

