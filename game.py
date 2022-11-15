"""
Chapitre 11.1

Classes pour représenter un personnage.
"""

import random

import utils


class Weapon:
    """
	Une arme dans le jeu.

	:param name: Le nom de l'arme
	:param power: Le niveau d'attaque
	:param min_level: Le niveau minimal pour l'utiliser
	"""
    UNARMED_POWER = 20

    def __init__(self, name, power, min_level):
        self.__name = name
        self.power = power
        self.min_level = min_level

    @property
    def name(self):
        return self.__name

    @classmethod
    def make_unarmed(cls):
        return cls("Unarmed", cls.UNARMED_POWER, 1)


class Character:
    """
	Un personnage dans le jeu

	:param name: Le nom du personnage
	:param max_hp: HP maximum
	:param attack: Le niveau d'attaque du personnage
	:param defense: Le niveau de défense du personnage
	:param level: Le niveau d'expérience du personnage
	"""

    def __init__(self, name, max_hp, attack, defense, level):
        self.__name = name
        self.max_hp = max_hp
        self.attack = attack
        self.defense = defense
        self.level = level
        self.__weapon = None
        self.hp = max_hp

    @property
    def name(self):
        return self.__name

    @property
    def weapon(self):
        return self.__weapon

    @property
    def hp(self):
        return self.__hp

    @hp.setter
    def hp(self, val):
        self.__hp = utils.clamp(val, 0, self.max_hp)

    @weapon.setter
    def weapon(self, val):
        if val is None:
            val = Weapon.make_unarmed()
        else:
            if val.min_level > self.level:
                raise ValueError(Weapon)
        self.__weapon = val

    def compute_damage(self, other_character):
        crit = random.random() <= 0.0625
        modifier = (2 if crit else 1) * random.uniform(0.85, 1)
        dmg = ((((2 * self.level / 5) + 2) * self.__weapon.power * (
                    self.attack / other_character.defense)) / 50 + 2) * modifier
        return dmg, crit


def deal_damage(attacker: Character, defender: Character):
    dmg, crit = attacker.compute_damage(defender)
    defender.hp -= dmg
    crit_message = "\n\tIt was super effective"
    print(f"{attacker.name} used {attacker.weapon.name}{crit_message if crit else ''}"
          f"\n\t{defender.name} took {int(dmg)} dmg")


def run_battle(c1: Character, c2: Character):
    print(f"{c1.name} starts a battle with {c2.name}")
    attacker = c1
    defender = c2
    turns = 0
    while c1.hp > 0 and c2.hp > 0:
        deal_damage(attacker, defender)
        attacker, defender = defender, attacker
        turns += 1
    print(f"{attacker.name} is dead")
    return turns
