#!/usr/bin/env python
"""
unlogin user.
"""
import copy
from basinboa import status
from basinboa.message import broadcast
from basinboa.user.account import Account
from basinboa.user.player import Player

RETRY_LIMIT = 3

class Guest(Account):
    """docstring for G"""
    def __init__(self, client):
        super(Guest, self).__init__(client)
        self.is_login = False
        self.process_name = None
        self.process_password = None
        self.retry = 0
        self.login()

    def login(self):
        """login the clietn."""
        #. get name
        self.check_retry()
        self.get_name()
        self.get_password()
        if self.name and self.password:
            if self.auth():
                self.is_login = True
            else:
                self.is_login = False
                self.retry += 1
                self.check_retry()
            #. final login
            if self.is_login:
                self.client.send("\nWelcome !!! %s !!! \n"  % (self.name))
            else:
                self.password, self.process_password = None, None

    def check_retry(self):
        """check if reach to RETRY_LIMIT"""
        if self.retry >= RETRY_LIMIT:
            self.client.send("Retry too many times, bye!\n")
            print "!! Client reach to the login limit: %s, kicking! " % (RETRY_LIMIT)
            status.QUIT_CLIENTS.append(self.client)


    def get_name(self):
        """get login name"""
        if not self.name:
            if not self.process_name:
                self.client.send("Username: ")
                self.process_name = True
                return
            if self.process_name and self.client.cmd_ready:
                self.name = self.client.get_command()
                if len(self.name) > 0:
                    print ('** Client %s try to login with name: %s.' % (self.client.addrport(), self.name) )
                    self.retry = 0
                    return
                else:
                    self.client.send("Please enter your name!\n")
                    self.retry += 1
                    self.name, self.process_name = None, None
                    self.check_retry()
                    return
    
    def get_password(self):
        """get login password"""
        if not self.password:
            if self.name and not self.process_password:
                self.client.password_mode_on()
                self.client.send("Password: ")
                self.process_password = True
                return
            if self.name and self.process_password and self.client.cmd_ready:
                self.password = self.client.get_command()
                if len(self.password) >0:
                    self.client.password_mode_off()
                    self.client.send('\n')
                    return
                else:
                    self.client.send("\nPlease enter your password!\n")
                    self.retry += 1
                    self.password, self.process_password = None, None
                    self.check_retry()
                    return

    def promote(self, character):
        """Guest become Player"""
        player = Player(self.client, character)
        status.PLAYERS[self.name] = player
        status.WORLD.locate_player_map(player).add_player(player)
        self.destroy()

    def destroy(self):
        """destroy self from lobby"""
        status.LOBBY.pop(self.client)

    def password_match(self):
        """docstring for check_password"""
        status.CHARACTER_LOADER.load(self.name)
        character = status.CHARACTER_LOADER.get(self.name)
        return True if character.get_password() == self.password else False

    def auth(self):
        """auth the client."""
        if self.client in status.LOBBY:
            status.CHARACTER_LOADER.load(self.name)
            character = status.CHARACTER_LOADER.get(self.name)
            if character:
                if character.get_password() == self.password:
                    origin_player = None
                    #. check current in game?
                    if self.player_was_login(self.name):
                        self.client.send('\nThis name was login, kick the user!\n')
                        origin_player = self.get_origin_player()
                        character = copy.deepcopy(origin_player.character) #. copy the character object, because the origin character object wiil be drop
                    #. send notice to origin player
                    if origin_player:
                        origin_player.send("Somebody login from %s, see you again!\n" % (self.client.addrport()) )
                        #. TODO: quit client
                        status.QUIT_CLIENTS.append(origin_player.client) #. origin character object drop here
                    #. become player
                    self.promote(character)
                    broadcast('%s enter the world.\n' % self.name )
                    print ('** Client %s login success with name: %s.' % (self.client.addrport(), self.name))
                    return True
                else:
                    print ('!! Client %s login fail with name: %s.' % (self.client.addrport(), self.client) )
                    return False
        return False

    def player_was_login(self, name):
        """docstring for character_in_game"""
        if name in [player.name for player in status.PLAYERS.values()]:
            return True
        return False
    
    def get_origin_player(self):
        """docstring for find_origin_client"""
        for player in status.PLAYERS.values:
            if player.get_name() == self.name:
                return player
        return None
        

#def login_queue(client):
#    """docstring for login_queue"""
#    status.UNLOGIN_CLIENTS[client] = {
#        'login' : None,
#        'name' : None,
#        'name_process' : None,
#        'password' : None,
#        'password_process' : None,
#        'retry' : 0,
#    }
#
#def character_was_login(character):
#    """docstring for character_in_game"""
#    if character.name in [character.name for character in status.CHARACTERS.values()]:
#        return True
#    return False
#
#def find_origin_client_and_character(character):
#    """docstring for find_origin_client"""
#    for client, character_ in status.CHARACTERS.items():
#        if character_.get_name() == character.get_name():
#            return client, character_
#    return None, None
#
#def auth_client(client):
#    """auth the client."""
#    if client in status.UNLOGIN_CLIENTS:
#        login_status = status.UNLOGIN_CLIENTS[client]
#        status.CHARACTER_LOADER.load(login_status['name'])
#        character = status.CHARACTER_LOADER.get(login_status['name'])
#        #. check password correct
#        if character and character.get_password() == login_status['password']:
#            origin_client, origin_character = None, None
#            #. check current in game?
#            if character_was_login(character):
#                client.send('\nThis name was login, kick the user!\n')
#                origin_client, origin_character = find_origin_client_and_character(character)
#                character = copy.deepcopy(origin_character) #. copy the character object, because the origin character object wiil be drop
#            character.client = client
#            #. remove origin_character in characters list if exist
#            if origin_client:
#                origin_client.send("Somebody login from %s, see you again!\n" % (client.addrport()) )
#                status.QUIT_CLIENTS.append(origin_client) #. origin character object drop here
#            status.CHARACTERS[client] = character
#            #. remove client from login queue
#            status.UNLOGIN_CLIENTS.pop(client)
#            broadcast('%s enter the world.\n' % status.CHARACTERS[client].get_name() )
#            print ('** Client %s login success with name: %s.' % (client.addrport(), login_status['name']))
#            return True
#        else:
#            print ('!! Client %s login fail with name: %s.' % (client.addrport(), login_status['name']) )
#            return False
#    return False
#
#def login_get_name(client):
#    """docstring for login_get_name"""
#    login_status = status.UNLOGIN_CLIENTS[client]
#    if not login_status['name']:
#        if not login_status['name_process']:
#            client.send("Username:")
#            login_status['name_process'] = True
#            return
#        if login_status['name_process'] and client.cmd_ready:
#            login_status['name'] = client.get_command()
#            print ('** Client %s try to login with name: %s.' % (client.addrport(), login_status['name']) )
#            return
#
#def login_get_password(client):
#    """docstring for login_get_password"""
#    login_status = status.UNLOGIN_CLIENTS[client]
#    if not login_status['password']:
#        if login_status['name'] and not login_status['password_process']:
#            client.password_mode_on()
#            client.send("Password:")
#            login_status['password_process'] = True
#            return
#        if login_status['name'] and login_status['password_process'] and client.cmd_ready:
#            login_status['password'] = client.get_command()
#            client.password_mode_off()
#            client.send('\n')
#            return
#
#def login(client):
#    """login the clietn."""
#    #. get name
#    login_status = status.UNLOGIN_CLIENTS[client]
#    login_get_name(client)
#    login_get_password(client)
#    if login_status['name'] and login_status['password']:
#        if auth_client(client):
#            login_status['login'] = True
#        else:
#            login_status['login'] = False
#            login_status['retry'] += 1
#        #. disconnect client if retry too many
#        if login_status['retry'] >= 3: 
#            client.send("\nRetry too many times, bye!\n")
#            status.QUIT_CLIENTS.append(client)
#            return 
#        #. final login
#        if login_status['login']:
#            client.send("\nWelcome !!! %s !!! \n"  % (status.CHARACTERS[client].get_name()))
#            status.WORLD.locate_client_map(client).add_client(client)
#        else:
#            login_status['password'], login_status['password_process'] = None, None
#
