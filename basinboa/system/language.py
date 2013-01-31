#!/usr/bin/env python
"""
language system
"""
from basinboa import status
from basinboa.system.loader import YamlLoader
from basinboa.system.config import Config

class Language(Config):
    """docstring for Language"""
    def __init__(self, name, encode):
        super(Language, self).__init__(name)
        self.encode = encode

    def __repr__(self):
        return "Language: %s, encode: %s, items: %s" % \
                (self.name, self.encode, self.items)

    def get_encode(self):
        """docstring for get_encode"""
        return self.encode

class LanguageLoader(YamlLoader):
    """docstring for LanguageLoader"""
    def __init__(self, data_dir):
        super(LanguageLoader, self).__init__(data_dir)

    def get(self, lang=None):
        """docstring for get"""
        lang = lang if lang else status.SERVER_CONFIG.language
        data = self.load(lang)
        if data:
            return self.register_attr(Language(
                name=lang,
                encode=status.SERVER_CONFIG.encode), data)
        return None

