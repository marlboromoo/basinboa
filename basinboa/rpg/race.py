#!/usr/bin/env python
"""
Race system
"""
import sys 
sys.path.append('../..')

from basinboa.data.attr import load, dump

class Race(object):
    """docstring for Race"""
    def __init__(self):
        super(Race, self).__init__()
        self.style = None
        self.strength_bonus = 1
        self.dexterity_bonus = 1
        self.wisdom_bonus = 0 
        self.constitution_bonus = 0
        self.intelligence_bonus = 0
        self.charisma_bonus = 0
        self.attrs = ['strength_bonus', 'dexterity_bonus', 'wisdom_bonus', 
                      'constitution_bonus', 'intelligence_bonus', 'charisma_bonus']

    def load(self, data):
        """docstring for load"""
        return load(self, data)

    def dump(self):
        """docstring for dump"""
        return dump(self)
