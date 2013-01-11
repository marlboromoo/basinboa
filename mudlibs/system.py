#!/usr/bin/env python
"""
system libs
"""
from player import Soul

IDLE_TIMEOUT = 300
CLIENT_LIST = []
SERVER_RUN = True

def init_client(client):
    """docstring for init_client"""
    client.soul = Soul(client)
    client.login = None
    client.username = None
    client.username_process = None
    client.password = None
    client.password_process = None

def login(client):
    """docstring for login"""
    if not client.username_process:
        client.send("Username:")
        client.username_process = True
    if client.username_process:
        client.username = client.get_command()
    if client.username and not client.password_process:
        client.password_mode_on()
        client.send("Password:")
        client.password_process = True
    if client.username and client.password_process:
        client.password = client.get_command()
        client.password_mode_off()
        client.login = True
    #if client.username and client.password:
    #    client.send("%s, %s" % (client.username, client.password))
    
def on_connect(client):
    """
    Sample on_connect function.
    Handles new connections.
    """
    print "++ Opened connection to %s" % client.addrport()
    broadcast('%s joins the conversation.\n' % client.addrport() )
    CLIENT_LIST.append(client)
    client.send("Welcome to the Chat Server, %s.\n" % client.addrport() )
    init_client(client)



def on_disconnect(client):
    """
    Sample on_disconnect function.
    Handles lost connections.
    """
    print "-- Lost connection to %s" % client.addrport()
    CLIENT_LIST.remove(client)
    broadcast('%s leaves the conversation.\n' % client.addrport() )


def kick_idle():
    """
    Looks for idle clients and disconnects them by setting active to False.
    """
    ## Who hasn't been typing?
    for client in CLIENT_LIST:
        if client.idle() > IDLE_TIMEOUT:
            print('-- Kicking idle lobby client from %s' % client.addrport())
            client.active = False


def process_clients():
    """
    Check each client, if client.cmd_ready == True then there is a line of
    input available via client.get_command().
    """
    for client in CLIENT_LIST:
        if not client.login:
            login(client)
        if client.active and client.cmd_ready:
            ## If the client sends input echo it to the chat room
            chat(client)


def broadcast(msg):
    """
    Send msg to every client.
    """
    for client in CLIENT_LIST:
        client.send(msg)


def chat(client):
    """
    Echo whatever client types to everyone.
    """
    global SERVER_RUN
    msg = client.get_command()
    print '%s says, "%s"' % (client.addrport(), msg)

    for guest in CLIENT_LIST:
        if guest != client:
            guest.send('%s says, %s\n' % (client.addrport(), msg))
        else:
            guest.send('You say, %s\n' % msg)

    cmd = msg.lower()
    ## bye = disconnect
    if cmd == 'bye':
        client.active = False
    ## shutdown == stop the server
    elif cmd == 'shutdown':
        SERVER_RUN = False
