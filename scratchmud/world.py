#!/usr/bin/env python
"""
world
"""
import os

class Map(object):
    """docstring for Map"""
    MAP_DIR = '../data/map'
    MAP_FILE_EXTENSION = 'map'
    SYMBOL_ROOM = ['*']
    SYMBOL_PATH = ['-', '|', ' ']

    def __init__(self):
        super(Map, self).__init__()

    def list(self):
        """docstring for list"""
        maps = os.listdir(self.MAP_DIR)
        leggle_maps = []
        for map_ in maps:
            if map_.split('.')[1] == self.MAP_FILE_EXTENSION:
                leggle_maps.append(map_)
        return leggle_maps

    def load(self):
        """docstring for load"""
        maps = self.list()
        for map_ in maps:
            map_ = os.path.join(self.MAP_DIR, map_)
            print map_
            with open(map_, 'r') as m:
                map_data = m.readlines()
                self.make_map(map_data)
                print ''.join(map_data)

    def make_grid(self, map_data):
        """docstring for make_grid"""
        grid = []
        id_ = 1
        #. grid
        for line in map_data:
            row = []
            for symbol in line:
                if symbol in self.SYMBOL_ROOM:
                    row.append(id_)
                    id_ += 1
            #. check row is leggle
            if len(row) > 0:
                grid.append(row)
        for line in grid:
            print line
        return grid

    def make_coordinate(self, grid):
        """docstring for make_coordinate"""
        y = 0
        coordinate = []
        for row in grid:
            xy = []
            x = 0
            for i in row:
                if i not in self.SYMBOL_PATH:
                    xy.append((x, y))
                    x += 1
            coordinate.append(xy)
            y += 1
        for line in coordinate:
            print line
        return coordinate

    def make_path(self, map_data, grid, coordinate):
        """docstring for make_path"""
        pass

    def make_map(self, map_data):
        """docstring for make_map"""
        grid = self.make_grid(map_data)
        coordinate = self.make_coordinate(grid)
        path = self.make_path(map_data, grid, coordinate)
        return path

if __name__ == '__main__':
    map = Map()
    map.load()
        
        


