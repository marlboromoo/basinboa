#!/usr/bin/env python
"""
combat system.
"""

from scratchmud import status
from scratchmud.message import mob_message_to_room, character_message_to_room

def fight():
    """docstring for fight"""
    for character in status.CHARACTERS.values():
        for target in character.get_combat_targets():
            #. player hit target
            character.hurt(target)
            character.client.send("you hit %s cause damage %s!\n" % (target.get_name(), '10'))
            if target.is_player():
                target.client.send("%s hit you cause damage %s!\n" % (character.get_name(), '10'))
            character_message_to_room(character, "%s hit %s cause damage %s!\n" % 
                                      (character.get_name(), target.get_name(), '10'))
            #. target hit player
            target.hurt(character)
            character.client.send("%s hit you cause damage %s!\n" % (target.get_name(), '10'))
            character_message_to_room(character, "%s hit %s cause damage %s!\n" % 
                                      (target.get_name(), character.get_name(), '10'))
            #. send prompt
            character.send_prompt()
            
