#!/usr/bin/env python
"""
system libs
"""
from player import Soul
from command import Command as command

class System(object):
    """docstring for System"""

    SERVER_RUN = True
    IDLE_TIMEOUT = 300
    CLIENTS = []

    def __init__(self):
        super(System, self).__init__()
        
    def inject_client(self, client):
        """docstring for inject_client"""
        client.soul = Soul(client)
        client.login = None
        client.username = None
        client.username_process = None
        client.password = None
        client.password_process = None
    
    def auth_client(self, client):
        """auth the client."""
        if client.username and client.password:
            #. check process
            client.soul.set_name(client.username)
            self.broadcast('%s enter the world.\n' % client.soul.get_name() )
            return True
    
    def login(self, client):
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
        #. auth 
        if client.username and client.password:
            client.login = True if self.auth_client(client) else False
            if client.login:
                client.send("\nWelcome !!! %s !!! \n"  % (client.soul.get_name()))
            else:
                client.password, client.password_process = None, None
        
    def on_connect(self, client):
        """
        Sample on_connect function.
        Handles new connections.
        """
        print "++ Opened connection to %s" % client.addrport()
        self.broadcast('Unkown try to enter the world from %s.\n' % client.addrport() )
        self.CLIENTS.append(client)
        client.send("Welcome to the strachmud, please login.\n")
        self.inject_client(client)
    
    def on_disconnect(self, client):
        """
        Sample on_disconnect function.
        Handles lost connections.
        """
        print "-- Lost connection to %s" % client.addrport()
        self.CLIENTS.remove(client)
        self.broadcast('%s leaves the world.\n' % client.addrport() )
    
    
    def kick_idle(self):
        """
        Looks for idle clients and disconnects them by setting active to False.
        """
        ## Who hasn't been typing?
        for client in self.CLIENTS:
            if client.idle() > self.IDLE_TIMEOUT:
                print('-- Kicking idle lobby client from %s' % client.addrport())
                client.active = False
    
    
    def process_clients(self):
        """
        Check each client, if client.cmd_ready == True then there is a line of
        input available via client.get_command().
        """
        for client in self.CLIENTS:
            if not client.login:
                self.login(client)
            if client.active and client.cmd_ready:
                ## If the client sends input echo it to the chat room
                self.process_command(client)

    def process_command(self, client):
        """
        Process the client input.
        """
        msg = client.get_command()
        command.chat(client, self.CLIENTS, msg)
    
        cmd = msg.lower()
        if cmd == 'bye' or cmd == 'exit' or cmd == 'quit':
            self.disconnect(client)
        elif cmd == 'shutdown':
            self.shutdown()
    
    def broadcast(self, msg):
        """
        Send msg to every client.
        """
        for client in self.CLIENTS:
            if client.login:
                client.send(msg)

    def disconnect(self, client):
        """disconnect the client."""
        client.active = False

    def shutdown(self):
        """Shutdown the server."""
        self.SERVER_RUN = False
    
