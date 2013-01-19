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
