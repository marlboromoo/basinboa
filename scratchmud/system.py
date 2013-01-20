#!/usr/bin/env python
"""
system libs
"""
import status
from auth import login_queue, login
from command import Command as command
from message import broadcast

def on_connect(client):
    """
    Sample on_connect function.
    Handles new connections.
    """
    print "++ Opened connection to %s" % client.addrport()
    broadcast('Unkown try to enter the world from %s.\n' % client.addrport() )
    status.CLIENTS.append(client)
    client.send("Welcome to the strachmud, please login.\n")
    login_queue(client)

def on_disconnect(client):
    """
    Sample on_disconnect function.
    Handles lost connections.
    """
    print "-- Lost connection to %s" % client.addrport()
    #. save user data
    if status.PLAYERS.has_key(client):
        status.PLAYER_LOADER.save(status.PLAYERS[client])
    try:
        status.CLIENTS.remove(client)
        status.UNLOGIN_CLIENTS.pop(client)
        status.PLAYERS.pop(client)
    except Exception:
        pass
    broadcast('%s leaves the world.\n' % client.addrport() )


def kick_idle():
    """
    Looks for idle clients and disconnects them by setting active to False.
    """
    ## Who hasn't been typing?
    for client in status.CLIENTS:
        if client.idle() > status.IDLE_TIMEOUT:
            print('-- Kicking idle lobby client from %s' % client.addrport())
            client.active = False
            status.CLIENTS.remove(client)

def kick_quit():
    """docstring for kick_quit"""
    for client in status.QUIT_CLIENTS:
        client.active = False

def process_clients():
    """
    Check each client, if client.cmd_ready == True then there is a line of
    input available via client.get_command().
    """
    for client in status.CLIENTS:
        if not status.PLAYERS.has_key(client):
            #. disconnect after sending message to client
            if status.UNLOGIN_CLIENTS[client]['retry'] >= 3:
                disconnect(client)
            else:
                login(client)
        if client in status.PLAYERS and client.active and client.cmd_ready:
            process_command(client)

def process_command(client):
    """
    Process the client input.
    """
    inputs = client.get_command()

    cmd = inputs.lower()
    #. check if system command
    if cmd == 'shutdown':
        shutdown()
    #. other commands
    else:
        if len(cmd) > 0:
            command(client, inputs)

def disconnect(client):
    """disconnect the client."""
    client.active = False

def shutdown():
    """Shutdown the server."""
    status.SERVER_RUN = False

