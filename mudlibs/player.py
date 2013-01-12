#!/usr/bin/env python
"""
player profile
"""

class Soul(object):
    """docstring for Soul"""
    def __init__(self, arg):
        super(Soul, self).__init__()
        self.NAME = arg
        self.logn = None
        self.login_name = None
        self.login_password = None

    def set_name(self, name):
        """docstring for set_name"""
        self.NAME = name

    def get_name(self):
        """docstring for get_name"""
        return self.NAME
        
