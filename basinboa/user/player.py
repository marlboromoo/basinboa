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

    def get_command(self):
        """docstring for get_command"""
        return self.client.get_command()

    def send(self, message):
        """docstring for send"""
        return self.client.send(message)

    def send_cc(self, message):
        """docstring for send_cc"""
        return self.client.send_cc(message)

    def is_player(self):
        """docstring for is_player"""
        return True

    def get_columns(self):
        """docstring for get_ codel"""
        return self.client.columns
