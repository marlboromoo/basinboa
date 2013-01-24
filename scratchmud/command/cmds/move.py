#!/usr/bin/env python
"""
move commands.
"""
from scratchmud import status

def west(self, args):
    """docstring for west"""
    status.CHARACTERS[self.client].go_west()

def east(self, args):
    """docstring for east"""
    status.CHARACTERS[self.client].go_east()

def north(self, args):
    """docstring for north"""
    status.CHARACTERS[self.client].go_north()

def south(self, args):
    """docstring for south"""
    status.CHARACTERS[self.client].go_south()

def up(self, args):
    """docstring for up"""
    status.CHARACTERS[self.client].go_up()

def down(self, args):
    """docstring for down"""
    status.CHARACTERS[self.client].go_down()

def follow(self, args):
    """docstring for follow"""
    target_name = args[0] if len(args) > 0 else None
    room = status.WORLD.locate_client_room(self.client)
    return status.CHARACTERS[self.client].follow(room.get_character_by_name, target_name) \
            if target_name else self.client.send('Huh?\n')

def track(self, args):
    """docstring for track"""
    target_name = args[0] if len(args) > 0 else None
    room = status.WORLD.locate_client_room(self.client)
    return status.CHARACTERS[self.client].follow(room.get_mob_by_name, target_name) \
            if target_name else self.client.send('Huh?\n')
