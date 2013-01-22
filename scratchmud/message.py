#!/usr/bin/env python
"""
message system
"""

import status

def broadcast(msg):
    """
    Send msg to every client.
    """
    for client in status.PLAYERS:
        client.send(msg)

def client_message_to_room(client, msg):
    """send client message to room"""
    room = status.WORLD.locate_client_room(client)
    for client_ in room.get_clients():
        if client_ != client and status.PLAYERS.has_key(client_):
            client_.send(msg)

def client_message_to_map(client, msg):
    """sen client message to map"""
    map_ = status.WORLD.locate_client_map(client)
    for client_ in map_.get_clients():
        if client_ != client and status.PLAYERS.has_key(client_):
            client_.send(msg)

def player_message_to_room(player, msg):
    """send player message to room"""
    room = status.WORLD.locate_player_room(player)
    for client in room.get_clients():
        player_ = status.PLAYERS[client] if status.PLAYERS.has_key(client) else None
        if player_ and player_ != player:
            client.send(msg)

def player_message_to_map(player, msg):
    """sen client message to map"""
    map_ = status.WORLD.locate_player_map(player)
    for client in map_.get_clients():
        player_ = status.PLAYERS[client] if status.PLAYERS.has_key(client) else None
        if player_ and player_ != player:
            client_.send(msg)

def mob_message_to_room(mob, msg):
    """send mob message to room"""
    room = status.WORLD.locate_mob_room(mob)
    for client_ in room.get_clients():
        if status.PLAYERS.has_key(client_):
            client_.send(msg)

def mob_message_to_map(mob, msg):
    """send mob message to map"""
    map_ = status.WORLD.locate_mob_map(mob)
    for client_ in map_.get_clients():
        if status.PLAYERS.has_key(client_):
            client_.send(msg)

