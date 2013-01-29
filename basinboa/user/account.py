#!/usr/bin/env python
"""
user account
"""

class Account(object):
    """docstring for Account"""
    def __init__(self, client):
        super(Account, self).__init__()
        self.client = client
        self.name = None
        self.password = None

    def get_name(self):
        """docstring for get_name"""
        return self.name

    def set_password(self):
        """docstring for set_password"""
        # TODO: write code...
        pass

    def get_password(self):
        """docstring for get_password"""
        return self.password

    def set_email(self):
        """docstring for set_email"""
        # TODO: write code...
        pass

    def get_email(self):
        """docstring for get_email"""
        # TODO: write code...
        pass

    def load(self):
        """docstring for load"""
        # TODO: write code...
        pass

    def dump(self):
        """docstring for dump"""
        # TODO: write code...
        pass


