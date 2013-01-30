#!/usr/bin/env python
"""
broadcast message
"""

from basinboa import status

def broadcast(msg):
    """
    Send msg to every client.
    """
    for player_ in status.PLAYERS.values():
        player_.send(msg)

def message_to_room(room, msg):
    """docstring for message_to_room"""
    for player in room.get_players():
        player.send(msg)

def message_to_map(map_, msg):
    """docstring for message_to_room"""
    for player in map_.get_players():
        player.send(msg)

def player_message_to_room(player, msg):
    """docstring for player_message_to_room"""
    room = status.WORLD.locate_player_room(player)
    for player_ in room.get_players():
        if player_ != player: 
            player_.send(msg)

def player_message_to_map(player, msg):
    """docstring for player_message_to_map"""
    map_ = status.WORLD.locate_player_map(player)
    for player_ in map_.get_players():
        if player_ != player:
            player_.send(msg)

def mob_message_to_room(mob, msg):
    """send mob message to room"""
    room = status.WORLD.locate_mob_room(mob)
    for player_ in room.get_players():
        player_.send(msg)

def mob_message_to_map(mob, msg):
    """send mob message to map"""
    map_ = status.WORLD.locate_mob_map(mob)
    for player_ in map_.get_players():
        player_.send(msg)

def invalid_args(player):
    """docstring for invalid_args"""
    player.send("Invalid args !\n")

