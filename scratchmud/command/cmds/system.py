#!/usr/bin/env python
"""
system commands.
"""
from scratchmud import status

def who(self, args):
    """docstring for who"""
    for character in status.CHARACTERS.values():
        self.client.send("%s\n" % repr(character))

def quit(self, args):
    """docstring for quit"""
    self.client.send('\nSee you next time ! \n')
    status.QUIT_CLIENTS.append(self.client)

def save(self, args):
    """docstring for save"""
    msg = 'okay.' if  status.CHARACTER_LOADER.dump(status.CHARACTERS[self.client]) else 'fail!'
    self.client.send('%s\n' % (msg))
