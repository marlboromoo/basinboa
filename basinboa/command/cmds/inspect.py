#!/usr/bin/env python
"""
inspect commands.
"""

from basinboa import status
from basinboa.decorator import command
from basinboa.encode import texts_encoder
from basinboa.date import mud_format_time
from basinboa.layout import align_right

@command
def look(client, args):
    """
    see you want to see.
    useage: look [NAME]
    """
    target_name = args[0] if args else None
    character = status.CHARACTERS.get(client)
    room = status.WORLD.locate_client_room(client)
    map_ = status.WORLD.locate_client_map(client)
    if not target_name:
        client.send_cc("%s\n" % (align_right(
            client, 
            msg_right="^KExits: %s^~" % (room.get_exits()),
            msg_left="^C%s, ^c%s.^~" % (map_.get_desc(), mud_format_time()), 
        )))
        #. view
        character.client.send('%s%s\n' % (' '*4, texts_encoder(room.texts)))
        #. other characters
        for client_ in room.get_clients():
            if client_ != character.client:
                character_ = status.CHARACTERS.get(client_)
                character.client.send(texts_encoder("%s(%s) in here.\n" % (character_.nickname, character_.name)))
        #. mobs
        for mob in room.get_mobs():
            character.client.send(texts_encoder("%s(%s) in here.\n" % (mob.nickname, mob.name)))
    else:
        target_character= room.get_character_by_name(target_name)
        if target_character:
            character.client.send("%s\n" % (target_character.get_desc()))
            if not target_character.client == character.client:
                target_character.client.send("%s look at you.\n" % (character.get_name()))
            return
        target_mob = room.get_mob_by_name(target_name)
        if target_mob:
            character.client.send("%s\n" % (target_mob.get_desc()))
            return
        if not target_character and not target_mob:
            client.send('No such target!\n')
