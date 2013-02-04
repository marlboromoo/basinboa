#!/usr/bin/env python
"""
Bag system.
"""

class Bag(object):
    """docstring for Bag"""
    def __init__(self):
        super(Bag, self).__init__()
        self.max_burden = 100
        self.burden = 0
        self.items = {} #.key is item name, value is list that contain Item objects
        
    def checkin(self, item):
        """docstring for checkin"""
        if self.burden < self.max_burden:
            if self.items.has_key(item.get_name()):
                self.items[item.get_name()].append(item)
            else:
                self.items[item.get_name()] = [item]
            return True
        return False

    def checkout(self, item_name):
        """docstring for checkout"""
        if self.items.has_key(item_name):
            if len(self.items[item_name]) == 1:
                item = self.items.pop(item_name)[0]
            else:
                item = self.items[item_name].pop(0)
            return item
        else:
            return None

    def checkout_all(self):
        """docstring for list_items"""
        items = self.list_items()
        self.remove_items()
        return items

    def remove_items(self):
        """docstring for remove_items"""
        self.items = {}

    def list_items(self):
        """docstring for list"""
        items = []
        for list_ in self.items.values():
            items.extend(list_)
        return items

    def count_items(self):
        """docstring for count"""
        return len(self.list_items())

