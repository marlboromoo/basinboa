#!/usr/bin/env python
"""
dice system.
"""

import random

DICE4 = 4
DICE6 = 6
DICE8 = 8
DICE10 = 10
DICE12 = 12
DICE20 = 20

class Dice(object):
    """docstring for Dice"""
    def __init__(self):
        super(Dice, self).__init__()

    def _side(self, side):
        """docstring for _side"""
        return range(1, side+1)

    def roll(self, number=1, side=20, offset=0):
        """docstring for roll"""
        i = 1
        point = 0
        while i <= number:
            point_ = random.choice(self._side(side))
            point += point_
            print 'roll - %s !' % (point_)
            i += 1
        print 'offset: %s' % (offset)
        return point + offset
        
if __name__ == '__main__':
    dice = Dice()
    print dice.roll(3, 8, -2)
        
