#!/usr/bin/env python
"""
commands !
"""

class Command(object):
    """docstring for Command"""
    def __init__(self):
        super(Command, self).__init__()
        
    @staticmethod
    def chat(client, clients, msg):
        """
        Echo whatever client types to everyone.
        """
        print '%s says, "%s"' % (client.soul.get_name(), msg)
    
        for guest in clients:
            if guest != client:
                guest.send('%s says, %s\n' % (client.soul.get_name(), msg))
            else:
                guest.send('You say, %s\n' % msg)
