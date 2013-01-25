#!/usr/bin/env python
"""
move commands.
"""
from scratchmud import status
from scratchmud.decorator import command

@command
def west(client, args):
    """
    go to west.
    useage: west
    alias: w
    """
    status.CHARACTERS[client].go_west()

@command
def east(client, args):
    """
    go to east.
    useage: east
    alias: e
    """
    status.CHARACTERS[client].go_east()

@command
def north(client, args):
    """
    go to north.
    useage: north
    alias: n
    """
    status.CHARACTERS[client].go_north()

@command
def south(client, args):
    """
    go to south.
    useage: sourth.
    alias: s
    """
    status.CHARACTERS[client].go_south()

@command
def up(client, args):
    """
    go to up.
    useage: up
    alias: u
    """
    status.CHARACTERS[client].go_up()

@command
def down(client, args):
    """
    go to down.
    useage: down
    alias: d
    """
    status.CHARACTERS[client].go_down()

def __follow(client, function, name):
    """docstring for _follow"""
    character = status.CHARACTERS.get(client)
    target = function(name)
    if target:
        if target in character.get_followers():
            character.client.send("You can't ! %s already follow you.\n." % (target.name))
            return
        target.add_follower(character)
        character.start_follow(target)
        name = target.name if target != character else 'yourself'
        character.client.send("You start to follow %s!\n" % (name))
        if target.is_player() and target != character:
            target.client.send("%s start to follow you!" % (character.get_name()))
    else:
        character.client.send("No such target !\n")

@command
def follow(client, args):
    """
    follow the player.
    useage: follow <PLAYER_NAME>
            follow <YOUR_NAME> to cancle following player.
    """
    target_name = args[0] if len(args) > 0 else None
    room = status.WORLD.locate_client_room(client)
    return __follow(client, room.get_character_by_name, target_name) \
            if target_name else client.send('Huh?\n')

@command
def track(client, args):
    """
    follow the mob.
    useage: follow <MOB_NAME>
            follow <YOUR_NAME> to cancle following mob.
    """
    target_name = args[0] if len(args) > 0 else None
    room = status.WORLD.locate_client_room(client)
    return __follow(client, room.get_mob_by_name, target_name) \
            if target_name else client.send('Huh?\n')

