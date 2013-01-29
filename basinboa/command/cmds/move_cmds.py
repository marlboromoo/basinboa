#!/usr/bin/env python
"""
move commands.
"""
from basinboa import status
from basinboa.decorator import command

@command
def west(player, args):
    """
    go to west.
    useage: west
    alias: w
    """
    player.character.go_west()

@command
def east(player, args):
    """
    go to east.
    useage: east
    alias: e
    """
    player.character.go_east()

@command
def north(player, args):
    """
    go to north.
    useage: north
    alias: n
    """
    player.character.go_north()

@command
def south(player, args):
    """
    go to south.
    useage: sourth.
    alias: s
    """
    player.character.go_south()

@command
def up(player, args):
    """
    go to up.
    useage: up
    alias: u
    """
    player.character.go_up()

@command
def down(player, args):
    """
    go to down.
    useage: down
    alias: d
    """
    player.character.go_down()

def __follow(player, function, name, is_track=False):
    """docstring for _follow"""
    target = function(name)
    if target:
        if target in player.character.get_followers():
            player.send("You can't ! %s already follow you.\n." % (target.name))
            return
        target.add_follower(player.character)
        player.character.start_follow(target)
        name = target.name if target != player else 'yourself'
        action = 'track' if is_track else 'follow'
        player.send("You start to %s %s!\n" % (action, name))
        if target.is_player() and target != player:
            target.send("%s start to follow you!\n" % (player.get_name()))
    else:
        player.send("No such target !\n")

@command
def follow(player, args):
    """
    follow the player.
    useage: follow <PLAYER_NAME>
            follow <YOUR_NAME> to cancle following player.
    """
    target_name = args[0] if len(args) > 0 else None
    room = status.WORLD.locate_player_room(player)
    return __follow(player, room.get_player_by_name, target_name) \
            if target_name else player.send('Huh?\n')

@command
def track(player, args):
    """
    follow the mob.
    useage: follow <MOB_NAME>
            follow <YOUR_NAME> to cancle following mob.
    """
    target_name = args[0] if len(args) > 0 else None
    room = status.WORLD.locate_player_room(player)
    return __follow(player, room.get_mob_by_name, target_name, is_track=True) \
            if target_name else player.send('Huh?\n')


@command
def recall(player, args):
    """docstring for recall"""
    xy = status.SERVER_CONFIG.get('recall_xy')
    map_name = status.SERVER_CONFIG.get('recall_map_name')
    status.WORLD.move_to(player.character, xy, map_name)



