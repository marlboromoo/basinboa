#!/usr/bin/env python
"""
represent a login client.
"""
from basinboa import status
from basinboa.user.account import Account
from basinboa.user.role import ROLE_ADMIN 
from basinboa.system.encode import texts_encoder

class Player(Account):
    """docstring for Player"""
    def __init__(self, client, character):
        super(Player, self).__init__(client)
        self.character = character
        self.name = character.name
        self.password = character.password
        self.prompt = character.prompt
        self.role = character.role

    def is_admin(self):
        """docstring for is_admin"""
        return True if self.get_role() == ROLE_ADMIN else False

    def set_name(self, name):
        """docstring for set_name"""
        self.name = name
        self.character.name = name

    def get_name(self):
        """docstring for get_name"""
        return self.name

    def set_password(self, password):
        """docstring for set_password"""
        self.password = password
        self.character.password = password

    def get_password(self):
        """docstring for get_password"""
        return self.password

    def set_role(self, role):
        """docstring for set_role"""
        self.role = role
        self.character.role = role

    def get_role(self):
        """docstring for get_role"""
        return self.role

    def get_command(self):
        """shortcut of self.client.get_command()"""
        return self.client.get_command()

    def send(self, msg):
        """shortcut of self.client.send()"""
        return self.client.send(msg)

    def send_cc(self, msg):
        """shortcut of self.client.send_cc()"""
        return self.client.send_cc("%s^~" % msg)

    def is_player(self):
        """docstring for is_player"""
        return True

    def get_columns(self):
        """shortcut of self.client.columns"""
        return self.client.columns

    def idle(self):
        """shortcut of self.client.idle()"""
        return self.client.idle()

    def addrport(self):
        """shortcut of self.client.addrport()"""
        return self.client.addrport()

    def deactivate(self):
        """shortcut of self.client.deactivate"""
        self.client.deactivate()

    def send_encode(self, msg):
        """docstring for send"""
        return self.client.send(texts_encoder(msg))

    def send_cc_encode(self, msg):
        """docstring for send"""
        return self.client.send_cc("%s^~" % texts_encoder(msg))

    def get_prompt(self, room=None):
        """docstring for get_prompt"""
        prompt = '\n(^w'
        hp, mhp = self.character.get_hp()
        mp, mmp = self.character.get_mp()
        prompt += "HP:%s/%s, MP:%s/%s, EXP:%s, COINS:%s" % (hp, mhp, mp, mmp, 0, 0)
        if self.is_admin():
            room = status.WORLD.locate_player_room(self) if room == None else room
            mobs = [mob.get_name() for mob in room.get_mobs()]
            prompt += "ID: %s, XY: %s MOBS: %s)\n> ^~" % (room.id_, str(room.xy), str(mobs))
        else:
            prompt += ")\n> ^~"
        return prompt


