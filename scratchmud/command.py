#!/usr/bin/env python
"""
commands !
"""

import status

class Command(object):
    """docstring for Command"""

    CMDS = [ 'chat', 'quit', 'look', 'rooms', 'maps', 'who', 'mobs', 'save',
            'track', 'follow', 'kill',
            'goto', 'north', 'south', 'west', 'east', 'up', 'down']
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
        print '%s says, "%s"' % (self.character.get_name(), msg)
    
        for guest in status.CLIENTS:
            if guest != self.client:
                guest.send('%s says: %s\n' % (self.character.get_name(), msg))
            else:
                guest.send('You say: %s\n' % msg)

    def look(self, args):
        """docstring for look"""
        target_name = args[0] if args else None
        return status.CHARACTERS[self.client].look(target_name)

    def goto(self, args):
        """docstring for goto"""
        if len(args) == 3:
            x, y, map_ = args
        elif len(args) == 2:
            x, y = args
            map_ = self.character.map_name
        else:
            return self.invalid_args()
        try:
            x, y = int(x), int(y)
        except Exception:
            return self.invalid_args()
        return status.CHARACTERS.get(self.client).goto((x, y), map_)

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
        status.CHARACTERS[self.client].go_west()

    def east(self, args):
        """docstring for east"""
        status.CHARACTERS[self.client].go_east()

    def north(self, args):
        """docstring for north"""
        status.CHARACTERS[self.client].go_north()

    def south(self, args):
        """docstring for south"""
        status.CHARACTERS[self.client].go_south()

    def up(self, args):
        """docstring for up"""
        status.CHARACTERS[self.client].go_up()

    def down(self, args):
        """docstring for down"""
        status.CHARACTERS[self.client].go_down()

    def who(self, args):
        """docstring for who"""
        for character in status.CHARACTERS.values():
            self.client.send("%s\n" % repr(character))

    def quit(self, args):
        """docstring for quit"""
        self.client.send('\nSee you next time ! \n')
        status.QUIT_CLIENTS.append(self.client)

    def save(self, args):
        """docstring for save"""
        msg = 'okay.' if  status.CHARACTER_LOADER.dump(status.CHARACTERS[self.client]) else 'fail!'
        self.client.send('%s\n' % (msg))

    def follow(self, args):
        """docstring for follow"""
        target_name = args[0] if len(args) > 0 else None
        room = status.WORLD.locate_client_room(self.client)
        return status.CHARACTERS[self.client].follow(room.get_character_by_name, target_name) \
                if target_name else self.client.send('Huh?\n')

    def track(self, args):
        """docstring for track"""
        target_name = args[0] if len(args) > 0 else None
        room = status.WORLD.locate_client_room(self.client)
        return status.CHARACTERS[self.client].follow(room.get_mob_by_name, target_name) \
                if target_name else self.client.send('Huh?\n')

    def kill(self, args):
        """docstring for kill"""
        target_name = args[0] if len(args) > 0 else None
        return status.CHARACTERS[self.client].kill(target_name) \
                if target_name else self.client.send('Huh?\n')



