#!/usr/bin/env python
"""
direction define
"""

NORTH = 'n'
SOUTH = 's'
EAST = 'e'
WEST = 'w'
UP = 'u'
DOWN = 'd'
NORTH_NAME = 'north'
SOUTH_NAME = 'south'
WEST_NAME = 'west'
EAST_NAME = 'east'
UP_NAME = 'up'
DOWN_NAME = 'down'

def exit_name(symbol):
    """docstring for exit_message"""
    if symbol == NORTH:
        return NORTH_NAME
    if symbol == SOUTH:
        return SOUTH_NAME
    if symbol == WEST:
        return WEST_NAME
    if symbol == EAST:
        return EAST_NAME
    if symbol == UP:
        return UP_NAME
    if symbol == DOWN:
        return DOWN_NAME

def north_xy(x, y):
    """docstring for north_xy"""
    return (x, y-1)

def south_xy(x, y):
    """docstring for south_xy"""
    return (x, y+1)

def west_xy(x, y):
    """docstring for west_xy"""
    return (x-1, y)

def east_xy(x, y):
    """docstring for east_xy"""
    return (x+1, y)
