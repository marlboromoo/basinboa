#!/usr/bin/env python
"""
system commands.
"""
from basinboa import status
from basinboa.decorator import command
from basinboa.date import mud_string_datetime

@command
def who(player, args):
    """
    list online players.
    useage: who
    """
    for player_ in status.PLAYERS.values():
        player.send("%s\n" % repr(player_.character))

@command
def quit(player, args):
    """
    exit the game.
    useage: quit
    """
    player.send('\nSee you next time ! \n')
    status.QUIT_CLIENTS.append(player)

@command
def save(player, args):
    """
    save your character data.
    useage: save
    """
    msg = 'okay.' if  status.CHARACTER_LOADER.dump(player.character) else 'fail!'
    player.send('%s\n' % (msg))

@command
def cmds(player, args):
    """
    list available commands.
    useage: cmds
    """
    player.send('%s\n' % (str(status.COMMANDS.keys())))

@command
def man(player, args):
    """
    show the documents of command.
    useage: man <COMMAND>
    """
    cmd = args[0] if len(args) > 0 else None
    if cmd:
        doc = status.COMMANDS.get(cmd).func_doc if status.COMMANDS.has_key(cmd) else 'No such documents.'
        player.send('%s\n' % (str(doc)))
    else:
        player.send('useage: man <COMMAND>\n')

@command
def datetime(player, args):
    """docstring for datetime"""
    player.send("%s\n" % mud_string_datetime())
