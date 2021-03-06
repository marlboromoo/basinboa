#!/usr/bin/env python
"""
data loader of universe.
"""
import os
import yaml
from basinboa import status
from basinboa.universe.room import Room
from basinboa.universe.map import Map
from basinboa.universe.world import World
from basinboa.universe.direction import north_xy, south_xy, west_xy, east_xy, NORTH, SOUTH, EAST, WEST

class WorldLoader(object):
    """docstring for WorldLoader"""
    MAP_DATA_EXTENSION = 'map'
    MAP_CONFIG_EXTENSION= 'yml'
    SYMBOL_ROOM = '*'
    SYMBOL_WE = '-'
    SYMBOL_NS = '|'
    SYMBOL_VOID = ' '
    SYMBOL_PATHS = [SYMBOL_WE, SYMBOL_NS]
    SYMBOLS = [SYMBOL_WE, SYMBOL_NS, SYMBOL_VOID, SYMBOL_ROOM]

    def __init__(self, map_dir):
        super(WorldLoader, self).__init__()
        self.map_dir = map_dir
        self.world = World()

    def list(self):
        """return list of *.map"""
        maps = os.listdir(self.map_dir)
        leggle_maps = []
        for map_ in maps:
            if map_.split('.')[1] == self.MAP_DATA_EXTENSION:
                leggle_maps.append(map_.split('.')[0])
        return leggle_maps

    def load(self, map_name):
        """load map by name"""
        config_path = os.path.join(self.map_dir, "%s.%s" % (map_name, self.MAP_CONFIG_EXTENSION))
        data_path = os.path.join(self.map_dir, "%s.%s" % (map_name, self.MAP_DATA_EXTENSION))
        #print config_path, data_path
        if all([os.path.exists(config_path), os.path.exists(data_path)]):
            #. load data
            with open(data_path, 'r') as f:
                map_data = f.readlines()
                rooms, coordinates = self.make_rooms(map_data)
                #print ''.join(map_data)
            #. load config
            with open(config_path, 'r') as f:
                map_config = yaml.load(f, Loader=yaml.Loader)
            if rooms:
                #. init room data
                self.inject_texts_to_rooms(rooms, map_config)
                self.inject_mobs_to_rooms(rooms, map_config)
                self.inject_links_to_rooms(rooms, map_config)
                #. create Map() object
                self.world.add_map(Map(
                    name=map_config['name'], desc=map_config['desc'],
                    rooms=rooms, coordinates=coordinates))
            else:
                print "!! Map %s process error! " % (map_name)

    def load_all(self):
        """docstring for load_all"""
        print ">> Loading all maps .."
        maps = self.list()
        #print maps
        for map_ in maps:
            self.load(map_)

    def get(self):
        """docstring for get"""
        return self.world

    def make_symbol_grid(self, map_data, replace_room_with_id=False):
        """docstring for make_symbol_grid"""
        grid = []
        id_ = 0
        #. grid
        for line in map_data:
            row = []
            for symbol in line:
                if symbol == self.SYMBOL_ROOM:
                    block = {}
                    block['id'] = id_
                    id_ += 1
                    row.append(block) if replace_room_with_id else row.append(symbol)
                else:
                    if symbol in self.SYMBOLS:
                        row.append(symbol)
            if len(row) != 0:
                grid.append(row)
        #. debug
        #for row in grid:
        #    print row
        return grid

    def make_id_grid(self, map_data):
        """docstring for make_id_grid"""
        grid = []
        id_ = 0
        #. grid
        y = 0
        for line in map_data:
            if y % 2 == 0:
                row = []
                for symbol in line:
                    block = {}
                    if symbol == self.SYMBOL_ROOM:
                        block['id'] = id_
                        id_ += 1
                        row.append(block)
                    else:
                        if symbol in self.SYMBOLS:
                            row.append(None)
                #. check row not empty
                if len(row) > 0:
                    grid.append(row)
            y += 1
        #. debug
        #for row in grid:
        #    print row
        return grid

    def make_coordinates(self, grid):
        """
        create coordinates from grid, gird can't contain symbol of paths
        """
        y = 0
        coordinates = []
        for row in grid:
            x = 0
            for block in row:
                if block:
                    grid[y][x]['xy'] = (x,y)
                    coordinates.append((x,y))
                x += 1
            y += 1
        return grid, coordinates

    def find_room_in_row(self, row, room_id):
        """return x in symbol_grid"""
        i = 0
        for block in row:
            if block not in self.SYMBOL_PATHS and block != self.SYMBOL_VOID:
                if block['id'] == room_id:
                    return i
            i += 1

    def make_exits(self, grid, symbol_grid):
        """
        create exits from grid contain symbol of paths
        """
        y = 0
        for row in grid:
            x = 0
            for block in [block for block in row if block]:
                index = self.find_room_in_row(symbol_grid[y], block['id'])
                symbol_grid[y][index]['exits'] = []
                try:
                    # process x ..
                    if index == 0:
                        #. leftmost block
                        if symbol_grid[y][index+1] in self.SYMBOL_PATHS:
                            symbol_grid[y][index]['exits'].append(EAST)
                    elif index == len(symbol_grid[y]) - 1:
                        #. rightmost block
                        if symbol_grid[y][index-1] in self.SYMBOL_PATHS:
                            symbol_grid[y][index]['exits'].append(WEST)
                    else:
                        if symbol_grid[y][index-1] in self.SYMBOL_PATHS:
                            symbol_grid[y][index]['exits'].append(WEST)
                        if symbol_grid[y][index+1] in self.SYMBOL_PATHS:
                            symbol_grid[y][index]['exits'].append(EAST)
                    #. process y ..
                    if y == 0:
                        #. highest block
                        if symbol_grid[y+1][index] in self.SYMBOL_PATHS:
                            symbol_grid[y][index]['exits'].append(SOUTH)
                    elif y == len(symbol_grid) - 1:
                        #. lowest block
                        if symbol_grid[y-1][index] in self.SYMBOL_PATHS:
                            symbol_grid[y][index]['exits'].append(NORTH)
                    else:
                        if symbol_grid[y+1][index] in self.SYMBOL_PATHS:
                            symbol_grid[y][index]['exits'].append(SOUTH)
                        if symbol_grid[y-1][index] in self.SYMBOL_PATHS:
                            symbol_grid[y][index]['exits'].append(NORTH)
                except Exception:
                    pass
                x += 1
            y += 2 #. line 1,3,5,7 ... is self.SYMBOL_PATHS
        return symbol_grid

    def purge_symbol_from_grid(self, symbol_grid):
        """purse symbols in grid"""
        grid = []
        y = 0
        for row in symbol_grid:
            #. room only at 0 2 4 6 .. in y
            if y % 2 == 0:
                row_ = []
                x = 0
                for block in row:
                    if block not in self.SYMBOLS:
                        row_.append(block)
                    #. room must be 0 2 4 6 .. in x
                    if block == self.SYMBOL_VOID and x % 2 == 0:
                        #print x
                        row_.append(None)
                    x += 1
                if len(row_) > 0:
                    grid.append(row_)
            y += 1
        return grid

    def make_paths(self, grid):
        """create paths in grid"""
        paths = []
        for row in grid:
            for block in [block for block in row if block]:
                block['paths'] = []
                x, y = block['xy']
                for exit in block['exits']:
                    if exit == EAST:
                        block['paths'].append(east_xy(x,y))
                        paths.append(east_xy(x,y))
                    if exit == WEST:
                        block['paths'].append(west_xy(x,y))
                        paths.append(west_xy(x,y))
                    if exit == NORTH:
                        block['paths'].append(north_xy(x,y))
                        paths.append(north_xy(x,y))
                    if exit == SOUTH:
                        block['paths'].append(south_xy(x,y))
                        paths.append(south_xy(x,y))
        return grid, paths

    def _grid_okay(self, grid):
        """check symbol gird okay"""
        y = 0
        while y < len(grid):
            #. check we
            if grid[y][0] in self.SYMBOL_PATHS or grid[y][len(grid[y])-1] in self.SYMBOL_PATHS:
                #print grid[y][0], grid[y][len(grid[y])-1]
                print '!! Invalid grid, path not connect to room.'
                return False
            if y == 0 and y == len(grid)-1: 
                for block in grid[y]:
                    if block == self.SYMBOL_NS:
                        print '!! Invalid grid, path(%s) not connect to room.' % (self.SYMBOL_NS)
                        return False
            y += 2
        return True

    def symbol_must_be_room(self, symbol, xy, allow_void=False, notice=True):
        """docstring for symbol_must_be_room"""
        x, y = xy
        if symbol != self.SYMBOL_ROOM and not allow_void:
            if notice:
                print "!! Invalid grid, block(%s, %s) '%s' must be '%s'." % (
                    x, y, symbol, self.SYMBOL_ROOM
                )
            return False
        if symbol != self.SYMBOL_ROOM and symbol != self.SYMBOL_VOID and allow_void:
            if notice:
                print "!! Invalid grid, block(%s, %s) '%s' must be '%s' or '%s'." % (
                    x, y, symbol, self.SYMBOL_ROOM, self.SYMBOL_VOID
                )
            return False
        return True

    def symbol_must_be_path(self, symbol, xy):
        """docstring for symbol_must_be_path"""
        x, y = xy
        if symbol not in self.SYMBOL_PATHS and symbol != self.SYMBOL_VOID: 
            print "!! Invalid grid, block(%s, %s) '%s' must be '%s' or follow one: '%s'." % (
                x, y, symbol, self.SYMBOL_VOID, "' '".join(self.SYMBOL_PATHS)
            )
            return False
        return True

    def symbol_rule_x(self, symbol, xy):
        """docstring for symbol_rule_x"""
        x, y = xy
        if x % 2 == 0:
            #. 0, 2, 4, 6 ... must be room or void in x
            return self.symbol_must_be_room(symbol, xy, allow_void=True)
        else:
            #. 1, 3, 5, 7 ... must be path in x
            return self.symbol_must_be_path(symbol, xy)

    def symbol_row_rule_x(self, row, y):
        """docstring for symbol_row_rule_x"""
        row = [symbol for symbol in row if symbol != self.SYMBOL_VOID]
        #print 'row:', row
        if not self.symbol_must_be_room(row[0], (0,y), notice=False) or \
           not self.symbol_must_be_room(row[len(row)-1], (len(row)-1,y), notice=False):
            print "!! Invalid grid, first/last symbol of row%s must be '%s'" % (
                y, self.SYMBOL_ROOM
            )
            return False
        return True

    def grid_okay(self, symbol_grid):
        """docstring for grid_okay"""
        y=0
        for row in symbol_grid:
            x = 0
            #. check row
            if y % 2 ==0:
                if not self.symbol_row_rule_x(row, y):
                    return False
            #. check symbol
            for block in row:
                #. 0, 2, 4, 6 ... must be room or path in y
                if y % 2 == 0:
                    if not self.symbol_rule_x(block, (x,y)):
                        return False
                # 1, 3, 5, 7 ... must be path in y
                else:
                    if not self.symbol_must_be_path(block, (x,y)):
                        return False
                x += 1
            y += 1
        return True


    def paths_okay(self, paths, coordinates):
        """docstring for paths_okay"""
        for xy in paths:
            if xy not in coordinates:
                # need log here..
                print "!! invalid path %s, please check your map data." % (str(xy))
                return False
        return True

    def make_rooms(self, map_data):
        """create map from map file"""
        #, create gird with coordinates and exits
        if self.grid_okay(self.make_symbol_grid(map_data)):
            symbol_grid = self.make_symbol_grid(map_data, replace_room_with_id=True)
            id_grid = self.make_id_grid(map_data)
            symbol_grid = self.make_exits(id_grid, symbol_grid)
            grid = self.purge_symbol_from_grid(symbol_grid)
            grid, coordinates = self.make_coordinates(grid)
            grid, paths = self.make_paths(grid)
            #. check all data is okay
            if self.paths_okay(paths, coordinates):
                #. create objects Room() from grid
                rooms = []
                for row in grid:
                    for block in [block for block in row if block]:
                        rooms.append(Room(block['id'], block['xy'], block['exits'], block['paths']))
                return rooms, coordinates
        return None, None

    def inject_texts_to_rooms(self, rooms, map_config):
        """docstring for inject_texts_to_rooms"""
        texts = [room['texts'] for room in map_config['rooms']]
        i = 0
        for room in rooms:
            room.texts = texts[i]
            i += 1

    def inject_mobs_to_rooms(self, rooms, map_config):
        """docstring for inject_mobs_to_rooms"""
        i = 0
        for room in rooms:
            mobs = map_config['rooms'][i]['mobs']
            if mobs:
                for mob in mobs:
                    mob_ = status.MOB_LOADER.get(mob.get('skeleton'))
                    mob_.name = mob.get('name') if mob.has_key('name') else mob_.name
                    mob_.nickname = mob.get('nickname') if mob.has_key('nickname') else mob_.nickname
                    mob_.desc = mob.get('desc') if mob.has_key('desc') else mob_.desc
                    mob_.gossip = mob.get('gossip') if mob.has_key('gossip') else mob_.gossip
                    mob_.xy = room.xy
                    mob_.map_name = map_config['name']
                    room.add_mob(mob_)
            i += 1

    def inject_links_to_rooms(self, rooms, map_config):
        """docstring for inject_links_to_rooms"""
        i = 0
        for room in rooms:
            try:
                links = map_config['rooms'][i]['links']
            except Exception:
                links = None
            if links:
                for link in links:
                    try:
                        map_ = link['map']
                        xy = link['xy']
                        exit = link['exit']
                    except Exception:
                        print "!! Link error, missing values 'map' or 'xy' or 'exit'."
                        continue
                    #. TODO: check map or xy exist
                    room.add_link(map_, xy, exit)
            i += 1

