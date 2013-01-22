#!/usr/bin/env python
"""
player player
"""
import yaml
import os
import status
from puppet import Puppet
from message import player_message_to_room 
from encode import texts_encoder

ROLE_ADMIN = 'admin'
ROLE_USER = 'user'

class Player(Puppet):
    """docstring for Player"""
    def __init__(self, username=None):
        super(Player, self).__init__()
        self.client = None
        self.login = None
        self.username = username
        self.password = None
        #. status
        self.nickname = None
        self.xy = (1, 0)
        self.map_name = 'void'
        self.skills = None
        self.spells = None
        self.race = None
        self.role = ROLE_USER
        self.job = None
        self.prompt = None

    def __repr__(self):
        return "User:%s, role:%s, xy:%s, map:%s" % (
            str(self.username), str(self.role), str(self.xy), str(self.map_name))

    def set_name(self, name):
        """docstring for set_name"""
        self.username = name

    def get_name(self):
        """docstring for get_name"""
        return self.username

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

    def dump(self):
        """docstring for dump"""
        return {
            'login' : self.login,
            'username' : self.username,
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
        self.username = data['username']
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

    def go(self, symbol, function, message):
        """docstring for go"""
        room = status.WORLD.locate_player_room(self)
        x, y = self.xy
        if symbol in room.exits:
            dst_xy = function(x, y)
            if dst_xy in room.paths:
                #. message to all the players in room
                player_message_to_room(self, '%s go to %s!\n' % (self.username, message))
                #. move player to room
                self.xy = dst_xy
                #. remove client from source room
                room.remove_client_by_player(self)
                #. add mob to target room
                status.WORLD.locate_player_room(self).add_client_by_player(self)
                #. send message to all the players in target room
                player_message_to_room(self, '%s come to here!\n' % (self.username))
        else:
            self.client.send('Huh?\n')

    def look(self, target=None):
        """docstring for look"""
        room = status.WORLD.locate_player_room(self)
        self.client.send('%s\n' % (texts_encoder(room.texts)))
        mobs = [mob.mobname for mob in room.mobs]
        self.client.send('exits: %s, id: %s, xy: %s mobs: %s\n' % (room.exits, room.id_, str(room.xy), str(mobs)))
        #. other players
        for client_ in room.get_clients():
            if client_ != self.client:
                player_ = status.PLAYERS[client_]
                self.client.send(texts_encoder("%s(%s) in here.\n" % (player_.nickname, player_.username)))
        #. mobs
        for mob in room.get_mobs():
            self.client.send(texts_encoder("%s(%s) in here.\n" % (mob.nickname, mob.mobname)))

class PlayerLoader(object):
    """docstring for PlayerLoader"""
    def __init__(self, data_dir):
        super(PlayerLoader, self).__init__()
        self.data_dir = data_dir
        self.players = {}

    def load(self, username):
        """docstring for load"""
        path = os.path.join(self.data_dir, "%s.yaml" % username)
        #print path
        try:
            with open(path, 'r') as f:
                data = yaml.load(f, Loader=yaml.Loader)
                player = Player(data['username'])
                player.load(data)
                self.players[username] = player
        except Exception:
            pass
            #print "Error! no such player !"

    def save_from_object(self, player):
        """docstring for save"""
        path = os.path.join(self.data_dir, "%s.yaml" % player.get_name())
        try:
            with open(path, 'w') as f:
                f.write(yaml.dump(player.dump()))
                return True
        except Exception:
            return False

    def save(self, player):
        """docstring for save"""
        return self.save_from_object(player)

    def get(self, username):
        """docstring for get"""
        return self.players.pop(username) if self.players.has_key(username) else None

if __name__ == '__main__':
    username = 'admin'
    #player = Player(username)
    pf = PlayerLoader('../data/player')
    #pf.save(username)
    pf.load(username)
    player = pf.get(username)
    print player
    player.set_role(ROLE_ADMIN)
    print player
    print player.get_password()

        

        
