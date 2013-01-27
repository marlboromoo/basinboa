#!/usr/bin/env python
"""
commands !
"""

from basinboa import status
from basinboa.command import cmds
from inspect import isfunction

CMDS_ALIAS = {
    'l' : 'look',
    'n' : 'north',
    'w' : 'west',
    'e' : 'east',
    's' : 'south',
    'u' : 'up',
    'd' : 'down',
}

def alias_2_cmd(cmd):
    """docstring for alias_2_cmd"""
    return CMDS_ALIAS[cmd] if CMDS_ALIAS.has_key(cmd) else None

def cmd_exist(cmd):
    """docstring for check_cmd"""
    return True if status.COMMANDS.has_key(cmd) else False

def fire_cmd(client, cmd, args):
    """docstring for fire_cmd"""
    status.COMMANDS.get(cmd)(client, args)
    
def process_command(client, inputs):
    """docstring for process_command"""
    inputs = inputs.split()
    cmd = inputs[0].lower()
    inputs.remove(cmd)
    args = inputs
    if not cmd_exist(cmd):
        cmd = alias_2_cmd(cmd)
        if cmd_exist(cmd):
            fire_cmd(client, cmd, args)
        else:
            client.send("Huh ?\n")
    else:
        fire_cmd(client, cmd, args)

def process_inputs(client):
    """
    Process the client input.
    """
    inputs = client.get_command()
    if len(inputs) == 0:
        #. send prompt
        prompt = status.CHARACTERS.get(client).get_prompt()
        client.send(prompt)
    else:
        cmd = inputs.lower()
        #. check if system command
        if cmd == 'shutdown':
            shutdown()
        #. other commands
        else:
            if len(cmd) > 0:
                process_command(client, inputs)

def register_cmds():
    """register commands from cmds.* to global status"""
    for attr in dir(cmds):
        object_ = getattr(cmds, attr)
        if isfunction(object_) and hasattr(object_, 'is_command'):
            #. check the functions is command
            if object_.is_command:
                status.COMMANDS[attr] = object_
