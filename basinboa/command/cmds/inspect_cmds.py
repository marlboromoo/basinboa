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
        player.send_cc_encode("%s\n" % (align_right(
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
                player.send_cc_encode("%s(%s) in here.\n" % (character_.nickname, character_.name))
        #. mobs
        for mob in room.get_mobs():
            player.send_cc_encode("%s(%s) in here.\n" % (mob.nickname, mob.name))
        #. items
        for item in room.get_items():
            player.send_cc_encode("%s(%s) on the floor." % (item.get_nickname(), item.get_name()))
    else:
        player_ = room.get_player_by_name(target_name)
        if player_:
            player.send("%s\n" % (player_.character.get_desc()))
            if not player_ == player:
                player_.send_cc_encode("%s look at you.\n" % (player.character.get_name()))
            return
        mob = room.get_mob_by_name(target_name)
        if mob:
            player.send_cc_encode("%s\n" % (mob.get_desc()))
            return
        item = room.get_item(target_name)
        if item:
            player.send_cc_encode("%s\n" % (item.get_desc()))
            return
        if not all([player_, mob, item]): 
            player.send_cc_encode('No such target!\n')
