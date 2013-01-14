#!/usr/bin/env python
"""
commands !
"""

class Command(object):
    """docstring for Command"""

    CMDS = [ 'chat', 'quit' ]

    def __init__(self, client, clients, inputs):
        super(Command, self).__init__()
        self.CLIENT = client
        self.CLIENTS = clients
        self.INPUTS = inputs
        self.process_inputs(inputs)

    def cmd_exist(self, cmd):
        """docstring for check_cmd"""
        return True if cmd in self.CMDS else False
        
    def process_inputs(self, inputs):
        """docstring for self.process_inputs"""
        inputs = inputs.split()
        cmd = inputs[0].lower()
        inputs.remove(cmd)
        args = inputs
        if self.cmd_exist(cmd):
            #. call the method by cmd name
            getattr(self, cmd)(args)
        else:
            self.CLIENT.send('Huh?\n')

    def chat(self, args):
        """
        Echo whatever client types to everyone.
        """
        msg = ' '.join(args)
        print '%s says, "%s"' % (self.CLIENT.soul.get_name(), msg)
    
        for guest in self.CLIENTS:
            if guest != self.CLIENT:
                guest.send('%s says: %s\n' % (self.CLIENT.soul.get_name(), msg))
            else:
                guest.send('You say: %s\n' % msg)

    def quit(self, args):
        """docstring for quit"""
        self.CLIENT.active = False


