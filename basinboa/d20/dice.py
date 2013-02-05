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
    def __init__(self, number, side):
        super(Dice, self).__init__()
        self.number = number
        self.side = side

    def _side(self, side):
        """docstring for _side"""
        return range(1, side+1)

    def roll(self, offset=0, debug=False):
        """docstring for roll"""
        i = 1
        point = 0
        while i <= self.number:
            point_ = random.choice(self._side(self.side))
            point += point_
            if debug: print 'roll - %s !' % (point_)
            i += 1
        if debug: print 'offset: %s' % (offset)
        return point + offset
        
if __name__ == '__main__':
    _3d8 = Dice(3,8)
    print _3d8.roll(0)
        
