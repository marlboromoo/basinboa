#!/usr/bin/env python
"""
commands !
"""
from world import north_xy, south_xy, west_xy, east_xy

class Command(object):
    """docstring for Command"""

    CMDS = [ 'chat', 'quit', 'look', 'north', 'south', 'west', 'east']
    CMDS_ALIAS = {
        'l' : 'look',
        'n' : 'north',
        'w' : 'west',
        'e' : 'east',
        's' : 'south',
    }

    def __init__(self, client, clients, inputs, maps):
        super(Command, self).__init__()
        self.client = client
        self.clientS = clients
        self.inputs = inputs
        self.maps = maps
        self.process_inputs(inputs)

    def alias_2_cmd(self, cmd):
        """docstring for alias_2_cmd"""
        return self.CMDS_ALIAS[cmd] if self.CMDS_ALIAS.has_key(cmd) else None

    def cmd_exist(self, cmd):
        """docstring for check_cmd"""
        return True if cmd in self.CMDS else False

    def fire_cmd(self, cmd, args):
        """docstring for fire_cmd"""
        if self.cmd_exist(cmd):
            #. call the method by cmd name
            getattr(self, cmd)(args)
        else:
            cmd = self.alias_2_cmd(cmd)
            self.client.send('Huh?\n')
        
    def process_inputs(self, inputs):
        """docstring for self.process_inputs"""
        inputs = inputs.split()
        #print inputs
        cmd = inputs[0].lower()
        inputs.remove(cmd)
        args = inputs
        if not self.cmd_exist(cmd):
            cmd = self.alias_2_cmd(cmd)
            self.fire_cmd(cmd, args)
        else:
            self.fire_cmd(cmd, args)

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

    def locate_user_room(self):
        """docstring for locate_user_room"""
        map_ = self.client.soul.map_
        xy = self.client.soul.xy
        return self.maps.get_map(map_).get_room(xy)

    def look(self, args):
        """docstring for look"""
        room = self.locate_user_room()
        self.client.send('%s\n' % (room.texts))
        self.client.send('exits: %s, id: %s, xy: %s\n' % (room.exits, room.id_, str(room.xy)))

    def north(self, args):
        """docstring for north"""
        room = self.locate_user_room()
        soul = self.client.soul
        x, y = soul.xy
        if 'n' in room.exits:
            dst_xy = north_xy(x, y)
            if dst_xy in room.paths:
                soul.xy = dst_xy
                self.client.send('You go to north !\n')
        else:
            self.client.send('Huh?\n')

    def go(self, symbol, function, message):
        """docstring for go"""
        room = self.locate_user_room()
        soul = self.client.soul
        x, y = soul.xy
        if symbol in room.exits:
            dst_xy = function(x, y)
            if dst_xy in room.paths:
                soul.xy = dst_xy
                self.client.send('You go to %s !\n' % (message))
        else:
            self.client.send('Huh?\n')

    def west(self, args):
        """docstring for west"""
        room = self.locate_user_room()
        soul = self.client.soul
        x, y = soul.xy
        if 'w' in room.exits:
            dst_xy = west_xy(x, y)
            if dst_xy in room.paths:
                soul.xy = dst_xy
                self.client.send('You go to west !\n')
        else:
            self.client.send('Huh?\n')

    def east(self, args):
        """docstring for east"""
        room = self.locate_user_room()
        soul = self.client.soul
        x, y = soul.xy
        if 'e' in room.exits:
            dst_xy = east_xy(x, y)
            if dst_xy in room.paths:
                soul.xy = dst_xy
                self.client.send('You go to east !\n')
        else:
            self.client.send('Huh?\n')

    def south(self, args):
        """docstring for south"""
        room = self.locate_user_room()
        soul = self.client.soul
        x, y = soul.xy
        if 's' in room.exits:
            dst_xy = south_xy(x, y)
            if dst_xy in room.paths:
                soul.xy = dst_xy
                self.client.send('You go to south !\n')
        else:
            self.client.send('Huh?\n')

    def quit(self, args):
        """docstring for quit"""
        self.client.active = False


