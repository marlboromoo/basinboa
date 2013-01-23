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
        'name' : None,
        'name_process' : None,
        'password' : None,
        'password_process' : None,
        'retry' : 0,
    }

def character_was_login(character):
    """docstring for character_in_game"""
    if character.name in [character.name for character in status.CHARACTERS.values()]:
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
        status.CHARACTER_LOADER.load(login_status['name'])
        character = status.CHARACTER_LOADER.get(login_status['name'])
        #. check password correct
        if character and character.get_password() == login_status['password']:
            origin_client, origin_character = None, None
            #. check current in game?
            if character_was_login(character):
                client.send('\nThis name was login, kick the user!\n')
                origin_client, origin_character = find_origin_client_and_character(character)
                character = copy.deepcopy(origin_character) #. copy the character object, because the origin character object wiil be drop
                origin_client.send("Somebody login from %s, see you again!\n" % (client.addrport()) )
                status.QUIT_CLIENTS.append(origin_client) #. origin character object drop here
            character.client = client
            #. remove origin_character in characters list if exist
            if origin_client:
                status.CHARACTERS.pop(origin_client) if status.CHARACTERS.has_key(origin_client) else None
            status.CHARACTERS[client] = character
            #. remove client from login queue
            status.UNLOGIN_CLIENTS.pop(client)
            broadcast('%s enter the world.\n' % status.CHARACTERS[client].get_name() )
            print ('** Client %s login success with name: %s.' % (client.addrport(), login_status['name']))
            return True
        else:
            print ('!! Client %s login fail with name: %s.' % (client.addrport(), login_status['name']) )
            return False
    return False

def login_get_name(client):
    """docstring for login_get_name"""
    login_status = status.UNLOGIN_CLIENTS[client]
    if not login_status['name']:
        if not login_status['name_process']:
            client.send("Username:")
            login_status['name_process'] = True
            return
        if login_status['name_process'] and client.cmd_ready:
            login_status['name'] = client.get_command()
            print ('** Client %s try to login with name: %s.' % (client.addrport(), login_status['name']) )
            return

def login_get_password(client):
    """docstring for login_get_password"""
    login_status = status.UNLOGIN_CLIENTS[client]
    if not login_status['password']:
        if login_status['name'] and not login_status['password_process']:
            client.password_mode_on()
            client.send("Password:")
            login_status['password_process'] = True
            return
        if login_status['name'] and login_status['password_process'] and client.cmd_ready:
            login_status['password'] = client.get_command()
            client.password_mode_off()
            client.send('\n')
            return

def login(client):
    """login the clietn."""
    #. get name
    login_status = status.UNLOGIN_CLIENTS[client]
    login_get_name(client)
    login_get_password(client)
    if login_status['name'] and login_status['password']:
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

