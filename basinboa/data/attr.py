#!/usr/bin/env python
"""
functions to set/get, load/dump attribute
"""

from collections import OrderedDict

def set_attr(object_, attr, value):
    """docstring for set_attr"""
    if hasattr(object_, attr):
        setattr(object_, attr, value)
        return True
    return False

def get_attr(object_, attr):
    """docstring for _get_attr"""
    if hasattr(object_, attr):
        return getattr(object_, attr)
    return None

def load(object_, data):
    """docstring for load"""
    for attr in object_.attrs:
        value = data[attr] if data.has_key(attr) else None
        set_attr(object_, attr, value)

def dump(object_):
    """docstring for dump"""
    data = OrderedDict()
    for attr in object_.attrs:
        data[attr] = get_attr(object_, attr)
    return data

