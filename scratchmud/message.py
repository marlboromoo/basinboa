#!/usr/bin/env python
"""
message system
"""

import status

def broadcast(msg):
    """
    Send msg to every client.
    """
    for client in status.CLIENTS:
        if status.PLAYERS.has_key(client):
            client.send(msg)

def client_message_to_room(client, msg):
    """docstring for client_message_to_room"""
    room = status.WORLD.locate_client_room(client)
    for client_ in room.get_clients():
        if client_ != client and status.PLAYERS.has_key(client_):
            client_.send(msg)

def client_message_to_map(client, msg):
    """docstring for client_message_to_map"""
    map_ = status.WORLD.locate_client_map(client)
    for client_ in map_.get_clients():
        if client_ != client and status.PLAYERS.has_key(client_):
            client_.send(msg)
