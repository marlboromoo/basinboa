#!/usr/bin/env python
"""
message system
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





#def client_message_to_room(client, msg):
#    """send client message to room"""
#    room = status.WORLD.locate_client_room(client)
#    for client_ in room.get_clients():
#        if client_ != client and status.CHARACTERS.has_key(client_):
#            client_.send(msg)
#            
#
#def client_message_to_map(client, msg):
#    """sen client message to map"""
#    map_ = status.WORLD.locate_client_map(client)
#    for client_ in map_.get_clients():
#        if client_ != client and status.CHARACTERS.has_key(client_):
#            client_.send(msg)
#
#def character_message_to_room(character, msg):
#    """send character message to room"""
#    room = status.WORLD.locate_character_room(character)
#    for client in room.get_clients():
#        character_ = status.CHARACTERS[client] if status.CHARACTERS.has_key(client) else None
#        if character_ and character_ != character:
#            client.send(msg)
#
#def character_message_to_map(character, msg):
#    """sen client message to map"""
#    map_ = status.WORLD.locate_character_map(character)
#    for client in map_.get_clients():
#        character_ = status.CHARACTERS[client] if status.CHARACTERS.has_key(client) else None
#        if character_ and character_ != character:
#            client.send(msg)

