#!/usr/bin/env python
"""
commands !
"""

class Command(object):
    """docstring for Command"""

    CMDS = [ 'chat', 'quit', 'look' ]

    def __init__(self, client, clients, inputs, maps):
        super(Command, self).__init__()
        self.client = client
        self.clientS = clients
        self.inputs = inputs
        self.maps = maps
        self.process_inputs(inputs)
        self.maps = maps

    def cmd_exist(self, cmd):
        """docstring for check_cmd"""
        return True if cmd in self.CMDS else False
        
    def process_inputs(self, inputs):
        """docstring for self.process_inputs"""
        inputs = inputs.split()
        #print inputs
        cmd = inputs[0].lower()
        inputs.remove(cmd)
        args = inputs
        if self.cmd_exist(cmd):
            #. call the method by cmd name
            getattr(self, cmd)(args)
        else:
            self.client.send('Huh?\n')

    def chat(self, args):
        """
        Echo whatever client types to everyone.
        """
        msg = ' '.join(args)
        print '%s says, "%s"' % (self.client.soul.get_name(), msg)
    
        for guest in self.clientS:
            if guest != self.client:
                guest.send('%s says: %s\n' % (self.client.soul.get_name(), msg))
            else:
                guest.send('You say: %s\n' % msg)

    def look(self, args):
        """docstring for look"""
        map_ = self.client.soul.map_
        xy = self.client.soul.xy
        self.client.send('%s\n' % (self.maps.get_map(map_).get_room(xy).texts))

    def quit(self, args):
        """docstring for quit"""
        self.client.active = False


