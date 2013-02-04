#!/usr/bin/env python
"""
Equipment system.
"""

from basinboa.universe.item import STYLE_ARMOR, STYLE_WEAPON

SLOT_HEAD = 'head'
SLOT_FACE = 'face'
SLOT_EAR = 'ear'
SLOT_NECK = 'neck'
SLOT_BODY = 'body'
SLOT_ARM = 'arm'
SLOT_LEFTHAND = 'lefthand'
SLOT_RIGHTHAND= 'righthand'
SLOT_LEG = 'leg'
SLOT_FOOT = 'foot'

class Equipment(object):
    """docstring for Equipment"""
    def __init__(self):
        super(Equipment, self).__init__()
        self.head = None
        self.face = None
        self.ear = None
        self.neck = None
        self.body = None
        self.arm = None
        self.lefthand = None
        self.righthand = None
        self.leg = None
        self.foot = None

    def has_equipment(self, item_name):
        """docstring for has_equipment"""
        eqs = self.dump().values()
        if item_name in [eq.name for eq in eqs if eq]:
                return True
        return False

    def pop_equipment(self, item_name):
        """docstring for pop_equipment"""
        for slot,item in self.dump().items():
            if item:
                if item.name == item_name:
                    setattr(self, slot, None)
                    return item
        return None

    def pop_equipment_by_slot(self, slot):
        """docstring for pop_equipment_by_slot"""
        if self._has_slot(slot):
            item = getattr(self, slot)
            setattr(self, slot, None)
            return item
        return None

    def _has_slot(self, slot):
        """docstring for has_slot"""
        return True if hasattr(self, slot) else False

    def _equip(self, item, style):
        """docstring for equip"""
        if item.style == style:
            if self._has_slot(item.slot):
                setattr(self, item.slot, item)
                return True
            else:
                return False
        return False

    def _wield(self, item, auto=True, right=True, twohand=False):
        """docstring for _wield"""
        if twohand:
            self.lefthand = item
            self.righthand = item
            return
        else:
            if auto:
            #. wield weapen with hand that empty, else wield with righthand
                if not self.righthand:
                    self.righthand = item
                    return
                if not self.lefthand:
                    self.lefthand = item
                    return
                if self.lefthand and self.righthand:
                    self.righthand = item
                    return
            else:
                if right:
                    self.righthand = item
                else:
                    self.lefthand = item

    def _remove(self, item):
        """docstring for _remove"""
        setattr(self, item.slot, None)
        return True

    def slot_empty(self, slot):
        """docstring for slot_empty"""
        if hasattr(self, slot):
            return True if not getattr(self, slot) else False
        return False

    def wear(self, item):
        """docstring for wear"""
        return self._equip(item, STYLE_ARMOR)

    def wield(self, item, auto=True, right=True):
        """docstring for wield"""
        if item.style == STYLE_WEAPON:
            self._wield(item, auto=auto, right=right)
            return True
        return False

    def hold(self, item):
        """docstring for hold"""
        if item.style == STYLE_WEAPON:
            self._wield(item, twohand=True)
            return True
        return False

    def remove(self, item):
        """docstring for remove"""
        return self._remove()

    def _get_attr(self, data, attr):
        """docstring for get_attr"""
        if hasattr(self, attr):
            data[attr] = getattr(self, attr)
        return data

    def _set_attr(self, data, attr):
        """docstring for set_attr"""
        if data.has_key(attr):
            setattr(self, attr, data[attr])

    def dump(self):
        """docstring for dump"""
        attrs = [
            'head', 'face', 'ear', 'neck', 
            'body', 'arm', 'lefthand', 'righthand',
            'leg', 'foot',
        ]
        data = {}
        for attr in attrs:
            data = self._get_attr(data, attr)
        return data

    def load(self, data):
        """docstring for load"""
        attrs = [
            'head', 'face', 'ear', 'neck', 
            'body', 'arm', 'lefthand', 'righthand',
            'leg', 'foot',
        ]
        for attr in attrs:
            self._set_attr(data, attr)


        
