#!/usr/bin/env python
"""
system libs
"""

from basinboa import status
from basinboa.command import process_inputs
from basinboa.message import broadcast
from basinboa.loader import YamlLoader
from basinboa.user import Guest

def clean_status(client):
    """remove client from status"""
    player = status._PLAYERS[client]
    status.WORLD.remove_player(player)
    #. TODO: use del() to purge reference
    status.LOBBY.pop(client) if status.LOBBY.has_key(client) else None
    status._PLAYERS.pop(client) if status._PLAYERS.has_key(client) else None
    status.PLAYERS.pop(player.name) if status.PLAYERS.has_key(player.name) else None
    status.QUIT_CLIENTS.remove(client) if client in status.QUIT_CLIENTS else None

def on_connect(client):
    """
    Sample on_connect function.
    Handles new connections.
    """
    client.request_naws() #. get Window Size: client.columns, client.rows 
    print "++ Opened connection to %s" % client.addrport()
    broadcast('Unkown try to enter the world from %s.\n' % client.addrport() )
    client.send_cc("^R^!%s^~\n" % (status.ASCII_ART))
    client.send("Welcome to the strachmud, please login.\n")
    status.LOBBY[client] = Guest(client)

def on_disconnect(client):
    """
    Sample on_disconnect function.
    Handles lost connections.
    """
    print "-- Lost connection to %s" % client.addrport()
    #. save user data
    if status._PLAYERS.has_key(client):
        player = status._PLAYERS[client]
        status.CHARACTER_LOADER.dump(player.character)
        broadcast('%s leaves the world.\n' % player.character.get_name())
    clean_status(client)

def kick_idle():
    """
    Looks for idle clients and disconnects them by setting active to False.
    """
    #. TODO: clean reconnecnt sessions 
    for player in status.PLAYERS.values():
        if player.idle() > status.IDLE_TIMEOUT:
            print('-- Kicking idle lobby client from %s' % player.addrport())
            disconnect(player.client)

def kick_quit():
    """docstring for kick_quit"""
    for client in status.QUIT_CLIENTS:
        disconnect(client)
        status.QUIT_CLIENTS.remove(client)

def process_players():
    """docstring for process_players"""
    for player in status.PLAYERS.values():
        if player.client.active and player.client.cmd_ready:
            process_inputs(player)

def process_lobby():
    """docstring for process_lobby"""
    # TODO: write code...
    for client, guest in status.LOBBY.items():
        guest.login()

def disconnect(client):
    """disconnect the client."""
    client.deactivate()

class SettingsLoader(YamlLoader):
    """docstring for SettingsLoader"""
    SERVER_CONFIG = 'server'

    def __init__(self, data_dir):
        super(SettingsLoader, self).__init__(data_dir)
        
    def get_server_config(self):
        """docstring for get"""
        data = self.load(self.SERVER_CONFIG)
        if data:
            return data
        return None

