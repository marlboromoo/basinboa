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
    SYMBOL_ROOM = '*'
    SYMBOL_WE = '-'
    SYMBOL_NS = '|'
    SYMBOL_VOID = ' '
    SYMBOL_PATH = [SYMBOL_WE, SYMBOL_NS]
    SYMBOLS = [SYMBOL_WE, SYMBOL_NS, SYMBOL_VOID, SYMBOL_ROOM]
    NORTH = 'n'
    SOUTH = 's'
    EAST = 'e'
    WEST = 'w'

    def __init__(self):
        super(Map, self).__init__()
        self.maps = []

    def list(self):
        """return list of map"""
        maps = os.listdir(self.MAP_DIR)
        leggle_maps = []
        for map_ in maps:
            if map_.split('.')[1] == self.MAP_FILE_EXTENSION:
                leggle_maps.append(map_)
        return leggle_maps

    def load(self):
        """load map files"""
        maps = self.list()
        for map_ in maps:
            map_ = os.path.join(self.MAP_DIR, map_)
            print map_
            with open(map_, 'r') as m:
                map_data = m.readlines()
                self.make_map(map_data)
                print ''.join(map_data)

    def make_grid(self, map_data, with_symbol=False):
        """create grid from map file"""
        grid = []
        id_ = 0
        #. grid
        for line in map_data:
            row = []
            for symbol in line:
                room = {}
                if symbol == self.SYMBOL_ROOM:
                    room['id'] = id_
                    id_ += 1
                    row.append(room)
                if symbol in self.SYMBOLS and symbol != self.SYMBOL_ROOM and with_symbol:
                    row.append(symbol)
            #. check row is leggle
            if len(row) > 0:
                grid.append(row)
        #. debug
        for row in grid:
            print row
        return grid

    def make_coordinates(self, grid):
        """
        create coordinates from grid, gird can't contain symbol of paths
        """
        y = 0
        coordinates = []
        for row in grid:
            #xys = []
            x = 0
            for i in row:
                #xys.append((x, y))
                grid[y][x]['xy'] = (x,y)
                coordinates.append((x,y))
                x += 1
            y += 1
        return grid, coordinates

    def find_room_in_row(self, row, room_id):
        """return x in symbol_grid"""
        i = 0
        for block in row:
            if block not in self.SYMBOL_PATH and block != self.SYMBOL_VOID:
                if block['id'] == room_id:
                    return i
            i += 1

    def make_exits(self, grid, symbol_grid):
        """
        create exits from grid contain symbol of paths
        """
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
                        symbol_grid[y][index]['exits'].append(self.EAST)
                elif index == len(symbol_grid[y]) - 1:
                    #. rightmost room
                    if symbol_grid[y][index-1] in self.SYMBOL_PATH:
                        symbol_grid[y][index]['exits'].append(self.WEST)
                else:
                    if symbol_grid[y][index-1] in self.SYMBOL_PATH:
                        symbol_grid[y][index]['exits'].append(self.WEST)
                    if symbol_grid[y][index+1] in self.SYMBOL_PATH:
                        symbol_grid[y][index]['exits'].append(self.EAST)
                #. process y ..
                if y == 0:
                    #. highest room
                    if symbol_grid[y+1][index] in self.SYMBOL_PATH:
                        symbol_grid[y][index]['exits'].append(self.SOUTH)
                elif y == len(symbol_grid) - 1:
                    #. lowest room
                    if symbol_grid[y-1][index] in self.SYMBOL_PATH:
                        symbol_grid[y][index]['exits'].append(self.NORTH)
                else:
                    if symbol_grid[y+1][index] in self.SYMBOL_PATH:
                        symbol_grid[y][index]['exits'].append(self.SOUTH)
                    if symbol_grid[y-1][index] in self.SYMBOL_PATH:
                        symbol_grid[y][index]['exits'].append(self.NORTH)
                x += 1
            y += 2 #. line 1,3,5,7 ... is self.SYMBOL_PATH
        return symbol_grid

    def purge_symbol_from_grid(self, symbol_grid):
        """purse symbols in grid"""
        grid = []
        for row in symbol_grid:
            row_ = []
            for block in row:
                if block not in self.SYMBOL_PATH and block != self.SYMBOL_VOID:
                    row_.append(block)
            if len(row_) > 0:
                grid.append(row_)
        return grid

    def north_xy(self, x, y):
        """docstring for north_xy"""
        return (x, y-1)

    def south_xy(self, x, y):
        """docstring for south_xy"""
        return (x, y+1)

    def west_xy(self, x, y):
        """docstring for west_xy"""
        return (x-1, y)

    def east_xy(self, x, y):
        """docstring for east_xy"""
        return (x+1, y)

    def make_paths(self, grid):
        """create paths in grid"""
        paths = []
        for row in grid:
            for room in row:
                room['paths'] = []
                x, y = room['xy']
                for exit in room['exits']:
                    if exit == self.EAST:
                        room['paths'].append(self.east_xy(x,y))
                        paths.append(self.east_xy(x,y))
                    if exit == self.WEST:
                        room['paths'].append(self.west_xy(x,y))
                        paths.append(self.west_xy(x,y))
                    if exit == self.NORTH:
                        room['paths'].append(self.north_xy(x,y))
                        paths.append(self.north_xy(x,y))
                    if exit == self.SOUTH:
                        room['paths'].append(self.south_xy(x,y))
                        paths.append(self.south_xy(x,y))
        return grid, paths

    def grid_okay(self, grid):
        """check symbol gird okay"""
        y = 0
        while y < len(grid):
            #. check we
            if grid[y][0] in self.SYMBOL_PATH or grid[y][len(grid[y])-1] in self.SYMBOL_PATH:
                print grid[y][0], grid[y][len(grid[y])-1]
                print 'invalid grid, path not connect to room.'
                return False
            if y == 0 and y == len(grid)-1: 
                for block in grid[y]:
                    if block == self.SYMBOL_NS:
                        print 'invalid grid, path(%s) not connect to room.' % (self.SYMBOL_NS)
                        return False
            y += 2
        return True

    def paths_okay(self, paths, coordinates):
        """docstring for paths_okay"""
        for xy in paths:
            if xy not in coordinates:
                # need log here..
                print "invalid path %s" % (str(xy))
                return False
        return True

    def make_map(self, map_data):
        """create map from map file"""
        #, create gird with coordinates and exits
        symbol_grid = self.make_grid(map_data, with_symbol=True)
        if self.grid_okay(symbol_grid):
            grid = self.make_grid(map_data)
            symbol_grid = self.make_exits(grid, symbol_grid)
            grid = self.purge_symbol_from_grid(symbol_grid)
            print grid
            grid, coordinates = self.make_coordinates(grid)
            #print grid
            #print coordinates
            #. create paths
            grid, paths = self.make_paths(grid)
            print coordinates, paths, grid
            #. check all data is okay
            if self.paths_okay(paths, coordinates):
                #. create objects Room() from grid
                rooms = []
                for row in grid:
                    for room in row:
                        rooms.append(Room(room['id'], room['xy'], room['exits'], room['paths']))
                print rooms

if __name__ == '__main__':
    map = Map()
    map.load()
        
        


