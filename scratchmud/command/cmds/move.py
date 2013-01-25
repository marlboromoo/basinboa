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

@command
def follow(client, args):
    """
    follow the player.
    useage: follow <PLAYER_NAME>
            follow <YOUR_NAME> to cancle following player.
    """
    target_name = args[0] if len(args) > 0 else None
    room = status.WORLD.locate_client_room(client)
    return status.CHARACTERS[client].follow(room.get_character_by_name, target_name) \
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
    return status.CHARACTERS[client].follow(room.get_mob_by_name, target_name) \
            if target_name else client.send('Huh?\n')

