#!/usr/bin/env python
"""
combat commands
"""

from basinboa import status
from basinboa.system.decorator import command

@command
def kill(player, args):
    """
    kill the mob, but can't kill player.
    useage: kill <MOB_NAME>
    """
    target_name = args[0] if len(args) > 0 else None
    if not target_name:
        player.send('Huh?\n')
        return
    room = status.WORLD.locate_player_room(player)
    mob = room.get_mob_by_name(target_name)
    if mob:
        player.character.add_combat_target(mob)
        mob.add_combat_target(player.character)
        player.send("You try to kill %s\n" % (mob.get_name()))
        return
    player_ = room.get_player_by_name(target_name)
    if player_:
        player.send("You can't 'kill' player, use 'murder' instead.\n")
        return
    if not player_ and not mob:
        player.send("No such target!\n")
        return

