#!/usr/bin/env python
"""
player profile
"""

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
        self.role = None
        self.job = None
        self.prompt = None
        #. combat status
        self.hp = 100
        self.mp = 100
        self.status = None

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

        
