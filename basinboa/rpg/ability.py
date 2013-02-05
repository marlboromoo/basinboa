#!/usr/bin/env python
"""
Ability system.
"""
import sys 
sys.path.append('../..')

from basinboa.rpg.dice import Dice
from basinboa.data.attr import set_attr, get_attr, load, dump

NORMAL_DICE = Dice(3,6)
EPIC_DICE = Dice(4,6)

class Ability(object):
    """docstring for Ability"""
    def __init__(self):
        super(Ability, self).__init__()
        self.str_ = None
        self.dex = None
        self.wis = None
        self.con = None
        self.int_ = None
        self.cha = None
        self.attrs = ['str_', 'dex', 'wis', 'con', 'int_', 'cha']
        self.generate()

    def generate(self, epic=False):
        """docstring for generate"""
        dice = NORMAL_DICE if not epic else EPIC_DICE
        for attr in self.attrs:
            set_attr(self, attr, dice.roll())

if __name__ == '__main__':
    ability = Ability()
    print  dump(ability)



