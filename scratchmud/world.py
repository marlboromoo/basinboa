#!/usr/bin/env python
"""
world
"""
import os

class Room(object):
    """docstring for Room"""
    def __init__(self):
        super(Room, self).__init__()
        

class Map(object):
    """docstring for Map"""
    MAP_DIR = '../data/map'
    MAP_FILE_EXTENSION = 'map'
    SYMBOL_ROOM = ['*']
    SYMBOL_PATH = ['-', '|', ' ']
    SYMBOL_WE = '-'
    SYNBOL_NS = '|'
    SYNBOL_VOID = ' '

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

    def make_grid(self, map_data, with_symbol=False):
        """docstring for make_grid"""
        grid = []
        id_ = 1
        #. grid
        for line in map_data:
            row = []
            for symbol in line:
                room = {}
                if symbol in self.SYMBOL_ROOM:
                    room['id'] = id_
                    id_ += 1
                    row.append(room)
                if symbol in self.SYMBOL_PATH and with_symbol:
                    row.append(symbol)
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
            xys = []
            x = 0
            for i in row:
                if i not in self.SYMBOL_PATH:
                    xys.append((x, y))
                    x += 1
            if len(xys) > 0:
                coordinate.append(xys)
                y += 1
        return coordinate

    def find_room_in_row(self, row, room_id):
        """docstring for find_room_in_row"""
        i = 0
        for block in row:
            if block not in self.SYMBOL_PATH:
                if block['id'] == room_id:
                    return i
            i += 1

    def make_exit(self, grid, symbol_grid):
        """docstring for make_exit"""
        #exit = [[], [], []]
        y = 0
        for row in grid:
            x = 0
            for room in row:
                index = self.find_room_in_row(symbol_grid[y], room['id'])
                #print index
                symbol_grid[y][index]['exit'] = []
                # process x ..
                if index == 0:
                    #. leftmost room
                    if symbol_grid[y][index+1] in self.SYMBOL_PATH:
                        symbol_grid[y][index]['exit'].append('e')
                elif index == len(symbol_grid[y]) - 1:
                    #. rightmost room
                    if symbol_grid[y][index-1] in self.SYMBOL_PATH:
                        symbol_grid[y][index]['exit'].append('w')
                else:
                    if symbol_grid[y][index-1] in self.SYMBOL_PATH:
                        symbol_grid[y][index]['exit'].append('w')
                    if symbol_grid[y][index+1] in self.SYMBOL_PATH:
                        symbol_grid[y][index]['exit'].append('e')
                #. process y ..
                if y == 0:
                    #. highest room
                    if symbol_grid[y+1][index] in self.SYMBOL_PATH:
                        symbol_grid[y][index]['exit'].append('s')
                elif y == len(symbol_grid) - 1:
                    #. lowest room
                    if symbol_grid[y-1][index] in self.SYMBOL_PATH:
                        symbol_grid[y][index]['exit'].append('n')
                else:
                    if symbol_grid[y+1][index] in self.SYMBOL_PATH:
                        symbol_grid[y][index]['exit'].append('s')
                    if symbol_grid[y-1][index] in self.SYMBOL_PATH:
                        symbol_grid[y][index]['exit'].append('n')
                x += 1
            y += 2 #. line 1,3,5,7 ... is self.SYMBOL_PATH
        return symbol_grid

    def purge_symbol_from_grid(self, symbol_grid):
        """docstring for purge_symbol_from_grid"""
        grid = []
        y = 0
        for row in symbol_grid:
            grid.append([])
            for block in row:
                if block not in self.SYMBOL_PATH:
                    grid[y].append(block)
            y += 1
        return grid

    def make_path(self, grid, symbol_grid, coordinate):
        """docstring for make_path"""
        for xys in coordinate:
            pass

    def check_map(self):
        """docstring for check_map"""
        pass

    def make_map(self, map_data):
        """docstring for make_map"""
        grid = self.make_grid(map_data)
        symbol_grid = self.make_grid(map_data, with_symbol=True)
        exit_grid = self.make_exit(grid, symbol_grid)
        grid = self.purge_symbol_from_grid(exit_grid)
        coordinate = self.make_coordinate(grid)
        print grid, coordinate

if __name__ == '__main__':
    map = Map()
    map.load()
        
        


