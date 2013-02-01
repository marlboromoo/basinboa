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
        self.items = {} #.key is item name, value is Item object
        
    def checkin(self, item):
        """docstring for checkin"""
        if self.burden < self.max_burden:
            self.items[item.get_name()] = item
            return True
        return False

    def checkout(self, item_name):
        """docstring for checkout"""
        if self.items.has_key(item_name):
            return self.items.pop(item_name)
        else:
            return None

    def checkout_all(self):
        """docstring for list_items"""
        items = self.items.values()
        self.remove_items()
        return items

    def remove_items(self):
        """docstring for remove_items"""
        self.items = {}

    def list_items(self):
        """docstring for list"""
        return self.items.values()

    def count_items(self):
        """docstring for count"""
        return len(self.items)

