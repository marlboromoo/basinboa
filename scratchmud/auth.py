#!/usr/bin/env python
"""
auth system
"""
import copy
import status
from message import broadcast

def login_queue(client):
    """docstring for login_queue"""
    status.UNLOGIN_CLIENTS[client] = {
        'login' : None,
        'username' : None,
        'username_process' : None,
        'password' : None,
        'password_process' : None,
        'retry' : 0,
    }

def character_was_login(character):
    """docstring for character_in_game"""
    if character.username in [character.username for character in status.CHARACTERS.values()]:
        return True
    return False

def find_origin_client_and_character(character):
    """docstring for find_origin_client"""
    for client, character_ in status.CHARACTERS.items():
        if character_.get_name() == character.get_name():
            return client, character_
    return None, None

def auth_client(client):
    """auth the client."""
    if client in status.UNLOGIN_CLIENTS:
        login_status = status.UNLOGIN_CLIENTS[client]
        status.CHARACTER_LOADER.load(login_status['username'])
        character = status.CHARACTER_LOADER.get(login_status['username'])
        #. check password correct
        if character and character.get_password() == login_status['password']:
            #. check current in game?
            if character_was_login(character):
                client.send('\nThis username was login, kick the user!\n')
                origin_client, origin_character = find_origin_client_and_character(character)
                character = copy.deepcopy(origin_character) #. copy the character object, because the origin character object wiil be drop
                origin_client.send("Somebody login from %s, see you again!\n" % (client.addrport()) )
                status.QUIT_CLIENTS.append(origin_client) #. origin character object drop here
            character.client = client
            status.CHARACTERS[client] = character
            status.UNLOGIN_CLIENTS.pop(client)
            broadcast('%s enter the world.\n' % status.CHARACTERS[client].get_name() )
            print ('** Client %s login success with username: %s.' % (client.addrport(), login_status['username']))
            return True
        else:
            print ('!! Client %s login fail with username: %s.' % (client.addrport(), login_status['username']) )
            return False
    return False

def login_get_username(client):
    """docstring for login_get_username"""
    login_status = status.UNLOGIN_CLIENTS[client]
    if not login_status['username']:
        if not login_status['username_process']:
            client.send("Username:")
            login_status['username_process'] = True
            return
        if login_status['username_process'] and client.cmd_ready:
            login_status['username'] = client.get_command()
            print ('** Client %s try to login with username: %s.' % (client.addrport(), login_status['username']) )
            return

def login_get_password(client):
    """docstring for login_get_password"""
    login_status = status.UNLOGIN_CLIENTS[client]
    if not login_status['password']:
        if login_status['username'] and not login_status['password_process']:
            client.password_mode_on()
            client.send("Password:")
            login_status['password_process'] = True
            return
        if login_status['username'] and login_status['password_process'] and client.cmd_ready:
            login_status['password'] = client.get_command()
            client.password_mode_off()
            client.send('\n')
            return

def login(client):
    """login the clietn."""
    #. get username
    login_status = status.UNLOGIN_CLIENTS[client]
    login_get_username(client)
    login_get_password(client)
    if login_status['username'] and login_status['password']:
        if auth_client(client):
            login_status['login'] = True
        else:
            login_status['login'] = False
            login_status['retry'] += 1
        #. disconnect client if retry too many
        if login_status['retry'] >= 3: 
            client.send("\nRetry too many times, bye!\n")
            return 
        #. final login
        if login_status['login']:
            client.send("\nWelcome !!! %s !!! \n"  % (status.CHARACTERS[client].get_name()))
            status.WORLD.locate_client_map(client).add_client(client)
        else:
            login_status['password'], login_status['password_process'] = None, None

