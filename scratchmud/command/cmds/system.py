#!/usr/bin/env python
"""
system commands.
"""
from scratchmud import status
from scratchmud.decorator import command

@command
def who(client, args):
    """
    list online players.
    useage: who
    """
    for character in status.CHARACTERS.values():
        client.send("%s\n" % repr(character))

@command
def quit(client, args):
    """
    exit the game.
    useage: quit
    """
    client.send('\nSee you next time ! \n')
    status.QUIT_CLIENTS.append(client)

@command
def save(client, args):
    """
    save your character data.
    useage: save
    """
    msg = 'okay.' if  status.CHARACTER_LOADER.dump(status.CHARACTERS[client]) else 'fail!'
    client.send('%s\n' % (msg))

@command
def cmds(client, args):
    """
    list available commands.
    useage: cmds
    """
    client.send('%s\n' % (str(status.COMMANDS.keys())))

@command
def man(client, args):
    """
    show the documents of command.
    useage: man <COMMAND>
    """
    cmd = args[0] if len(args) > 0 else None
    if cmd:
        doc = status.COMMANDS.get(cmd).func_doc if status.COMMANDS.has_key(cmd) else 'No such documents.'
        client.send('%s\n' % (str(doc)))
    else:
        client.send('useage: man <COMMAND>\n')
