#!/usr/bin/env python
"""
Level system
"""
import random

EXP_BASE = 10
EXP_STEP = 15

class Level(object):
    """docstring for Level"""
    def __init__(self):
        super(Level, self).__init__()
        self.exp = 0

    def increase(self):
        """docstring for increase"""
        self.level += 1

    def get(self):
        """docstring for get"""
        level = 1
        while self.exp >= self.require_exp(level):
            level += 1
        return level - 1 if level > 1 else 1

    def set(self, level):
        """docstring for set"""
        self.exp = self.require_exp(level)

    def increase_exp(self, value):
        """docstring for fname"""
        self.exp += value

    def decrease_exp(self, value):
        """docstring for decrease_exp"""
        self.exp -= value

    def require_exp(self, level):
        """
        level   experience points
        2       10
        3       40
        4       85
        5       145
        6       220
        7       310
        8       415
        9       535
        10      670
        11      820
        12      985
        13      1165
        14      1360
        15      1570
        16      1795
        17      2035
        18      2290
        19      2560
        20      2845
        """
        if level == 1:
            return 0
        else:
            exp = EXP_BASE
            i = 2 #. because level 1 don't need exp
            while i < level:
                exp += EXP_STEP * i
                i += 1
            return exp

if __name__ == '__main__':
    level = Level()
    i = 1
    while i <= 20:
        print "%s: %s" % (i, level.require_exp(i))
        i += 1
    level.increase_exp(random.randint(1, 2845))
    print "exp:%s = level:%s" % (level.exp, level.get())

