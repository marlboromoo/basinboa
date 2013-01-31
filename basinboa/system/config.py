#!/usr/bin/env python
"""
server config.
"""

from basinboa.system.loader import YamlLoader

class Config(object):
    """docstring for Config"""
    def __init__(self, name):
        super(Config, self).__init__()
        self.name = name
        self.items = 0

    def __repr__(self):
        return "Config: %s, items: %s" % \
                (self.name, self.items)
        

class ConfigLoader(YamlLoader):
    """docstring for ConfigLoader"""
    SERVER_CONFIG = 'server'

    def __init__(self, data_dir):
        super(ConfigLoader, self).__init__(data_dir)

    def get(self, name):
        """docstring for get"""
        data = self.load(name)
        if data:
            return self.register_attr(Config(name), data)
        return None
        
    def get_server_config(self):
        """docstring for get"""
        return self.get(self.SERVER_CONFIG)
