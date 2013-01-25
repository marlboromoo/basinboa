#!/usr/bin/env python
"""
move commands.
"""
from scratchmud import status

def west(client, args):
    """docstring for west"""
    status.CHARACTERS[client].go_west()

def east(client, args):
    """docstring for east"""
    status.CHARACTERS[client].go_east()

def north(client, args):
    """docstring for north"""
    status.CHARACTERS[client].go_north()

def south(client, args):
    """docstring for south"""
    status.CHARACTERS[client].go_south()

def up(client, args):
    """docstring for up"""
    status.CHARACTERS[client].go_up()

def down(client, args):
    """docstring for down"""
    status.CHARACTERS[client].go_down()

def follow(client, args):
    """docstring for follow"""
    target_name = args[0] if len(args) > 0 else None
    room = status.WORLD.locate_client_room(client)
    return status.CHARACTERS[client].follow(room.get_character_by_name, target_name) \
            if target_name else client.send('Huh?\n')

def track(client, args):
    """docstring for track"""
    target_name = args[0] if len(args) > 0 else None
    room = status.WORLD.locate_client_room(client)
    return status.CHARACTERS[client].follow(room.get_mob_by_name, target_name) \
            if target_name else client.send('Huh?\n')
