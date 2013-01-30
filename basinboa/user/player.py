#!/usr/bin/env python
"""
represent a login client.
"""
from basinboa.user.account import Account

class Player(Account):
    """docstring for Player"""
    def __init__(self, client, character):
        super(Player, self).__init__(client)
        self.character = character
        self.name = character.name

    def get_name(self):
        """docstring for get_name"""
        return self.name

    def get_command(self):
        """shortcut of self.client.get_command()"""
        return self.client.get_command()

    def send(self, message):
        """shortcut of self.client.send()"""
        return self.client.send(message)

    def send_cc(self, message):
        """shortcut of self.client.send_cc()"""
        return self.client.send_cc(message)

    def is_player(self):
        """docstring for is_player"""
        return True

    def get_columns(self):
        """shortcut of self.client.columns"""
        return self.client.columns

    def idle(self):
        """shortcut of self.client.idle()"""
        return self.client.idle()

    def addport(self):
        """shortcut of self.client.addport()"""
        return self.client.addport()
