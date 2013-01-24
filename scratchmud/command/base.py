#!/usr/bin/env python
"""
commands !
"""

from scratchmud import status
from scratchmud.command import cmds
from inspect import isfunction

class Command(object):
    """call"""

    #CMDS = [ 'chat', 'quit', 'look', 'rooms', 'maps', 'who', 'mobs', 'save',
    #        'track', 'follow', 'kill',
    #        'goto', 'north', 'south', 'west', 'east', 'up', 'down']
    CMDS_ALIAS = {
        'l' : 'look',
        'n' : 'north',
        'w' : 'west',
        'e' : 'east',
        's' : 'south',
        'u' : 'up',
        'd' : 'down',
    }

    def __init__(self, client, inputs):
        super(Command, self).__init__()
        self.client = client
        self.character = status.CHARACTERS[client]
        self.inputs = inputs
        self.process_inputs(inputs)

    def alias_2_cmd(self, cmd):
        """docstring for alias_2_cmd"""
        return self.CMDS_ALIAS[cmd] if self.CMDS_ALIAS.has_key(cmd) else None

    def cmd_exist(self, cmd):
        """docstring for check_cmd"""
        if hasattr(cmds, str(cmd)):
            if isfunction(getattr(cmds, cmd)):
                return True 
        return False

    def fire_cmd(self, cmd, args):
        """docstring for fire_cmd"""
        getattr(cmds, cmd)(self, args)
        
    def process_inputs(self, inputs):
        """docstring for self.process_inputs"""
        inputs = inputs.split()
        #print inputs
        cmd = inputs[0].lower()
        inputs.remove(cmd)
        args = inputs
        if not self.cmd_exist(cmd):
            cmd = self.alias_2_cmd(cmd)
            if self.cmd_exist(cmd):
                self.fire_cmd(cmd, args)
            else:
                self.client.send("Huh ?\n")
        else:
            self.fire_cmd(cmd, args)

    def invalid_args(self):
        """docstring for invalid_args"""
        self.client.send("Invalid args !")

