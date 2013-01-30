#!/usr/bin/env python
"""
unlogin user.
"""
import copy
from basinboa import status
from basinboa.system.scheduler import SCHEDULER
from basinboa.message.broadcast import broadcast
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
        self.quit = False
        self.greet()
        self.login()
    
    def greet(self):
        """docstring for greeting"""
        self.client.send_cc("^R^!%s^~\n" % (status.ASCII_ART))
        self.client.send("Welcome to the %s, please login.\n" % (status.SERVER_CONFIG['mud_name']))
    
    def login(self):
        """login the clietn."""
        self.check_retry()
        if not self.retry >= RETRY_LIMIT:
            self.get_name()
            self.get_password()
            if self.name and self.password:
                if self.auth():
                    self.is_login = True
                else:
                    self.client.send("Password error!\n")
                    self.is_login = False
                    self.retry += 1
                #. final login
                if self.is_login:
                    self.client.send("\nWelcome !!! %s !!! \n"  % (self.name))
                else:
                    self.password, self.process_password = None, None

    def check_retry(self):
        """check if reach to RETRY_LIMIT"""
        if not self.quit and self.retry >= RETRY_LIMIT:
            self.quit = True
            self.client.send("Retry too many times, bye!\n")
            print "!! Client reach to the login limit: %s, kicking! " % (RETRY_LIMIT)
            SCHEDULER.add(.2, self.client.deactivate)


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
                    #self.check_retry()
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
                    return
                else:
                    self.client.send("\nPlease enter your password!\n")
                    self.retry += 1
                    self.password, self.process_password = None, None
                    #self.check_retry()
                    return

    def promote(self, character):
        """Guest become Player"""
        player = Player(self.client, character)
        #. add Player object in status
        status._PLAYERS[self.client] = player
        status.PLAYERS[self.name] = player
        #. add Player object in World object
        status.WORLD.locate_player_map(player).add_player(player)
        #. delete Guest object from LOBBY
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
                        #. drop origin Player
                        SCHEDULER.add(.2, origin_player.deactivate)
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
        for player in status.PLAYERS.values():
            if player.get_name() == self.name:
                return player
        return None
        

