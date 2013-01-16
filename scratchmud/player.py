#!/usr/bin/env python
"""
player profile
"""

class Soul(object):
    """docstring for Soul"""
    def __init__(self, username):
        super(Soul, self).__init__()
        self.logn = None
        self.username = username
        self.password = None
        #. status
        self.nickname = None
        self.xy = (1, 0)
        self.map_ = 'void'
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
        
