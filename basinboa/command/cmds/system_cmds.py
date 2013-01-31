#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
system commands.
"""
from basinboa import status
from basinboa.system.decorator import command
from basinboa.system.scheduler import SCHEDULER
from basinboa.system.encode import texts_encoder
from basinboa.universe.date import mud_string_datetime

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
    SCHEDULER.add(.2, player.deactivate)

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


@command
def test(player, args):
    """docstring for encode_test"""
    player.send_cc_encode("%s" % player.character.desc)
