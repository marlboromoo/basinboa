#!/usr/bin/env python
"""
character character
"""
from basinboa import status
from basinboa.system.loader import YamlLoader
from basinboa.mobile.puppet import Puppet

ROLE_ADMIN = 'admin'
ROLE_USER = 'user'

class Character(Puppet):
    """docstring for Character"""
    def __init__(self, name=None):
        super(Character, self).__init__()
        self.name = name
        self.is_mob = False
        self.client = None
        self.login = None
        self.password = None
        self.xy = (1, 0)
        self.map_name = 'void'
        self.role = ROLE_USER
        self.prompt = None

    def __repr__(self):
        return "User:%s, role:%s, xy:%s, map:%s" % (
            str(self.name), str(self.role), str(self.xy), str(self.map_name))

    def set_name(self, name):
        """docstring for set_name"""
        self.name = name

    def set_password(self, password):
        """docstring for set_password"""
        self.password = password

    def get_password(self):
        """docstring for get_password"""
        return self.password

    def set_role(self, role):
        """docstring for set_role"""
        self.role = role

    def get_role(self):
        """docstring for get_role"""
        return self.role

    def is_admin(self):
        """docstring for is_admin"""
        return True if self.get_role() == ROLE_ADMIN else False

    def dump(self):
        """docstring for dump"""
        return {
            'login' : self.login,
            'name' : self.name,
            'password' : self.password,
            #. status
            'nickname' : self.nickname,
            'xy' : self.xy,
            'map_name' : self.map_name,
            'skills' : self.skills,
            'spells' : self.spells,
            'race' : self.race,
            'role' : self.role,
            'job' : self.job,
            'prompt' : self.prompt,
            #. combat status
            'hp' : self.hp,
            'mp' : self.mp,
            'status' : self.status,
        }

    def load(self, data):
        """docstring for load"""
        self.login = data['login']
        self.name = data['name']
        self.password = data['password']
        #. status
        self.nickname = data['nickname']
        self.xy = data['xy']
        self.map_name = data['map_name']
        self.skills = data['skills']
        self.spells = data['spells']
        self.race = data['race']
        self.role = data['role']
        self.job = data['job']
        self.prompt = data['prompt']
        #. combat status
        self.hp = data['hp']
        self.mp = data['mp']
        self.status = data['status']
        #. other
        #self.init_prev_location()

    def get_prompt(self, room=None):
        """docstring for get_prompt"""
        prompt = '\n(^w'
        hp, mhp = self.get_hp()
        mp, mmp = self.get_mp()
        prompt += "HP:%s/%s, MP:%s/%s, EXP:%s, COINS:%s" % (hp, mhp, mp, mmp, 0, 0)
        if self.is_admin():
            room = status.WORLD.locate_player_room(status.PLAYERS[self.name]) if room == None else room
            mobs = [mob.get_name() for mob in room.get_mobs()]
            prompt += "ID: %s, XY: %s MOBS: %s)\n> ^~" % (room.id_, str(room.xy), str(mobs))
        else:
            prompt += ")\n> ^~"
        return prompt

class CharacterLoader(YamlLoader):
    """docstring for CharacterLoader"""
    def __init__(self, data_dir):
        super(CharacterLoader, self).__init__(data_dir)
        self.data_dir = data_dir

    def get(self, name):
        """docstring for get"""
        data = self.load(name)
        if data:
            character = Character(data.get(name))
            character.load(data)
            return character
        return None

