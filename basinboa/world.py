#!/usr/bin/env python
"""
world
"""
import os
import yaml
from basinboa import status

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

class Room(object):
    """docstring for Room"""
    def __init__(self, id_, xy, exits, paths):
        super(Room, self).__init__()
        self.xy = xy
        self.id_ = id_
        self.exits = exits
        self.paths = paths
        self.texts = None
        self.mobs = [] #. Mob objects
        self.players = []
        self.links = [] #. 

    def __repr__(self):
        return "Room%s%s - %s, %s mobs/%s players, links: %s" % (
            str(self.id_), str(self.xy), str('/'.join(self.exits)), 
            str(len(self.mobs)), str(len(self.players)), str(self.links))

    def add_player(self, player):
        """docstring for add_player"""
        self.players.append(player)

    def remove_player(self, player):
        """docstring for remove_player"""
        self.players.remove(player) if player in self.players else None

    def get_players(self):
        """docstring for get_players"""
        return self.players

    def add_mob(self, mob):
        """docstring for add_mob"""
        self.mobs.append(mob)

    def get_mobs(self):
        """docstring for get_mobs"""
        return self.mobs

    def remove_mob(self, mob):
        """docstring for add_client"""
        if mob in self.mobs:
            self.mobs.remove(mob)

    def remove_mobs(self):
        """docstring for remove_mobs"""
        self.mobs = []

    def get_mob_by_name(self, name):
        """return mob object by name else None"""
        for mob in self.mobs:
            if name == mob.name:
                return mob
        return None

    def get_player_by_name(self, name):
        """docstring for get_player_by_name"""
        for player in self.players:
            if player.character.name == name:
                return player
        return None

    def add_link(self, map_, xy, exit):
        """docstring for add_link"""
        if exit in self.exits or self.has_link(exit):
            print "!! Link error, exit: '%s' alreay exist." % (exit)
            return False
        self.links.append({'exit' : exit, 'map' : map_, 'xy' : xy})
        return True

    def remove_link(self, exit):
        """docstring for remove_link"""
        for link in self.links:
            if link['exit'] == exit:
                self.links.remove(link)
                break

    def get_link(self, exit):
        """docstring for get_link"""
        for link in self.links:
            if link['exit'] == exit:
                return link
        return None

    def get_links(self):
        """docstring for get_links"""
        return self.links

    def has_link(self, exit):
        """docstring for has_link"""
        for link in self.links:
            if link['exit'] == exit:
                return True
        return False

    def get_exits(self):
        """docstring for get_exits"""
        if len(self.links) > 0:
            exits = []
            exits.extend(self.exits)
            for link in self.links:
                exits.append(link['exit'])
            return exits
        else:
            return self.exits

class Map(object):
    """docstring for Map"""
    def __init__(self, name, desc, rooms, coordinates):
        super(Map, self).__init__()
        self.name = name
        self.coordinates = coordinates
        self.desc = desc
        self.players = []
        self.init_rooms(rooms) #. key is (x,y), value is Room object
        self.init_mobs()

    def __repr__(self):
        return "Map(%s) - %s rooms/%s mobs/%s players" % (
            str(self.name), str(len(self.rooms)), str(len(self.mobs)), str(len(self.players)))

    def init_rooms(self, rooms):
        """docstring for init_rooms"""
        self.rooms = {}
        for room in rooms:
            self.rooms[room.xy] = room

    def init_mobs(self):
        """docstring for init_mobs"""
        self.mobs = []
        for room in self.rooms.values():
            for mob in room.get_mobs():
                self.mobs.append(mob)

    def get_mobs(self):
        """docstring for get_mobs"""
        return self.mobs

    def add_mob(self, mob):
        """add mob to map"""
        #. add to map
        self.mobs.append(mob)
        #. add to room 
        self.get_room(mob.xy).add_mob(mob)

    def remove_mob(self, mob):
        """remove mob from map"""
        #. remove from room
        room = self.get_room(mob.xy)
        if room:
            room.remove_mob(mob)
        #. remove from map
        self.mobs.remove(mob)

    def get_rooms(self):
        """docstring for get_rooms"""
        return self.rooms.values()

    def get_room(self, xy):
        """docstring for get_room"""
        return self.rooms[xy] if self.rooms.has_key(xy) else None

    def get_name(self):
        """docstring for get_name"""
        return self.name

    def add_player(self, player):
        """docstring for add_player"""
        #. add to map
        self.players.append(player)
        #. add to room
        self.get_room(player.character.xy).add_player(player)

    def remove_player(self, player):
        """docstring for remove_player"""
        if player in self.players:
            #. remove from room
            room = self.get_room(player.character.xy)
            if room:
                room.remove_player(player)
            #. remove from map
            self.players.remove(player)

    def get_players(self):
        """docstring for get_players"""
        return self.players

    def has_coordinates(self, xy):
        """docstring for check_coordinates"""
        return True if xy in self.coordinates else False

    def get_desc(self):
        """docstring for get_desc"""
        return self.desc

class World(object):
    """docstring for World"""
    def __init__(self):
        super(World, self).__init__()
        self.maps = {}

    def add_map(self, map_):
        """docstring for add_map"""
        self.maps[map_.get_name()] = map_

    def get_map(self, map_name):
        """docstring for get_map"""
        return self.maps[map_name] if self.maps.has_key(map_name) else None

    def get_maps(self):
        """docstring for get_maps"""
        return self.maps.values()

    def has_map(self, map_name):
        """docstring for has_map"""
        return True if self.maps.has_key(map_name) else False

    def locate_player_room(self, player):
        """docstring for locate_player_room"""
        return self.get_map(player.character.map_name).get_room(player.character.xy)

    def locate_player_map(self, player):
        """docstring for locate_player_map"""
        return self.get_map(player.character.map_name)

    def locate_mob_room(self, mob):
        """find room by mob object"""
        return self.get_map(mob.map_name).get_room(mob.xy)

    def locate_mob_map(self, mob):
        """find map by mob object"""
        return self.get_map(mob.map_name)

    def check_links(self):
        """check links in whole world."""
        print ">> Checking links in whole world .."
        for map_ in self.get_maps():
            for room in map_.get_rooms():
                for link in room.get_links():
                    if not self.has_map(link['map']):
                        print "!! Invalid link: %s, remove it!" % (str(link))
                        room.remove_link(link['exit'])
                        continue
                    else:
                        if not self.get_map(link['map']).has_coordinates(link['xy']):
                            print "!! Invalid link: %s, remove it!" % (str(link))
                            room.remove_link(link['exit'])
                            continue

    def move_character(self, character, symbol, function):
        """move character object between rooms if rooms connected"""
        player = status.PLAYERS[character.name]
        src_room = self.locate_player_room(player)
        x, y = character.xy
        #. check n,s,w,e
        if symbol in src_room.exits:
            dst_xy = function(x, y)
            if dst_xy in src_room.paths:
                #. move character to room
                character.set_prev_location(character.xy, character.map_name)
                character.xy = dst_xy
                #. remove character from source room
                src_room.remove_player(player)
                #. add character to target room
                dst_room = self.locate_player_room(player)
                dst_room.add_player(player)
                return (src_room, dst_room)
        #. check link
        elif src_room.has_link(symbol):
            link = src_room.get_link(symbol)
            return self.move_character_to(character, link['xy'], link['map'])
        else:
            return (None, None)

    def move_mob(self, mob, symbol, function):
        """move mob object between rooms if rooms connected"""
        src_room = self.locate_mob_room(mob)
        x, y = mob.xy
        #. check n,s,w,e
        if symbol in src_room.exits:
            dst_xy = function(x, y)
            if dst_xy in src_room.paths:
                #. move mob to room
                mob.set_prev_location(mob.xy, mob.map_name)
                mob.xy = dst_xy
                #. remove mob from source room
                src_room.remove_mob(mob)
                #. add mob to target room
                dst_room = self.locate_mob_room(mob)
                dst_room.add_mob(mob)
                return (src_room, dst_room)
        #. check link
        elif src_room.has_link(symbol):
            link = src_room.get_link(symbol)
            return self.move_mob_to(mob, link['xy'], link['map'])
        else:
            return (None, None)


    def move_character_to(self, character, xy, map_name):
        """move character object between rooms even if rooms not connected"""
        try:
            dst_map = self.get_map(map_name)
            dst_room = dst_map.get_room(xy)
        except Exception:
            dst_map, dst_room = None, None
        if dst_map and dst_room:
            # remove character from origin map & room
            player = status.PLAYERS[character.name]
            src_map = self.locate_player_map(player)
            src_room = src_map.get_room(character.xy)
            src_map.remove_player(player)
            #. move character to destation
            character.set_prev_location(character.xy, character.map_name)
            character.set_location(xy, dst_map.get_name())
            dst_map.add_player(player)
            #return((src_map, src_room), (dst_map, dst_room))
            return (src_room, dst_room)
        else:
            #return ((None, None), (None, None))
            return (None, None)

    def move_mob_to(self, mob, xy, map_name):
        """move mob object between rooms even if rooms not connected"""
        try:
            dst_map = self.get_map(map_name)
            dst_room = dst_map.get_room(xy)
        except Exception:
            dst_map, dst_room = None, None
        if dst_map and dst_room:
            # remove mob from origin map & room
            src_map = self.locate_mob_map(mob)
            src_room = src_map.get_room(mob.xy)
            src_map.remove_mob(mob)
            #. move mob to destation
            mob.set_prev_location(mob.xy, mob.map_name)
            mob.set_location(xy, dst_map.get_name())
            dst_map.add_mob(mob)
            #return((src_map, src_room), (dst_map, dst_room))
            return (src_room, dst_room)
        else:
            #return ((None, None), (None, None))
            return (None, None)

    def remove_player(self, player):
        """docstring for remove_client"""
        for map_ in self.get_maps():
            map_.remove_player(player)


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

