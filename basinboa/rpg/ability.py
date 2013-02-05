#!/usr/bin/env python
"""
Ability system.
"""
import sys 
sys.path.append('../..')

from basinboa.rpg.dice import Dice
from basinboa.data.attr import set_attr, load, dump

NORMAL_DICE = Dice(3,6)
EPIC_DICE = Dice(4,6)
MODIFIER_BASE = (10, 11)

class Ability(object):
    """docstring for Ability"""
    def __init__(self):
        super(Ability, self).__init__()
        self.level = 1
        self.strength = None
        self.dexterity = None
        self.wisdom = None
        self.constitution = None
        self.intelligence = None
        self.charisma = None
        self.attrs = ['strength', 'dexterity', 'wisdom', 
                      'constitution', 'intelligence', 'charisma']

    def modifier(self, ability):
        """
        ability     modifier
        4-5         -3
        6-7         -2
        8-9         -1
        10-11       0
        12-13       +1
        14-15       +2
        16-17       +3
        18-19       +4
        20-21       +5
        """
        start, end = MODIFIER_BASE
        if ability >= start and ability <= end:
            return ability
        if ability < start:
            mod_start = start
            mod = 0
            while ability < mod_start:
                mod_start -= 2
                mod -= 1
            return mod
        if ability > end:
            mod_end = end
            mod = 0
            while ability > mod_end:
                mod_end += 2
                mod += 1
            return mod

    def level_bonus(self):
        """docstring for level_bonus"""
        return self.level/2

    def bonus(self, ability):
        """docstring for bonus"""
        return self.modifier(ability) + self.level_bonus()

    def generate(self, epic=False):
        """docstring for generate"""
        dice = NORMAL_DICE if not epic else EPIC_DICE
        for attr in self.attrs:
            set_attr(self, attr, dice.roll())

    def load(self, data):
        """docstring for load"""
        return load(self, data)

    def dump(self):
        """docstring for dump"""
        return dump(self)

    def apply_race_bonus(self, race):
        """docstring for apply_race_bonus"""
        for attr in self.attrs:
            attr_ = getattr(self, attr)
            bonus = getattr(race, "%s_bonus" % (attr))
            setattr(self, attr, attr_+bonus)

