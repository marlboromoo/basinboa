#!/usr/bin/env python
"""
character character
"""
#import yaml
#import os
import status
from scratchmud.loader import YamlLoader
from scratchmud.puppet import Puppet
from scratchmud.message import character_message_to_room 
#from scratchmud.encode import texts_encoder
from scratchmud.world import exit_name
from scratchmud.command.cmds.inspect import look

ROLE_ADMIN = 'admin'
ROLE_USER = 'user'

class Character(Puppet):
    """docstring for Character"""
    def __init__(self, name=None):
        super(Character, self).__init__()
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
        set.password = password

    def get_password(self):
        """docstring for get_password"""
        return self.password

    def set_location(self, xy, map_name=None):
        """docstring for set_location"""
        map_name = map_name if map_name else self.map_name
        self.xy = xy
        self.map_name = map_name

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

    def goto(self, xy, map_, message=None, autolook=True):
        """docstring for goto"""
        try:
            map_ = status.WORLD.get_map(map_)
            room =  map_.get_room(xy)
        except Exception:
            map_, room = None, None
        if map_ and room:
            src_map = status.WORLD.locate_client_map(self.client)
            src_room = status.WORLD.locate_client_room(self.client)
            #. send message notice all characters in the room
            if message:
                character_message_to_room(self, "%s go to %s.\n" % (self.get_name(), message))
            else:
                character_message_to_room(self, "%s leave here.\n" % (self.get_name()) )
            #. remove character in old place
            src_map.remove_client(self.client)
            src_room.remove_client(self.client)
            #. move character to destation
            self.set_location(xy, map_.get_name())
            map_.add_client(self.client)
            #. send message 
            character_message_to_room(self, '%s come to here!\n' % (self.get_name()))
            if autolook:
                return look(self.client, None)
        else:
            self.client.send("You can't!\n")

    def go(self, symbol, function, message):
        """docstring for go"""
        room = status.WORLD.locate_character_room(self)
        x, y = self.xy
        #. check n,s,w,e
        if symbol in room.exits:
            dst_xy = function(x, y)
            if dst_xy in room.paths:
                #. message to all the characters in room
                character_message_to_room(self, '%s go to %s!\n' % (self.name, message))
                #. move character to room
                self.xy = dst_xy
                #. remove character from source room
                room.remove_client_by_character(self)
                #. add character to target room
                status.WORLD.locate_character_room(self).add_client_by_character(self)
                #. send message to all the characters in target room
                character_message_to_room(self, '%s come to here!\n' % (self.name))
        #. check link
        elif room.has_link(symbol):
            link = room.get_link(symbol)
            self.goto(link['xy'], link['map'], exit_name(symbol), autolook=False)
        else:
            self.client.send('Huh?\n')

    def get_prompt(self, room=None):
        """docstring for get_prompt"""
        prompt = ''
        room = status.WORLD.locate_character_room(self) if room == None else room
        mobs = [mob.get_name() for mob in room.get_mobs()]
        prompt += "hp:%s/mp:%s, exits: %s" % (str(self.get_hp()), str(self.get_mp()), room.get_exits())
        if self.is_admin():
            prompt += "id: %s, xy: %s mobs: %s\n" % (room.id_, str(room.xy), str(mobs))
        else:
            prompt += "\n"
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

