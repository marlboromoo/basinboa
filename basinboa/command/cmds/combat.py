#!/usr/bin/env python
"""
combat commands
"""

from basinboa import status
from basinboa.decorator import command

@command
def kill(client, args):
    """
    kill the mob, but can't kill player.
    useage: kill <MOB_NAME>
    """
    target_name = args[0] if len(args) > 0 else None
    if not target_name:
        client.send('Huh?\n')
        return
    room = status.WORLD.locate_client_room(client)
    character = status.CHARACTERS.get(client)
    target_mob = room.get_mob_by_name(target_name)
    if target_mob:
        character.add_combat_target(target_mob)
        target_mob.add_combat_target(character)
        character.client.send("You try to kill %s\n" % (target_mob.get_name()))
        return
    target_character= room.get_character_by_name(target_name)
    if target_character:
        character.client.send("You can't 'kill' player, use 'murder' instead.\n")
        return
    if not target_character and not target_mob:
        character.client.send("No such target!\n")
        return

