#!/usr/bin/env python
"""
items.
"""
import copy
from basinboa.system.uid import Uid
from basinboa.system.loader import YamlLoader

STYLE_BAG = 'bag'
STYLE_WEAPON = 'weapon'
STYLE_ARMOR = 'armor'
STYLE_LIQUID = 'liquid'
STYLE_FOOD = 'food'
STYLE_KEY = 'key'
STYLE_TOOL = 'tool'

class Item(Uid):
    """docstring for Item"""
    def __init__(self, data):
        super(Item, self).__init__()
        self.name = None
        self.nickname = None
        self.desc = None
        self.style = None
        self.slot = None
        self.dropable = None
        self.getable = None
        #. values
        self.weight = 0
        self.value = 0 #. coin/gold ?
        self.duration = 0
        self.damage = 0
        #. extra status
        self.skills = None
        self.spells = None
        self.status = None
        #. geography
        self.xy = None
        self.map_name = None
        #. init
        self.load(data)

    def __repr__(self):
        """docstring for __repr__"""
        return "Item: %s(%s), style:%s, slot:%s" % (
            self.nickname, self.name, self.style, self.slot
        )

    def get_name(self):
        """docstring for get_name"""
        return self.name

    def get_nickname(self):
        """docstring for get_nickname"""
        return self.nickname

    def get_desc(self):
        """docstring for get_desc"""
        return self.desc

    def get_attr(self, data, attr):
        """docstring for get_attr"""
        if hasattr(self, attr):
            data[attr] = getattr(self, attr)
        return data

    def set_attr(self, data, attr):
        """docstring for set_attr"""
        if data.has_key(attr):
            setattr(self, attr, data[attr])

    def dump(self):
        """docstring for dump"""
        attrs = [
            'name', 'nickname', 'desc', 'style', 'slot', 'dropable', 'getable',
            #. values
            'weight', 'value', 'duration', 'damage',
            #. extra status
            'skills', 'spells', 'status',
            #. geography
            'xy', 'map_name',
        ]
        data = {}
        for attr in attrs:
            data = self.get_attr(data, attr)
        return data

    def load(self, data):
        """docstring for load"""
        attrs = [
            'name', 'nickname', 'desc', 'style', 'slot', 'dropable', 'getable',
            #. values
            'weight', 'value', 'duration', 'damage',
            #. extra status
            'skills', 'spells', 'status',
            #. geography
            'xy', 'map_name',
        ]
        for attr in attrs:
            self.set_attr(data, attr)

#------------------------------------------------------------------------------
#       ability
#------------------------------------------------------------------------------

    def can_wear(self):
        """docstring for can_wear"""
        pass

    def can_hold(self):
        """docstring for can_hold"""
        pass

    def can_sell(self):
        """docstring for can_sell"""
        pass

    def can_get(self):
        """docstring for can_get"""
        pass

    def can_drop(self):
        """docstring for can_drop"""
        pass

    def can_craft(self):
        """docstring for can_craft"""
        pass

    def can_repair(self):
        """docstring for can_repair"""
        pass

    def can_drink(self):
        """docstring for can_drink"""
        pass

    def can_eat(self):
        """docstring for can_eat"""
        pass

    def can_checkin(self):
        """docstring for can_checkin"""
        pass

    def can_checkout(self):
        """docstring for can_checkout"""
        pass

#------------------------------------------------------------------------------
#       Event
#------------------------------------------------------------------------------
        
        def on_wear(self):
            """docstring for on_wear"""
            pass

class ItemLoader(YamlLoader):
    """docstring for ItemLoader"""
    def __init__(self, data_dir):
        super(ItemLoader, self).__init__(data_dir)
        self.items = {}
        self.load_items()
        
    def load_items(self):
        """docstring for load_skeletons"""
        datas = self.load_all()
        for data in datas:
            self.items[data.get('name')] = Item(data)

    def get(self, name):
        """docstring for get"""
        if self.items.has_key(name):
            item = copy.deepcopy(self.items.get(name))
            item.renew_uuid()
            return item

    def get_all(self):
        """docstring for get_items"""
        return self.items.values()

