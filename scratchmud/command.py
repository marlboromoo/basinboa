#!/usr/bin/env python
"""
commands !
"""

import status
from encode import texts_encoder
from message import broadcast, client_message_to_room, client_message_to_map

class Command(object):
    """docstring for Command"""

    CMDS = [ 'chat', 'quit', 'look', 'rooms', 'maps', 'who', 'mobs', 'save',
            'track', 'follow',
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
        self.player = status.PLAYERS[client]
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
        print '%s says, "%s"' % (self.player.get_name(), msg)
    
        for guest in status.CLIENTS:
            if guest != self.client:
                guest.send('%s says: %s\n' % (self.player.get_name(), msg))
            else:
                guest.send('You say: %s\n' % msg)

    def look(self, args):
        """docstring for look"""
        target = args[0] if args else None
        return status.PLAYERS[self.client].look(target)

    def go(self, symbol, function, message):
        """docstring for go"""
        room = status.WORLD.locate_client_room(self.client)
        x, y = self.player.xy
        if symbol in room.exits:
            dst_xy = function(x, y)
            if dst_xy in room.paths:
                #. message to all the players in room
                client_message_to_room(self.client, '%s go to %s!\n' % (self.player.get_name(), message))
                #. move player to room
                self.player.set_location(dst_xy)
                #. remove player form source room
                room.remove_client(self.client)
                #. add client in target room
                status.WORLD.locate_client_room(self.client).add_client(self.client)
                #. send message to all the players in target room
                self.client.send('You go to %s !\n' % (message))
                client_message_to_room(self.client, '%s come to here!\n' % (self.player.get_name()))
        else:
            self.client.send('Huh?\n')

    def goto(self, args):
        """docstring for goto"""
        if len(args) == 3:
            x, y, map_ = args
        elif len(args) == 2:
            x, y = args
            map_ = self.player.map_name
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
                src_room = status.WORLD.locate_client_room(self.client)
                #. send message notice all players in the room
                client_message_to_room(self.client, "%s leave here.\n" % (self.player.get_name()) )
                #. remove player in old place
                src_map.remove_client(self.client)
                src_room.remove_client(self.client)
                #. move player to destation
                self.player.set_location((x,y), map_.get_name())
                map_.add_client(self.client)
                #. send message 
                client_message_to_room(self.client, '%s come to here!\n' % (self.player.get_name()))
                return self.look(None)
            else:
                self.client.send("You can't!")

    def rooms(self, args):
        """docstring for rooms"""
        rooms = status.WORLD.locate_client_map(self.client).get_rooms()
        for room in rooms:
            self.client.send("%s\n" % repr(room))

    def maps(self, args):
        """docstring for maps"""
        maps = status.WORLD.get_maps()
        for map_ in maps:
            self.client.send("%s\n" % repr(map_))

    def mobs(self, args):
        """docstring for mobs"""
        maps = status.WORLD.get_maps()
        for map_ in maps:
            for mob in map_.get_mobs():
                self.client.send("%s\n" % repr(mob))

    def west(self, args):
        """docstring for west"""
        status.PLAYERS[self.client].go_west()

    def east(self, args):
        """docstring for east"""
        status.PLAYERS[self.client].go_east()

    def north(self, args):
        """docstring for north"""
        status.PLAYERS[self.client].go_north()

    def south(self, args):
        """docstring for south"""
        status.PLAYERS[self.client].go_south()

    def who(self, args):
        """docstring for who"""
        for player in status.PLAYERS.values():
            self.client.send("%s\n" % repr(player))

    def quit(self, args):
        """docstring for quit"""
        self.client.send('\nSee you next time ! \n')
        status.QUIT_CLIENTS.append(self.client)

    def save(self, args):
        """docstring for save"""
        msg = 'okay.' if  status.PLAYER_LOADER.save(status.PLAYERS[self.client]) else 'fail!'
        self.client.send('%s\n' % (msg))

    def _follow(self, function, name):
        """docstring for _follow"""
        target = function(name)
        if target:
            name = target.mobname if hasattr(target, 'mobname') else target.username
            player = status.PLAYERS[self.client]
            target.add_follower(player)
            player.follow(target)
            self.client.send("You start to follow %s!\n" % (name))
        else:
            self.client.send("No such target !\n")

    def follow(self, args):
        """docstring for follow"""
        target_name = args[0]
        room = status.WORLD.locate_client_room(self.client)
        return self._follow(room.get_player_by_username, target_name)

    def track(self, args):
        """docstring for track"""
        target_name = args[0]
        room = status.WORLD.locate_client_room(self.client)
        return self._follow(room.get_mob_by_mobname, target_name)



