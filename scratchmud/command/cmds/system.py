#!/usr/bin/env python
"""
system commands.
"""
from scratchmud import status

def who(client, args):
    """docstring for who"""
    for character in status.CHARACTERS.values():
        client.send("%s\n" % repr(character))

def quit(client, args):
    """docstring for quit"""
    client.send('\nSee you next time ! \n')
    status.QUIT_CLIENTS.append(client)

def save(client, args):
    """docstring for save"""
    msg = 'okay.' if  status.CHARACTER_LOADER.dump(status.CHARACTERS[client]) else 'fail!'
    client.send('%s\n' % (msg))
