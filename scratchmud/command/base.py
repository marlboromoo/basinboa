#!/usr/bin/env python
"""
commands !
"""

from scratchmud.command import cmds
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
    if hasattr(cmds, str(cmd)):
        if isfunction(getattr(cmds, cmd)):
            return True 
    return False

def fire_cmd(client, cmd, args):
    """docstring for fire_cmd"""
    getattr(cmds, cmd)(client, args)
    
def process_inputs(client, inputs):
    """docstring for process_inputs"""
    inputs = inputs.split()
    #print inputs
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

def invalid_args(client):
    """docstring for invalid_args"""
    client.send("Invalid args !")

