#!/usr/bin/env python
"""
commands !
"""

import status
from world import north_xy, south_xy, west_xy, east_xy, NORTH, SOUTH, EAST, WEST

class Command(object):
    """docstring for Command"""

    CMDS = [ 'chat', 'quit', 'look', 'rooms', 'maps',
            'goto', 'north', 'south', 'west', 'east']
    CMDS_ALIAS = {
        'l' : 'look',
        'n' : 'north',
        'w' : 'west',
        'e' : 'east',
        's' : 'south',
    }

    def __init__(self, client, inputs):
        super(Command, self).__init__()
        self.client = client
        self.inputs = inputs
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

    def invalid_args(self):
        """docstring for invalid_args"""
        self.client.send("Invalid args !")

    def chat(self, args):
        """
        Echo whatever client types to everyone.
        """
        msg = ' '.join(args)
        print '%s says, "%s"' % (status.PLAYERS[self.client].get_name(), msg)
    
        for guest in status.CLIENTS:
            if guest != self.client:
                guest.send('%s says: %s\n' % (status.PLAYERS[self.client].get_name(), msg))
            else:
                guest.send('You say: %s\n' % msg)

    def look(self, args):
        """docstring for look"""
        room = status.WORLD.locate_client_room(self.client)
        self.client.send('%s\n' % (room.texts.encode( "big5" )))
        self.client.send('exits: %s, id: %s, xy: %s\n' % (room.exits, room.id_, str(room.xy)))

    def go(self, symbol, function, message):
        """docstring for go"""
        room = status.WORLD.locate_client_room(self.client)
        player = status.PLAYERS[self.client]
        print player
        x, y = player.xy
        if symbol in room.exits:
            dst_xy = function(x, y)
            if dst_xy in room.paths:
                player.set_location(dst_xy)
                print player.xy
                #. remove client form source room
                room.remove_client(self.client)
                #. add client in target room
                status.WORLD.locate_client_room(self.client).add_client(self.client)
                self.client.send('You go to %s !\n' % (message))
        else:
            self.client.send('Huh?\n')

    def goto(self, args):
        """docstring for goto"""
        if len(args) == 3:
            x, y, map_ = args
        elif len(args) == 2:
            x, y = args
            map_ = status.PLAYERS[self.client].map_name
        else:
            return self.invalid_args()
        try:
            x, y = int(x), int(y)
        except Exception:
            return self.invalid_args()
        map_ = status.WORLD.get_map(map_)
        room =  map_.get_room((x,y))
        if map_:
            if room:
                src_map = status.WORLD.locate_client_map(self.client)
                src_map.remove_client(self.client)
                status.PLAYERS[self.client].set_location((x,y), map_.get_name())
                map_.add_client(self.client)
                return self.look(None)
            else:
                self.client.send("You can't!")

    def rooms(self, args):
        """docstring for rooms"""
        rooms = status.WORLD.locate_client_map(self.client).get_rooms()
        for room in rooms:
            #. TODO use repr() instesd .
            #msg = "Room%s%s - %s,  " % (
            #    str(room.id_), str(room.xy), str('/'.join(room.exits)))
            self.client.send("%s\n" % repr(room))

    def maps(self, args):
        """docstring for maps"""
        maps = status.WORLD.get_maps()
        for map_ in maps:
            self.client.send("%s\n" % repr(map_))

    def west(self, args):
        """docstring for west"""
        self.go(WEST, west_xy, 'west')
        return self.look(None)

    def east(self, args):
        """docstring for east"""
        self.go(EAST, east_xy, 'east')
        return self.look(None)

    def north(self, args):
        """docstring for north"""
        self.go(NORTH, north_xy, 'north')
        return self.look(None)

    def south(self, args):
        """docstring for south"""
        self.go(SOUTH, south_xy, 'south')
        return self.look(None)

    def quit(self, args):
        """docstring for quit"""
        self.client.active = False


