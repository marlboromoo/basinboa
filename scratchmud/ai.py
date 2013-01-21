#!/usr/bin/env python
"""
robot !
"""
import copy
from uid import Uid
from loader import YamlLoader


class Mob(Uid):
    """docstring for Mob"""
    def __init__(self, data):
        super(Mob, self).__init__()
        #. mob type
        self.skeleton = None
        #. status
        self.mobname = None
        self.nickname = None
        self.xy = None
        self.map_name = None
        self.skills = None
        self.spells = None
        self.race = None
        self.job = None
        self.desc = None
        #. combat status
        self.hp = 100
        self.mp = 100
        self.status = None
        #. here we go
        self.reborn(data)

    def __repr__(self):
        return "Mob:%s, skeleton:%s, xy:%s, map:%s, uuid:%s" % (
            str(self.mobname), str(self.skeleton), 
            str(self.xy), str(self.map_name), str(self.uuid))

    def reborn(self, data):
        """docstring for reborn"""
        return self.load(data)

    def dump(self):
        """docstring for dump"""
        return {
            'skeleton' : self.skeleton,
            #. status
            'mobname' : self.mobname,
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
        }

    def load(self, data):
        """docstring for load"""
        self.skeleton = data['skeleton']
        #. status
        self.mobname = data['mobname']
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

class MobLoader(YamlLoader):
    """docstring for MobLoader"""
    def __init__(self, data_dir):
        super(MobLoader, self).__init__(data_dir)
        self.skeletons = {}
        self.load_skeletons()
        self.reborn_mobs()

    def load_skeletons(self):
        """docstring for load_skeletons"""
        datas = self.load_all()
        for data in datas:
            self.skeletons[data.get('skeleton')] = Mob(data)

    def reborn_mobs(self):
        """reborn mobs into world"""
        # TODO: write code...
        pass
    
    def get(self, skeleton):
        """docstring for get"""
        if self.skeletons.has_key(skeleton):
            mob = copy.deepcopy(self.skeletons.get(skeleton))
            mob.generate_uuid()
            return mob

if __name__ == '__main__':
    ml =  MobLoader('../data/mob/')
    dog = ml.get('dog')
    dog.map_name = 'void'
    dog.xy = (1,1)
    cat = ml.get('cat')
    cat.map_name = 'chinese'
    cat.xy = (1,1)
    print dog, cat

