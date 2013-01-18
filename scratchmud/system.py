#!/usr/bin/env python
"""
system libs
"""
import status
from player import Player
from command import Command as command


IDLE_TIMEOUT = 300

def inject_client(client):
    """docstring for inject_client"""
    client.login = None
    client.username = None
    client.username_process = None
    client.password = None
    client.password_process = None

def auth_client(client):
    """auth the client."""
    if client.username and client.password:
        #. TODO check process ..
        status.PLAYERS[client] = Player(client.username)
        broadcast('%s enter the world.\n' % status.PLAYERS[client].get_name() )
        return True

def login(client):
    """login the clietn."""
    #. get username
    if not client.username:
        if not client.username_process:
            client.send("Username:")
            client.username_process = True
            return
        if client.username_process and client.cmd_ready:
            client.username = client.get_command()
            return
    #. get password
    if not client.password:
        if client.username and not client.password_process:
            client.password_mode_on()
            client.send("Password:")
            client.password_process = True
            return
        if client.username and client.password_process and client.cmd_ready:
            client.password = client.get_command()
            client.password_mode_off()
            return
    #. auth, TODO: load player profile
    if client.username and client.password:
        client.login = True if auth_client(client) else False
        if client.login:
            client.send("\nWelcome !!! %s !!! \n"  % (status.PLAYERS[client].get_name()))
            status.WORLD.locate_client_map(client).add_client(client)
        else:
            client.password, client.password_process = None, None
    
def on_connect(client):
    """
    Sample on_connect function.
    Handles new connections.
    """
    print "++ Opened connection to %s" % client.addrport()
    broadcast('Unkown try to enter the world from %s.\n' % client.addrport() )
    status.CLIENTS.append(client)
    client.send("Welcome to the strachmud, please login.\n")
    inject_client(client)

def on_disconnect(client):
    """
    Sample on_disconnect function.
    Handles lost connections.
    """
    print "-- Lost connection to %s" % client.addrport()
    status.CLIENTS.remove(client)
    broadcast('%s leaves the world.\n' % client.addrport() )


def kick_idle():
    """
    Looks for idle clients and disconnects them by setting active to False.
    """
    ## Who hasn't been typing?
    for client in status.CLIENTS:
        if client.idle() > IDLE_TIMEOUT:
            print('-- Kicking idle lobby client from %s' % client.addrport())
            client.active = False


def process_clients():
    """
    Check each client, if client.cmd_ready == True then there is a line of
    input available via client.get_command().
    """
    for client in status.CLIENTS:
        if not client.login:
            login(client)
        if client.active and client.cmd_ready:
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

def broadcast(msg):
    """
    Send msg to every client.
    """
    for client in status.CLIENTS:
        if client.login:
            client.send(msg)

def disconnect(client):
    """disconnect the client."""
    client.active = False

def shutdown():
    """Shutdown the server."""
    status.SERVER_RUN = False

