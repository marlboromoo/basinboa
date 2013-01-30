#!/usr/bin/env python
"""
fight.
"""

from basinboa import status
from basinboa.message.broadcast import player_message_to_room

def fight():
    """docstring for fight"""
    for player in status.PLAYERS.values():
        character = player.character
        if character.get_hp() >= 1:
            for target in character.get_combat_targets():
                #. player hit target
                damage = character.hit(target)
                player.send("you hit %s cause damage %s!\n" % (target.get_name(), damage))
                if target.is_player():
                    target.send("%s hit you cause damage %s!\n" % (character.get_name(), damage))
                player_message_to_room(player, "%s hit %s cause damage %s!\n" % 
                                          (character.get_name(), target.get_name(), damage))
                #. target hit player
                damage = target.hit(character)
                player.send("%s hit you cause damage %s!\n" % (target.get_name(), damage))
                player_message_to_room(player, "%s hit %s cause damage %s!\n" % 
                                          (target.get_name(), character.get_name(), damage))
                #. send prompt
                prompt = character.get_prompt()
                player.send(prompt)
        else:
            player.send_cc('^RYou Dead!^~\n')
            character.increase_hp(1)
            
