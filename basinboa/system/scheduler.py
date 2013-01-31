#!/usr/bin/env python
"""
scheduler in the world.
reference: http://code.google.com/p/bogboa/source/browse/trunk/mudlib/sys/scheduler.py
"""
import time
import random

class Cycle(object):
    """ add a event to scheduler periodical """
    def __init__(self, delay, func, args=()):
        super(Cycle, self).__init__()
        self.delay = delay
        self.func = func
        self.args = args
        self.previous_time = None
        self.time = None
        self._add()

    def __repr__(self):
        return "Cycle: %s, args:%s, delay:%s, fire_time:%s" % (
            self.func, self.args, self.delay, self.time)

    def _add(self):
        """docstring for _add"""
        SCHEDULER.add(self.delay, self.fire, self.args)

    #def _can_add(self):
    #    """docstring for _can_add"""
    #    if not self.previous_time:
    #        self.previous_time = time.time()
    #    self.time = time.time()
    #    if self.time - self.previous_time >= self.delay:
    #        self.time, self.previous_time = None, None
    #        return True
    #    return False

    def fire(self, args=()):
        """docstring for fire"""
        self.func(self.args) if len(self.args) > 0 else self.func()
        #if self._can_add:
        #    self._add()
        self._add()
        
class Event(object):
    """function wrapper"""
    def __init__(self, delay, func, args=()):
        super(Event, self).__init__()
        self.delay = delay
        self.func = func
        self.args = args
        self.time = time.time() + delay

    def __repr__(self):
        return "Event: %s, args:%s, delay:%s, fire_time:%s" % (
            self.func, self.args, self.delay, self.time
        )
        
class Scheduler(object):
    """fire event by order"""
    def __init__(self):
        super(Scheduler, self).__init__()
        self.time = time.time()
        self.event_list = []

    def add(self, delay, func, args=()):
        """docstring for add"""
        self.event_list.append(Event(delay, func, args))

    def get_events(self):
        """docstring for get_events"""
        return self.event_list

    def tick(self):
        """docstring for tick"""
        #. update time
        self.time = time.time()
        #. find event to fire
        for event in self.event_list:
            if event.time <= self.time:
                self.event_list.remove(event)
                event.func(event.args) if len(event.args) > 0 else event.func()
            else:
                #. wait to next tick
                pass

#------------------------------------------------------------------------------
#       Shared Instance
#------------------------------------------------------------------------------

SCHEDULER = Scheduler()

#------------------------------------------------------------------------------
#       Debug
#------------------------------------------------------------------------------

if __name__ == '__main__':
    def echo(msg):
        print msg

    def ping():
        print 'pong!'

    Cycle(2, echo, 'cycle!')
    Cycle(2, ping)
    SCHEDULER.add(1, ping)
    SCHEDULER.add(1, echo, 'echo!')
    #SCHEDULER.add(3, echo, 'foo')
    while True:
        time.sleep(1)
        print "%s %s" % (SCHEDULER.time, SCHEDULER.get_events())
        SCHEDULER.tick()
        if random.choice([True, False]):
            SCHEDULER.add(random.choice([1,2,3]), echo, random.choice(['foo', 'bar', 'spam']))


