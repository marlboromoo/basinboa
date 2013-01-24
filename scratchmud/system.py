#!/usr/bin/env python
"""
system libs
"""
import status
from scratchmud.auth import login_queue, login
from scratchmud.command import Command as command
from scratchmud.message import broadcast


def clean_status(client):
    """remove client from status"""
    status.CLIENTS.remove(client)  if client in status.CLIENTS else None
    status.UNLOGIN_CLIENTS.pop(client) if status.UNLOGIN_CLIENTS.has_key(client) else None
    status.QUIT_CLIENTS.remove(client) if client in status.QUIT_CLIENTS else None

def on_connect(client):
    """
    Sample on_connect function.
    Handles new connections.
    """
    print "++ Opened connection to %s" % client.addrport()
    broadcast('Unkown try to enter the world from %s.\n' % client.addrport() )
    status.CLIENTS.append(client)
    client.send_cc("^R^!%s^~\n" % (status.ASCII_ART))
    client.send("Welcome to the strachmud, please login.\n")
    login_queue(client)

def on_disconnect(client):
    """
    Sample on_disconnect function.
    Handles lost connections.
    """
    print "-- Lost connection to %s" % client.addrport()
    #. save user data
    if status.CHARACTERS.has_key(client):
        status.CHARACTER_LOADER.dump(status.CHARACTERS[client])
        broadcast('%s leaves the world.\n' % status.CHARACTERS[client].get_name())
        clean_status(client)

def kick_idle():
    """
    Looks for idle clients and disconnects them by setting active to False.
    """
    #. TODO: clean reconnecnt sessions 
    for client in status.CLIENTS:
        if client.idle() > status.IDLE_TIMEOUT:
            print('-- Kicking idle lobby client from %s' % client.addrport())
            client.active = False
            clean_status(client)

def kick_quit():
    """docstring for kick_quit"""
    for client in status.QUIT_CLIENTS:
        clean_status(client)
        client.active = False

def process_clients():
    """
    Check each client, if client.cmd_ready == True then there is a line of
    input available via client.get_command().
    """
    for client in status.CHARACTERS.keys():
        if client.active and client.cmd_ready:
            process_command(client)

def login_clients():
    """docstring for login_clients"""
    for client in status.CLIENTS:
        if client in status.UNLOGIN_CLIENTS:
            if status.UNLOGIN_CLIENTS[client]['retry'] >= 3:
                status.UNLOGIN_CLIENTS.pop(client) if status.UNLOGIN_CLIENTS.has_key(client) else None
                disconnect(client)
            else:
                login(client)


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

