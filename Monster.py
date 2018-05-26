import random
import time
from termcolor import cprint


class Monster:

    def __init__(self, level, location):
        self.location = location
        self.level = level
        self.creature_type = None
        self.monster_hp = random.randint(5 * level, 5 * level + level)

        self.monster_mana = 100
        self.max_monster_hp = self.monster_hp
        self.monster_buff = 0
        self.monster_stun_left = 0
        self.looted = False
        self.type = None
        self.types = ['Paranoid', 'Ruthless', 'Magical']
        self.turns_to_unbuff_mons = 0
        self.monster_damage = random.randint(int(1.0 * level), int(2 * level))
        self.monster_ability_weights = {}
        self.monster_abilities = {"Regrow": "Heal",
                                  "Claw": "Damage",
                                  "Growl": "Buff",
                                  "Shield": "Mana"}

        self.name = None
        self.forest_names = ['Dire Wolf', 'Rabid Dog', 'Insane Elk',
                             'Rotting Fox']

        # self.generate_char(False)

    def create_ability_weights(self):
        for ability in self.monster_abilities:
            self.monster_ability_weights[ability] = 0.33

    def generate_char(self, boss):
        self.type = random.choice(self.types)
        if boss is False:
            if self.location == 'forest':
                name = self.forest_names
            else:
                name = self.forest_names
            if self.type == 'Paranoid':
                self.monster_hp += self.monster_hp / 2
            if self.type == 'Ruthless':
                self.monster_damage += self.monster_damage / 2
            if self.type == 'Magical':
                self.monster_mana += self.monster_mana / 2
        else:
            name = boss
            self.monster_hp *= 2
            self.monster_mana *= 1.5
            self.monster_damage *= 1.5
            self.type = 'Badass'
            if 10 < self.level < 30:
                self.type = 'Super Badass'
                self.monster_hp += self.monster_hp / 2

        self.creature_type = self.name
        self.name = 'LVL: ' + str(
            self.level) + ' ' + self.type + " " + random.choice(name)

    def play_turn(self, combat):
        print("----Monster's Turn----")

        if combat.monster_stun_left >= 1:
            combat.monster_stun_left -= 1
            if combat.monster_stun_left == 0:
                cprint("The stun effect has worn off on " + self.name, "red")
            else:
                if combat.monster_stun_left > 1:
                    turn = " more turns"
                else:
                    turn = " more turn"
                cprint(self.name + "is stunned for " + str(
                    combat.monster_stun_left) + turn, "red")
        else:
            if combat.turns_to_unbuff_mons_shield >= 1:
                combat.turns_to_unbuff_mons_shield -= 1
                if combat.turns_to_unbuff_mons_shield == 0:
                    combat.monster_dr = 0
                    cprint(
                        combat.monster.name + "has lost it's increased armor!",
                        "red")
                else:
                    if combat.turns_to_unbuff_mons_shield > 1:
                        turn = " more turns"
                    else:
                        turn = " more turn"
                    cprint(
                        self.name + "'s armor is increased for " + str(
                            combat.turns_to_unbuff_mons_shield) + turn,
                        "red")

            ability = self.cast_ability()
            combat.cast_ability(ability, "monster")

        if combat.player.hp <= 0:
            combat.lose()
        time.sleep(3)

    def cast_ability(self):
        self.create_ability_weights()
        if self.monster_hp < 2:
            my_hp_status = 'Bad'
        else:
            my_hp_status = 'Good'

        if self.monster_mana < 2:
            my_mana_status = 'Bad'
        else:
            my_mana_status = 'Good'

        if self.type == 'Paranoid':
            if my_hp_status == 'Bad' and my_mana_status == 'Good':
                self.monster_ability_weights['Regrow'] += 0.33
            elif my_mana_status == 'Bad' or my_hp_status == 'Bad':
                self.monster_ability_weights['Shield'] += 0.20
            elif my_hp_status == 'Good' and my_hp_status == 'Good':
                self.monster_ability_weights['Claw'] += 0.15
            else:
                self.monster_ability_weights['Shield'] += 0.15

        if self.type == 'Ruthless':

            if my_hp_status == 'Bad' and my_mana_status == 'Good':
                self.monster_ability_weights['Regrow'] += 0.15
            elif my_mana_status == 'Bad' or my_hp_status == 'Bad':
                self.monster_ability_weights['Shield'] += 0.20
            elif my_hp_status == 'Good' and my_hp_status == 'Good':
                self.monster_ability_weights['Claw'] += 0.33
            else:
                self.monster_ability_weights['Shield'] += 0.15

        if self.type == 'Magical':

            if my_hp_status == 'Bad' and my_mana_status == 'Good':
                self.monster_ability_weights['Regrow'] += 0.20
            elif my_mana_status == 'Bad' or my_hp_status == 'Bad':
                self.monster_ability_weights['Shield'] += 0.33
            elif my_hp_status == 'Good' and my_hp_status == 'Good':
                self.monster_ability_weights['Claw'] += 0.15
            else:
                self.monster_ability_weights['Shield'] += 0.15

        if self.type == 'Badass' or self.type == 'Super Badass':

            if my_hp_status == 'Bad' and my_mana_status == 'Good':
                self.monster_ability_weights['Regrow'] += 0.60
            elif my_hp_status == 'Bad' or my_mana_status == 'Bad' or \
                    my_hp_status == 'Good' or my_mana_status == 'Bad':

                self.monster_ability_weights['Shield'] += 0.60

            elif my_hp_status == 'Good' and my_mana_status == 'Good':
                self.monster_ability_weights['Claw'] += 0.60
            else:
                self.monster_ability_weights['Shield'] += 0.60

        ability_chosen = False
        index = 0
        while ability_chosen is False:
            chance_to_cast = random.uniform(0, 1)
            ability_testing = random.choice(list(self.monster_ability_weights))

            ability_weight = self.monster_ability_weights[ability_testing]
            if ability_weight > chance_to_cast:
                return ability_testing

            if index == 15:
                return ability_testing
            index += 1

    def heal_text(self, heal):
        print(self.name)
        if 'Rotting Fox' in self.name:
            cprint(self.name + " regrows, regaining " + str(
                heal) + " points of health", "red")
        if 'Dire Wolf' in self.name:
            cprint(self.name + " licks it's wounds, regaining " + str(
                heal) + " points of health", "red")
        if 'Insane Elk' in self.name:
            cprint(self.name + " shrieked as it danced. It's wounds healing"
                               "with dark magic, regaining " +
                   str(heal) + " points of health", "red")
        if 'Rabid Dog' in self.name:
            cprint(
                self.name + " barked. It's skin binding tighter, regaining " +
                str(heal) + " points of health",
                "red")
        if self.name == 'Kragold The Goblin Thief':
            cprint(self.name + " licks it's wounds, regaining " + str(
                heal) + " points of health", "red")

        cprint(self.name + " loses 50 mana", "red")
