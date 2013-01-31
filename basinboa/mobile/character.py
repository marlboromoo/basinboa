#!/usr/bin/env python
"""
character character
"""
from basinboa import status
from basinboa.system.loader import YamlLoader
from basinboa.mobile.puppet import Puppet

class Character(Puppet):
    """docstring for Character"""
    def __init__(self, name=None):
        super(Character, self).__init__()
        self.name = name
        self.is_mob = False
        self.password = None
        self.role = None
        self.prompt = None
        self.check_location()

    def __repr__(self):
        return "User:%s, role:%s, xy:%s, map:%s" % (
            str(self.name), str(self.role), str(self.xy), str(self.map_name))

    def set_password(self, password):
        """docstring for set_password"""
        self.password = password

    def get_password(self):
        """docstring for get_password"""
        return self.password

    def dump(self):
        """docstring for dump"""
        data = self._dump()
        attrs = ['password', 'role', 'prompt']
        for attr in attrs:
            data = self.get_attr(data, attr)
        return data

    def load(self, data):
        """docstring for load"""
        self._load(data)
        attrs = ['password', 'role', 'prompt']
        for attr in attrs:
            self.set_attr(data, attr)
        self.init_prev_location()

    def check_location(self):
        """docstring for check_location"""
        if not self.xy or not self.map_name:
            self.xy = status.SERVER_CONFIG.recall_xy
            self.map_name = status.SERVER_CONFIG.recall_map_name

class CharacterLoader(YamlLoader):
    """docstring for CharacterLoader"""
    def __init__(self, data_dir):
        super(CharacterLoader, self).__init__(data_dir)
        self.data_dir = data_dir

    def get(self, name):
        """docstring for get"""
        data = self.load(name)
        if data:
            character = Character(data.get(name))
            character.load(data)
            return character
        return None

