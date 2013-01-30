#!/usr/bin/env python
"""
inspect commands.
"""

from basinboa import status
from basinboa.system.decorator import command
from basinboa.system.encode import texts_encoder
from basinboa.universe.date import mud_format_time
from basinboa.message.layout import align_right

@command
def look(player, args):
    """
    see you want to see.
    useage: look [NAME]
    """
    target_name = args[0] if args else None
    room = status.WORLD.locate_player_room(player)
    map_ = status.WORLD.locate_player_map(player)
    if not target_name:
        player.send_cc("%s\n" % (align_right(
            player, 
            msg_right="^KExits: %s^~" % (room.get_exits()),
            msg_left="^C%s, ^c%s.^~" % (map_.get_desc(), mud_format_time()), 
        )))
        #. view
        player.send('%s%s\n' % (' '*4, texts_encoder(room.texts)))
        #. other characters
        for player_ in room.get_players():
            if player_ != player:
                character_ = player_.character
                player.send(texts_encoder("%s(%s) in here.\n" % (character_.nickname, character_.name)))
        #. mobs
        for mob in room.get_mobs():
            player.send(texts_encoder("%s(%s) in here.\n" % (mob.nickname, mob.name)))
    else:
        player_ = room.get_player_by_name(target_name)
        if player_:
            player.send("%s\n" % (player_.character.get_desc()))
            if not player_ == player:
                player_.send("%s look at you.\n" % (player.character.get_name()))
            return
        mob = room.get_mob_by_name(target_name)
        if mob:
            player.send("%s\n" % (mob.get_desc()))
            return
        if not player_ and not mob:
            player.send('No such target!\n')
