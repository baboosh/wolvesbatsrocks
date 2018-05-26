import random
from Monster import Monster
import time
from termcolor import cprint, colored

from items.loot import Loot


class Combat:
    # Randomly Generated Combat

    def __init__(self, monster, player):
        self.player = player
        self.monster = monster
        self.turns_to_unbuff_mons_shield = 0
        self.monster_dr = 0

        self.monster_hp = self.monster.monster_hp
        self.monster_mana = self.monster.monster_mana
        self.max_monster_hp = self.monster.max_monster_hp
        self.monster_buff = self.monster.monster_buff
        self.monster_stun_left = self.monster.monster_stun_left
        self.turns_to_unbuff_mons = self.monster.turns_to_unbuff_mons
        self.monster_damage = self.monster.monster_damage
        self.monster_abilities = self.monster.monster_abilities

        self.player_abilities = self.player.abilities
        self.mana_cost = self.player.mana_cost

        self.knight_abilities = {0: 'Slash',
                                 1: 'Destroy',
                                 2: 'Potion',
                                 3: 'Chant',
                                 4: 'Channel',
                                 5: 'Concuss',
                                 }
        self.archer_abilities = {0: 'Aimed Shot',
                                 1: 'Volley',
                                 2: 'Potion',
                                 3: 'Roar',
                                 4: 'Rest',
                                 5: 'Stun Arrow',
                                 }

    def cast_ability(self, ability, caster):
        self.player.monster_attacking_player = self.monster.name
        if caster is "player":
            if self.player.turns_to_unbuff_play > 0:
                self.player.turns_to_unbuff_play -= 1
            if self.player.turns_to_unbuff_play == 0:
                self.player.buff = 0
            if self.player_abilities[ability] == "Heal":

                heal = random.randint(int(2 + self.player.magic_power),
                                      int(3 + self.player.magic_power +
                                          self.player.buff))
                self.player.hp += heal
                if self.player.hp > self.player.max_hp:
                    self.player.hp = self.player.max_hp
                self.player.heal_text(heal)

            if self.player_abilities[ability] == "Damage":

                damage = random.randint(int(self.player.min_dmg),
                                        int(
                                            self.player.max_dmg)) +\
                         self.player.buff
                monster_dr = self.monster_dr
                if self.player.buff > 0:
                    monster_dr /= 2
                damage2 = damage - (damage * monster_dr)

                self.monster_hp -= damage2
                self.player.damage_text(damage2)

            if self.player_abilities[ability] == "Buff":
                self.player.buff = random.randint(1, 2)
                self.player.turns_to_unbuff_play = 3
                self.player.buff_text()

            if self.player_abilities[ability] == "Mana":
                mana_gain = 50
                self.player.mana += mana_gain
                if self.player.mana > self.player.mana_boost:
                    mana_gain = self.player.mana - self.player.mana_boost
                    self.player.mana = self.player.mana_boost
                self.player.mana_text(mana_gain)

            if self.player_abilities[ability] == "Execute":
                damage = random.randint(int(self.player.min_dmg) + 3,
                                        int(self.player.max_dmg + 6))
                damage = (damage - (damage * self.monster_dr))
                self.monster_hp -= damage
                self.player.execute_text(damage)

            if self.player_abilities[ability] == "Stun":
                self.monster_stun_left = random.randint(1, 3)
                self.player.stun_text()
            self.player.mana -= self.mana_cost[ability]

        elif caster is "monster":

            if self.monster.monster_abilities[ability] == "Heal":
                self.monster_mana -= 50
                heal = random.randint(1 + self.player.magic_power / 2,
                                      3 + self.player.magic_power) +\
                    self.monster_buff

                self.monster_hp += heal
                self.monster.heal_text(heal)

            if self.monster_abilities[ability] == "Damage":
                self.monster_mana -= 10
                monster_did_a_critical = False
                base_min_damage = int(
                    self.monster.level * 2 + self.player.min_dmg)
                base_max_damage = int(
                    self.monster.level * 2 + self.player.max_dmg)

                basic_damage = random.randint(base_min_damage, base_max_damage)
                damage = (basic_damage + self.monster_buff) / 2.5
                critical_chance = random.randint(1, 20)
                if critical_chance == 20:
                    damage *= 2
                    monster_did_a_critical = True
                damage_reduction = (self.player.armor / 200)
                if damage_reduction > 0.3:
                    damage_reduction = 0.3
                damage = (damage - (damage * (
                        damage_reduction - .01 * (self.player.level / 2))))
                hit_chance = random.randint(1, 100)
                hit_chance -= (damage_reduction * 100)

                cprint(self.monster.name + " attempts to claw at you", "red")
                if hit_chance > 30 and monster_did_a_critical is False:
                    cprint(self.monster.name + " hits you and deals " + str(
                        int(damage)) + ' damage', 'red', attrs=['bold'])
                    self.player.hp -= damage
                elif hit_chance > 30 and monster_did_a_critical:
                    cprint('!CRITICAL!', 'red', attrs=['bold'])
                    damage_txt = str(int(damage)) + ' damage'
                    cprint(
                        self.monster.name + " deeply wounds you and deals " +
                        damage_txt, 'red')

                    self.player.hp -= damage
                else:
                    cprint(self.monster.name + " misses!", 'cyan',
                           attrs=['bold'])

                cprint(self.monster.name + " loses 10 mana", "red")

            if self.monster_abilities[ability] == "Buff":
                self.monster_mana -= 40
                self.monster_buff = random.randint(1, 3)
                self.turns_to_unbuff_mons = 3
                cprint(self.monster.name + " Growls at you, giving it a"
                                           " bonus to it's abilities", "red")
                cprint(self.monster.name + " loses 40 mana", "red")

            if self.monster_abilities[ability] == "Mana":
                self.monster_mana += 30
                self.turns_to_unbuff_mons_shield = 3
                self.monster_dr = 0.30
                cprint(self.monster.name + " shields itself, "
                                           "gaining thirty mana"
                                           " back and shielding "
                                           "itself for 3 turns.", "red")
                cprint("Monster gains 30 mana", "red")

    def make_new_monster(self):
        level = self.player.level
        assert level > 0
        if level > 5 and self.player.location_in_wild == 'forest':
            level = 5
        elif level > 10 and self.player.location_in_wild == 'orc':
            level = 10
        elif level < 5 and self.player.location_in_wild == 'orc':
            level = 5

        elif level > 15 and self.player.location_in_wild == 'plains':
            level = 15

        elif level < 10 and self.player.location_in_wild == 'plains':
            level = 10

        if level < 15 and self.player.location_in_wild == 'mountain':
            level = 15

            # Level scales from 15 to 100 in mountains.

        self.monster = Monster(level=level,
                               location=self.player.location_in_wild)
        self.monster.generate_char(boss=False)
        self.monster_hp = self.monster.monster_hp
        self.monster_mana = self.monster.monster_mana
        self.max_monster_hp = self.monster.max_monster_hp
        self.monster_buff = self.monster.monster_buff
        self.monster_stun_left = self.monster.monster_stun_left
        self.turns_to_unbuff_mons = self.monster.turns_to_unbuff_mons
        self.monster_damage = self.monster.monster_damage
        self.monster_abilities = self.monster.monster_abilities

        self.combat()

    def gain_xp(self, xp):
        self.player.xp += xp
        if self.player.xp > self.player.level_up_xp:
            cprint("XP: " + str(self.player.xp) + "/" + str(
                self.player.level_up_xp), "green", attrs=['bold'])
            self.player.xp -= self.player.level_up_xp
            self.player.level_up_xp = self.player.level * 40
            self.player.level += 1
            cprint("Level Up! Level: " + str(self.player.level), "green",
                   attrs=['bold'])
            self.player.max_hp += int(self.player.level)
            self.player.hp = self.player.max_hp
            self.player.mana_boost += self.player.level
            self.player.mana = self.player.mana_boost

        else:
            cprint("XP: " + str(self.player.xp) + "/" + str(
                self.player.level_up_xp) +
                   " to Level " + str(self.player.level + 1), "magenta")

    def knight_cant_wear(self, treasure):
        cprint("But you can not equip this item! Reason:"
               " Knights can not equip leather/bows", 'red')
        a = input("Keep the item?")
        a = a.lower()
        if 'y' in a:
            self.player.inventory.append(treasure)

    def archer_cant_wear(self, treasure):
        cprint("But you can not equip this item! Reason:"
               " Archers can not wear plate/swords", 'red')
        a = input("Keep the item?")
        a = a.lower()
        if 'y' in a or 'k' in a:
            self.player.inventory.append(treasure)

    def win(self):
        if self.monster.looted is False:
            loot_chance = random.randint(1, 100)
            xp_reward = random.randint(self.player.level * 5,
                                       self.player.level * 10)
            coin_reward = random.randint(self.player.level * 2,
                                         self.player.level * 10)
            cprint("You win!", "cyan", attrs=["bold"])
            cprint("Coins Gained: " + str(coin_reward), "yellow")
            cprint("XP Gained: " + str(xp_reward), "magenta")
            self.player.coins += coin_reward
            self.gain_xp(xp_reward)
            if loot_chance > 40 and self.monster.looted is False:
                print(
                    "You looted an item from the " + self.monster.name +
                    "'s corpse!")
                self.monster.looted = True
                loot = Loot(self.player.level)
                treasure = loot.random_loot(self.player.player_class)
                treasure.print()

                if treasure.armor_type == 'Leather' and\
                        self.player.player_class == 'Knight' or \
                        (
                        treasure.armor_type == 'Bow' and
                        self.player.player_class == 'Knight'):
                    self.knight_cant_wear(treasure)

                elif (
                        treasure.armor_type == 'Plate' and
                        self.player.player_class == 'Archer') or \
                        (
                                treasure.armor_type == 'Sword' and
                                self.player.player_class == 'Archer'):
                    self.archer_cant_wear(treasure)

                elif self.player.slots[loot.slot] is None:
                    print("Equip this item? The current slot is empty.")
                    a = input("[E]quip or [K]eep the item for later")
                    if a == "E" or a == "e":
                        self.player.slots[loot.slot] = treasure
                        print("Equipped!")
                        self.player.update_stats()
                    else:

                        self.player.inventory.append(treasure)
                else:
                    print("You already have an item with the same slot!")
                    print("Equipped:")
                    self.player.slots[loot.slot].print()
                    print("New Item:")
                    treasure.print()
                    b = input("[R]eplace [K]eep item")
                    if b == 'R' or b == 'r':
                        old_item = self.player.slots[loot.slot]
                        self.player.slots[loot.slot] = treasure
                        a = input("Keep the old item?.")
                        if 'y' in a:
                            self.player.inventory.append(old_item)

                    elif b == 'k' or b == "K":
                        self.player.inventory.append(treasure)
                    self.player.update_stats()
            print("Continue? [Y] or [N] or [V]iew Player")
            a = input()
            if a.lower() == "n":
                return True
            elif a.lower() == "y":
                return False
            elif a.lower() == "v":
                b = self.player.view_player()
                if b == 'y':
                    return False
                if b == 'n':
                    return True

    def lose(self):

        lose_dict = ["| ____    ____  ______    __    __               |",
                     "| \   \  /   / /  __  \  |  |  |  |              |",
                     "|  \   \/   / |  |  |  | |  |  |  |              |",
                     "|   \_    _/  |  |  |  | |  |  |  |              |",
                     "|     |  |    |  `--'  | |  `--'  |              |",
                     "|     |__|     \______/   \______/               |",
                     "|                                                |",
                     "|  __        ______        _______. _______  __  |",
                     "| |  |      /  __  \      /       ||   ____||  | |",
                     "| |  |     |  |  |  |    |   (----`|  |__   |  | |",
                     "| |  |     |  |  |  |     \   \    |   __|  |  | |",
                     "| |  `----.|  `--'  | .----)   |   |  |____ |__| |",
                     "| |_______| \______/  |_______/    |_______|(__) |",
                     "                                                  "
                     ]
        for l in lose_dict:
            cprint(l, "yellow", 'on_red')
            time.sleep(0.2)
        cprint("FINAL SCORE:                                      ", "green")
        print(str(self.player.xp) + " XP")
        print(str(self.player.level) + " LVL")
        print(str(self.player.coins) + " Coins")

        quit(0)

    def can_player_cast_ability(self, ability: str):
        if self.player.mana >= self.mana_cost[ability]:
            return True
        elif self.player.mana < self.mana_cost[ability]:
            cprint("You don't have enough mana to cast " + ability + " (need "
                   + str(self.mana_cost[ability]) + " mana)", "red")

            return False

    def combat(self):
        self.player.update_stats()
        while self.player.hp > 0 or self.monster_hp > 0:
            # Player's Turn First
            for l in range(20):
                print(" ")
            ability_casted = False
            while ability_casted is False:
                print("----Player's Turn----")
                if self.player.max_hp / 4 >= self.player.hp\
                        <= self.player.max_hp / 2:
                    color = 'yellow'
                elif self.player.hp < self.player.max_hp / 4:
                    color = 'red'
                else:
                    color = 'green'
                player_hp_text = colored(str(round(self.player.hp, 2)), color,
                                         attrs=['bold'])
                cprint(self.monster.name + "'s HP: " + str(
                    round(self.monster_hp, 2)), "red", attrs=["bold"])
                cprint(self.player.name + "'s HP:  " + player_hp_text,
                       attrs=["bold"])
                if self.player.turns_to_unbuff_play > 0:
                    cprint(self.player.name + "'s Buff Left: " + str(
                        self.player.turns_to_unbuff_play), "green")
                if self.monster_stun_left > 0:
                    cprint(self.monster.name + " is stunned for " + str(
                        self.monster_stun_left) + " more turns", "red",
                           attrs=['bold'])
                if self.turns_to_unbuff_mons_shield > 0:
                    cprint(self.monster.name + "'s armor increased for " + str(
                        self.turns_to_unbuff_mons_shield) + " more turns",
                           "red", attrs=['bold'])
                if self.turns_to_unbuff_mons > 0:
                    cprint(self.player.name + "'s armor broken for " + str(
                        self.turns_to_unbuff_mons) + " more turns", "red",
                           attrs=['bold'])
                cprint("Mana: " + str(self.player.mana), "blue",
                       attrs=["bold"])
                index = 0
                for ability in self.player_abilities:
                    if self.mana_cost[ability] > self.player.mana:
                        color = 'red'
                    elif self.mana_cost[ability] == self.player.mana:
                        color = 'yellow'
                    else:
                        color = 'green'

                    space = ability.ljust(14, ' ')
                    mana_cost = str(self.mana_cost[ability])
                    printed_ability = str(index)

                    cprint('[' + printed_ability + ']' + " | " + space +
                           '(' + mana_cost + ')', color)
                    index += 1
                print("---What do you do?---")
                ability_choice = input()
                if ability_choice == "die":
                    self.lose()
                if ability_choice == 'wound':
                    self.player.hp = 1
                elif ability_choice == 'half':
                    self.player.hp = self.player.hp / 2
                if ability_choice not in '1234567890':
                    ability_casted = False
                    print("Invalid Option!")
                else:
                    ability_choice = int(ability_choice)
                    if self.player.player_class == 'Knight':
                        ability_choice = self.knight_abilities[ability_choice]
                    elif self.player.player_class == 'Archer':
                        ability_choice = self.archer_abilities[ability_choice]

                    if self.can_player_cast_ability(ability_choice):
                        self.cast_ability(ability_choice, 'player')
                        ability_casted = True

            if self.player.hp < self.player.max_hp / 2:
                color = 'yellow'
            elif self.player.hp < self.player.max_hp / 4:
                color = 'red'
            else:
                color = 'green'
            player_hp_text = colored(str(round(self.player.hp, 2)), color,
                                     attrs=['bold'])
            cprint(
                self.monster.name + "'s HP: " + str(round(self.monster_hp, 2)),
                "red", attrs=["bold"])
            cprint(self.player.name + "'s HP:  " + player_hp_text, "green",
                   attrs=["bold"])

            if self.player.turns_to_unbuff_play > 0:
                cprint(self.player.name + "'s Buff Left: " + str(
                    self.player.turns_to_unbuff_play - 1), "green")
            time.sleep(3)
            if self.player.mana < 0:
                self.player.mana = 0
            if self.monster_mana < 0:
                self.monster_mana = 0
            # Monster's Turn
            if self.monster_hp <= 0:
                self.win()
            if self.monster_hp <= 0:
                return False
            self.monster.play_turn(self)
