#!/usr/bin/env python
"""
world
"""
import os

class Room(object):
    """docstring for Room"""
    def __init__(self, id_, xy, exits, paths):
        super(Room, self).__init__()
        self.xy = xy
        self.id_ = id_
        self.exits = exits
        self.paths = paths
        self.texts = None
    def __repr__(self):
        return "Room%s%s - %s,  " % (str(self.id_), str(self.xy), str('/'.join(self.exits)))

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
        self.maps = []

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
        id_ = 0
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
        return grid

    def make_coordinate(self, grid):
        """docstring for make_coordinate"""
        y = 0
        coordinate = []
        for row in grid:
            xys = []
            x = 0
            for i in row:
                xys.append((x, y))
                grid[y][x]['xy'] = (x,y)
                x += 1
            coordinate.append(xys)
            y += 1
        return grid, coordinate

    def find_room_in_row(self, row, room_id):
        """docstring for find_room_in_row"""
        i = 0
        for block in row:
            if block not in self.SYMBOL_PATH:
                if block['id'] == room_id:
                    return i
            i += 1

    def make_exits(self, grid, symbol_grid):
        """docstring for make_exits"""
        #exit = [[], [], []]
        y = 0
        for row in grid:
            x = 0
            for room in row:
                index = self.find_room_in_row(symbol_grid[y], room['id'])
                #print index
                symbol_grid[y][index]['exits'] = []
                # process x ..
                if index == 0:
                    #. leftmost room
                    if symbol_grid[y][index+1] in self.SYMBOL_PATH:
                        symbol_grid[y][index]['exits'].append('e')
                elif index == len(symbol_grid[y]) - 1:
                    #. rightmost room
                    if symbol_grid[y][index-1] in self.SYMBOL_PATH:
                        symbol_grid[y][index]['exits'].append('w')
                else:
                    if symbol_grid[y][index-1] in self.SYMBOL_PATH:
                        symbol_grid[y][index]['exits'].append('w')
                    if symbol_grid[y][index+1] in self.SYMBOL_PATH:
                        symbol_grid[y][index]['exits'].append('e')
                #. process y ..
                if y == 0:
                    #. highest room
                    if symbol_grid[y+1][index] in self.SYMBOL_PATH:
                        symbol_grid[y][index]['exits'].append('s')
                elif y == len(symbol_grid) - 1:
                    #. lowest room
                    if symbol_grid[y-1][index] in self.SYMBOL_PATH:
                        symbol_grid[y][index]['exits'].append('n')
                else:
                    if symbol_grid[y+1][index] in self.SYMBOL_PATH:
                        symbol_grid[y][index]['exits'].append('s')
                    if symbol_grid[y-1][index] in self.SYMBOL_PATH:
                        symbol_grid[y][index]['exits'].append('n')
                x += 1
            y += 2 #. line 1,3,5,7 ... is self.SYMBOL_PATH
        return symbol_grid

    def purge_symbol_from_grid(self, symbol_grid):
        """docstring for purge_symbol_from_grid"""
        grid = []
        for row in symbol_grid:
            row_ = []
            for block in row:
                if block not in self.SYMBOL_PATH:
                    row_.append(block)
            if len(row_) > 0:
                grid.append(row_)
        return grid

    def make_path(self, grid, symbol_grid, coordinate):
        """docstring for make_path"""
        pass

    def check_grid(self):
        """docstring for check_grid"""
        # TODO: write code...
        pass

    def make_map(self, map_data):
        """docstring for make_map"""
        #, create gird with coordinate and exits
        grid = self.make_grid(map_data)
        symbol_grid = self.make_grid(map_data, with_symbol=True)
        symbol_grid = self.make_exits(grid, symbol_grid)
        grid = self.purge_symbol_from_grid(symbol_grid)
        grid, coordinate = self.make_coordinate(grid)
        #print grid
        #. create objects Room() from grid
        rooms = []
        for row in grid:
            for room in row:
                room['paths'] = None
                rooms.append(Room(room['id'], room['xy'], room['exits'], room['paths']))
        print rooms

if __name__ == '__main__':
    map = Map()
    map.load()
        
        


