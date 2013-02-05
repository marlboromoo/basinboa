#!/usr/bin/env python
"""
Statistics system.
"""

class Statistics(object):
    """docstring for Statistics"""
    def __init__(self, ability, class_):
        super(Statistics, self).__init__()
        self.ability = ability
        self.class_ = class_

    def max_health_points(self):
        """docstring for max_health_points"""
        con_mod = self.ability.modifier(self.ability.constitution)
        hp = self.ability.constitution + self.class_.health_points + \
                ((con_mod+self.class_.health_points) * (self.ability.level-1))
        return hp

    def max_anima_points(self):
        """docstring for max_anima_points"""
        return 5 + self.ability.bonus(self.ability.wisdom)

    def initiative_bonus(self):
        """docstring for initiative_bonus"""
        return self.ability.bonus(self.ability.dexterity) #+ misc

    def melee_bonus(self):
        """docstring for melee_bonus"""
        return self.ability.bonus(self.ability.strength) #+ misc

    def ranged_bonus(self):
        """docstring for ranged_bonus"""
        return self.ability.bonus(self.ability.dexterity) #+ misc

    def magic_bonus(self):
        """docstring for magic_bonus"""
        return self.ability.bonus(self.ability.wisdom) #+ misc

    def armor_defense(self, armor):
        """docstring for armor_defense"""
        return 10 + self.ability.bonus(self.ability.dexterity) + armor #+ misc

    def evasion_defense(self):
        """docstring for evasion_defense"""
        return 10 + self.ability.bonus(self.ability.dexterity) #+ misc

    def magic_defense(self):
        """docstring for magic_defense"""
        return 10 + self.ability.bonus(self.ability.wisdom) #+ misc

    def resilience_defense(self):
        """docstring for resilience_defense"""
        return 10 + self.ability.bonus(self.ability.constitution) #+ misc

    def movemnet_speed(self):
        """docstring for movemnet_speed"""
        return 5 + self.ability.modifier(self.ability.dexterity) #+ misc


if __name__ == '__main__':
    from ability import Ability
    from class_ import Class
    from race import Race
    race = Race()
    ability = Ability()
    ability.generate()
    ability.wisdom = 22
    class_ = Class()
    statistics = Statistics(ability, class_)
    def yell():
        """docstring for debug"""
        print "hp:%s ap:%s mb:%s rb:%s mab:%s ad:%s ed:%s md:%s rd:%s spd:%s at level: %s" % (
            statistics.max_health_points(),
            statistics.max_anima_points(),
            statistics.melee_bonus(),
            statistics.ranged_bonus(),
            statistics.magic_bonus(),
            statistics.armor_defense(10),
            statistics.evasion_defense(),
            statistics.magic_defense(),
            statistics.resilience_defense(),
            statistics.movemnet_speed(),
            ability.level)
    print ability.dump()
    print race.dump()
    ability.apply_race_bonus(race)
    print ability.dump()

    while ability.level <= 15:
        yell()
        ability.level += 1

