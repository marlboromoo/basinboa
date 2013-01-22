#!/usr/bin/env python
"""
event in the world.
"""
import time

class Cycle(object):
    """tick base on second"""
    def __init__(self, second):
        super(Cycle, self).__init__()
        self.second = second
        self.previous_time = None
        self.time = None

    def can_fire(self):
        """can we fire ?"""
        if not self.previous_time:
            self.previous_time = time.time()
        self.time = time.time()
        if self.time - self.previous_time >= self.second:
            self.time, self.previous_time = None, None
            return True
        return False

    def fire(self, function, *args, **kwargs):
        """shoot !"""
        #print args, #kwargs
        if self.can_fire():
            function(*args, **kwargs)

def echo(msg):
    """docstring for echo"""
    print msg

if __name__ == '__main__':
    second = 1
    e = Cycle(second)
    e.fire(echo, 'hello tick %s' % str(second))
        
