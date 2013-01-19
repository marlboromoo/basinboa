#!/usr/bin/env python
"""
event in the world.
"""
import status
import time

class Tick(object):
    """tick base on second"""
    def __init__(self, second):
        super(Tick, self).__init__()
        self.second = second
        self.start_time = int(time.time())
        self.previous_time = None
        self.time = None

    def can_fire(self):
        """can we fire ?"""
        if not self.previous_time:
            self.previous_time = int(time.time())
        self.time = int(time.time())
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
    e = Tick(second)
    e.fire(echo, 'hello tick %s' % str(second))
        
