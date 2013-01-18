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

    def __init__(self, world):
        super(System, self).__init__()
        self.clients = []
        self.world = world
        
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
            #. check process ..
            client.soul = Soul(client.username)
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
        #. auth, TODO: load player profile
        if client.username and client.password:
            client.login = True if self.auth_client(client) else False
            if client.login:
                client.send("\nWelcome !!! %s !!! \n"  % (client.soul.get_name()))
                self.world.locate_client_map(client).add_client(client)
            else:
                client.password, client.password_process = None, None
        
    def on_connect(self, client):
        """
        Sample on_connect function.
        Handles new connections.
        """
        print "++ Opened connection to %s" % client.addrport()
        self.broadcast('Unkown try to enter the world from %s.\n' % client.addrport() )
        self.clients.append(client)
        client.send("Welcome to the strachmud, please login.\n")
        self.inject_client(client)
    
    def on_disconnect(self, client):
        """
        Sample on_disconnect function.
        Handles lost connections.
        """
        print "-- Lost connection to %s" % client.addrport()
        self.clients.remove(client)
        self.broadcast('%s leaves the world.\n' % client.addrport() )
    
    
    def kick_idle(self):
        """
        Looks for idle clients and disconnects them by setting active to False.
        """
        ## Who hasn't been typing?
        for client in self.clients:
            if client.idle() > self.IDLE_TIMEOUT:
                print('-- Kicking idle lobby client from %s' % client.addrport())
                client.active = False
    
    
    def process_clients(self):
        """
        Check each client, if client.cmd_ready == True then there is a line of
        input available via client.get_command().
        """
        for client in self.clients:
            if not client.login:
                self.login(client)
            if client.active and client.cmd_ready:
                self.process_command(client)

    def process_command(self, client):
        """
        Process the client input.
        """
        inputs = client.get_command()
    
        cmd = inputs.lower()
        #. check if system command
        if cmd == 'shutdown':
            self.shutdown()
        #. other commands
        else:
            if len(cmd) > 0:
                command(client, self.clients, inputs, self.world)
    
    def broadcast(self, msg):
        """
        Send msg to every client.
        """
        for client in self.clients:
            if client.login:
                client.send(msg)

    def disconnect(self, client):
        """disconnect the client."""
        client.active = False

    def shutdown(self):
        """Shutdown the server."""
        self.SERVER_RUN = False
    
