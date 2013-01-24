#!/usr/bin/env python
"""
combat system.
"""

from scratchmud import status
from scratchmud.message import mob_message_to_room, character_message_to_room

def fight():
    """docstring for fight"""
    for character in status.CHARACTERS.values():
        if character.get_hp() >= 1:
            for target in character.get_combat_targets():
                #. player hit target
                damage = character.hit(target)
                character.client.send("you hit %s cause damage %s!\n" % (target.get_name(), damage))
                if target.is_player():
                    target.client.send("%s hit you cause damage %s!\n" % (character.get_name(), damage))
                character_message_to_room(character, "%s hit %s cause damage %s!\n" % 
                                          (character.get_name(), target.get_name(), damage))
                #. target hit player
                damage = target.hit(character)
                character.client.send("%s hit you cause damage %s!\n" % (target.get_name(), damage))
                character_message_to_room(character, "%s hit %s cause damage %s!\n" % 
                                          (target.get_name(), character.get_name(), damage))
                #. send prompt
                character.send_prompt()
        else:
            character.client.send_cc('^RYou Dead!^~\n')
            character.increase_hp(1)
            
