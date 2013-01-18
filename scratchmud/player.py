#!/usr/bin/env python
"""
player profile
"""
import yaml
import os

ROLE_ADMIN = 'admin'
ROLE_USER = 'user'

class Profile(object):
    """docstring for Profile"""
    def __init__(self, username):
        super(Profile, self).__init__()
        self.logn = None
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
        #. combat status
        self.hp = 100
        self.mp = 100
        self.status = None

    def __repr__(self):
        return "User:%s, role:%s, xy:%s, map:%s" % (
            str(self.username), str(self.role), str(self.xy), str(self.map_name))

    def set_name(self, name):
        """docstring for set_name"""
        self.username = name

    def get_name(self):
        """docstring for get_name"""
        return self.username

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

    def package_attributes(self):
        """docstring for package_attributes"""
        return {
            'login' : self.logn,
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

    def unpackage_attributes(self, data):
        """docstring for unpackage_attributes"""
        self.logn = data['login']
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

class ProfileLoader(object):
    """docstring for ProfileLoader"""
    def __init__(self, profile_dir):
        super(ProfileLoader, self).__init__()
        self.profile_dir = profile_dir
        self.profiles = {}

    def load(self, username):
        """docstring for load"""
        path = os.path.join(self.profile_dir, "%s.yaml" % username)
        print path
        try:
            with open(path, 'r') as f:
                data = yaml.load(f, Loader=yaml.Loader)
                profile = Profile(data['username'])
                self.profiles[username] = profile
        except Exception:
            print "Error! no such profile !"

    def save(self, profile):
        """docstring for save"""
        path = os.path.join(self.profile_dir, "%s.yaml" % profile.username)
        with open(path, 'w') as f:
            f.write(yaml.dump(profile.package_attributes()))

    def get(self, username):
        """docstring for get"""
        return self.profiles[username] if self.profiles.has_key(username) else None


if __name__ == '__main__':
    username = 'admin'
    profile = Profile(username)
    pf = ProfileLoader('../data/player')
    pf.save(profile)
    pf.load(username)
    profile = pf.get(username)
    print profile
    profile.set_role(ROLE_ADMIN)
    print profile

        

        
