from termcolor import cprint, colored
from items.loot import Loot
import random
import time


class Player:

    def __init__(self, name, player_class):
        self.monster_attacking_player = None
        self.player_class = player_class
        self.location_in_wild = ''
        self.name = name + ' the ' + player_class
        self.slots = {'Gloves': None, 'Bracers': None, 'Shoulders': None,
                      'Cape': None, 'Necklace': None,
                      'Trinket': None, 'Leggings': None, 'Boots': None,
                      'Chestplate': None, 'Helmet': None,
                      "Hand": None}

        self.slots_to_number = {0: 'Gloves',
                                1: 'Bracers',
                                2: 'Shoulders',
                                3: 'Cape',
                                4: 'Necklace',
                                5: 'Trinket',
                                6: 'Leggings',
                                7: 'Boots',
                                8: 'Chestplate',
                                9: 'Helmet',
                                10: 'Hand',
                                }
        self.taken_boss_one_paper = False
        self.boss_one = 'alive'

        self.strength = 0
        self.dexterity = 0
        if self.player_class == 'Knight':
            self.max_hp = 25
            self.hp = 25
        else:
            self.max_hp = 20
            self.hp = 20

        if self.player_class == 'Knight':
            self.armor = 10
        else:
            self.armor = 0
        self.max_hp = self.hp
        self.magic_power = 0
        self.mana_boost = 100
        self.mana = self.mana_boost
        if self.player_class == 'Archer':
            self.min_dmg = 5
            self.max_dmg = 7
        if self.player_class == 'Knight':
            self.min_dmg = 3
            self.max_dmg = 5
        self.damage = random.randint(self.min_dmg, self.max_dmg)
        self.xp = 0
        self.level = 1
        self.coins = 100
        self.level_up_xp = self.level * 40
        self.turns_to_unbuff_play = 0
        self.player_buff = 0
        if self.player_class == 'Knight':
            self.abilities = {
                "Slash": "Damage",
                "Destroy": "Execute",
                "Potion": "Heal",
                "Chant": "Buff",
                "Channel": "Mana",
                "Concuss": "Stun"
            }

            self.mana_cost = {"Potion": 40,
                              "Slash": 30,
                              "Destroy": 75,
                              "Chant": 30,
                              "Channel": 00,
                              "Concuss": 70}
        if self.player_class == 'Archer':
            self.abilities = {
                "Aimed Shot": "Damage",
                "Volley": "Execute",
                "Potion": "Heal",
                "Roar": "Buff",
                "Rest": "Mana",
                "Stun Arrow": "Stun"
            }

            self.mana_cost = {"Potion": 40,
                              "Aimed Shot": 20,
                              "Volley": 65,
                              "Roar": 30,
                              "Rest": 00,
                              "Stun Arrow": 80}
        self.inventory = []

    def give_starting_gear(self):
        item_generator = Loot(level=1)
        if self.player_class == 'Knight':
            weapon = item_generator.random_loot('Knight', force_name='Dull',
                                                force_rarity='common',
                                                force_slot='Hand',
                                                force_type=True)
        elif self.player_class == 'Archer':
            weapon = item_generator.random_loot('Archer',
                                                force_name='Terrible',
                                                force_rarity='common',
                                                force_slot='Hand',
                                                force_type=False)
        else:
            weapon = item_generator.random_loot('Knight',
                                                force_name='You forgot '
                                                           'to add a clause '
                                                           'for this new'
                                                           ' class',
                                                force_rarity='legendary',
                                                force_slot='Necklace',
                                                force_type=True,)
        self.slots['Hand'] = weapon
        self.reset_stats()

    def stun_text(self):
        if self.player_class == 'Knight':
            cprint(
                "You smash the " + self.monster_attacking_player +
                "'s head with the hilt of your sword stunning it",
                "green")
            cprint("-30 mana", "blue")
        elif self.player_class == 'Archer':
            cprint(
                "You fire a stun arrow laced with anaesthetic stunning the " +
                self.monster_attacking_player,
                "green")
            cprint("-30 mana", "blue")

    def execute_text(self, damage):
        if self.player_class == 'Knight':
            cprint("You unleash a flurry of destructive steel, dealing " + str(
                damage) + " damage",
                   "green", attrs=["bold"])
            cprint("-75 mana", "blue")
        elif self.player_class == 'Archer':
            cprint(
                "You fire dozens of shots raging"
                " through the air to your target, dealing " + str(
                    damage) + " damage",
                "green", attrs=["bold"])
            cprint("-65 mana", "blue")

    def mana_text(self, mana_gain):
        if self.player_class == 'Knight':
            cprint("You channel nearby magic to yourself gaining " + str(
                mana_gain)
                   + " mana", "green", attrs=["bold"])
            cprint("+" + str(mana_gain) + " mana", "blue", attrs=["bold"])
        elif self.player_class == 'Archer':
            cprint(
                "You rest, delving deep into"
                " the earth to find renewed power gaining " + str(
                    mana_gain)
                + " mana", "green", attrs=["bold"])
            cprint("+" + str(mana_gain) + " mana", "blue", attrs=["bold"])

    def buff_text(self):
        if self.player_class == 'Knight':
            cprint(
                "You chant at the" + self.monster_attacking_player +
                ", giving you holy power ",
                "green", attrs=["bold"])
            cprint("-30 mana", "blue", attrs=["bold"])
        elif self.player_class == 'Archer':
            cprint(
                "You let out a furious roar,"
                " giving you the strength of a bear ",
                "green", attrs=["bold"])
            cprint("-30 mana", "blue", attrs=["bold"])

    def heal_text(self, heal):
        if self.player_class == 'Knight':
            cprint("You drink a potion, gaining back " + str(
                heal) + " points of health", "green", attrs=["bold"])
            cprint("-40 mana", "blue", attrs=["bold"])
        elif self.player_class == 'Archer':
            cprint("You rest, nature giving you life. You gain back " + str(
                heal) + " points of health", "green", attrs=["bold"])
            cprint("-40 mana", "blue", attrs=["bold"])

    def damage_text(self, damage):
        if self.player_class == 'Knight':
            cprint(
                "You slash your sword against the " +
                self.monster_attacking_player + ", dealing " + str(
                    damage) + " damage",
                "green", attrs=["bold"])
            cprint("-30 mana", "blue", attrs=["bold"])
        elif self.player_class == 'Archer':
            cprint(
                "You fire a shot against the " + self.monster_attacking_player
                + "'s head, dealing " + str(
                    damage) + " damage",
                "green", attrs=["bold"])
            cprint("-20 mana", "blue", attrs=["bold"])

    def __str__(self):

        self.coins = int(self.coins)
        damage_reduction = self.armor / 200
        if damage_reduction > 0.30:
            damage_reduction = 0.30
        self.armor = round(self.armor, 2)
        self.max_dmg = round(self.max_dmg, 2)
        self.min_dmg = round(self.min_dmg, 2)
        self.max_hp = round(self.max_hp, 2)
        self.hp = round(self.hp, 2)
        if self.player_class == 'Knight':
            string = """
----{0}-----
{1}

Health:         {17}/{11}
Strength:       {2} (+{14} Player DMG)
Dexterity:      {3}
Armor:          {4} (-{15}% Monster DMG)
Magic Power:    {5} (+{16} Heal Power)
Mana:           {6}
Damage:         {7} - {8}

Exp:       {9} / {13}
Level:     {10}
Coins:     {12}
------------
            """.format(self.name, self.player_class, self.strength,
                       self.dexterity, self.armor, self.magic_power,
                       self.mana_boost,
                       self.min_dmg, self.max_dmg, self.xp, self.level,
                       self.max_hp, self.coins, self.level_up_xp,
                       (self.strength / 2), (damage_reduction * 100)
                       - (self.level / 2),
                       self.magic_power / 2, self.hp)
        elif self.player_class == 'Archer':
            string = """
----{0}-----
{1}

Health:         {17}/{11}
Strength:       {2}
Dexterity:      {3} (+{14}  Player DMG)
Armor:          {4} (-{15}% Monster DMG)
Magic Power:    {5} (+{16}  Heal Power)
Mana:           {6}
Damage:         {7} - {8}

Exp:       {9} / {13}
Level:     {10}
Coins:     {12}
------------
                    """.format(self.name, self.player_class, self.strength,
                               self.dexterity, self.armor, self.magic_power,
                               self.mana_boost,
                               self.min_dmg, self.max_dmg, self.xp, self.level,
                               self.max_hp, self.coins,
                               self.level_up_xp, (self.dexterity / 2),
                               damage_reduction,
                               self.magic_power / 2, self.hp)

        else:
            string = 'Invalid Class! Check if you added' \
                     ' a new string clause in Player.py'
        return string

    def reset_stats(self):

        self.strength = 0
        self.dexterity = 0
        if self.player_class == 'Knight':
            self.armor = 10
        else:
            self.armor = 0
        self.magic_power = 0
        self.mana_boost = 100
        if self.player_class == 'Knight':
            self.min_dmg = 3
            self.max_dmg = 5
        elif self.player_class == 'Archer':
            self.min_dmg = 5
            self.max_dmg = 7
        self.level_up_xp = self.level * 40
        self.damage = random.randint(self.min_dmg, self.max_dmg)

    def update_stats(self):
        self.reset_stats()
        for l in self.slots:
            if self.slots[l] is not None:
                stats = self.slots[l].armor_stats
                if 'Strength' in stats:
                    self.strength += stats['Strength']
                    if self.player_class == 'Knight':
                        self.min_dmg = 3 + (self.strength / 4)
                        self.max_dmg = 5 + (self.strength / 2)

                if 'Dexterity' in stats:
                    self.dexterity += stats['Dexterity']
                    if self.player_class == 'Archer':
                        self.min_dmg = 3 + (self.dexterity / 2)
                        self.max_dmg = 5 + self.dexterity
                if 'Health' in stats:
                    self.max_hp += (stats['Health'] / 3)
                if 'Mana Boost' in stats:
                    self.mana_boost += stats['Mana Boost']
                if 'Armor' in stats:
                    if self.player_class == 'Knight':
                        self.armor += stats['Armor'] * 1.5
                    else:
                        self.armor += stats['Armor']
                if 'Magic Power' in stats:
                    self.magic_power += stats['Magic Power']
                if 'Damage' in stats:
                    if self.slots[
                        l].armor_type == 'Bow' and\
                            self.player_class == "Archer":
                        self.min_dmg = 3 + stats['Damage'] / 2
                        self.max_dmg = 5 + stats['Damage']
                    elif self.slots[
                        l].armor_type == 'Sword' and\
                            self.player_class == "Knight":
                        self.min_dmg = 3 + stats['Damage'] / 2
                        self.max_dmg = 5 + stats['Damage']
        if self.player_class == 'Knight':
            self.min_dmg = 3 + self.strength / 4
            self.max_dmg = 5 + self.strength / 2
        if self.player_class == 'Archer':
            self.min_dmg = 3 + self.dexterity / 3
            self.max_dmg = 5 + self.dexterity / 2

    def view_player(self):
        continue_ = False
        while continue_ is False:
            for _ in range(20):
                print('')
            print(self)
            index = 0
            for l in self.slots:
                if self.slots[l] is None:
                    name = None
                    color = 'red'
                    color2 = 'red'
                else:
                    slot = str(self.slots[l].slot)
                    if slot == 'Hand':
                        slot = self.slots[l].armor_type
                    name = str(self.slots[l].name) + " " + slot
                    color = self.slots[l].color_rarity
                    color2 = 'green'
                print(colored(
                    "[" + str(index) + "]Slot: " + l + "    Equipped: ",
                    color2) + colored(str(name),
                                      color=color))
                index += 1

            print(' _______________________________________________')
            print('| Press [Y] to Continue                         |')
            print('| Press [N] to Quit                             |')
            print('| Press [I] to view inventory                   |')
            print('| Press a Number to view more information       |')
            print(' -----------------------------------------------')
            a = input()
            a = a.lower()
            if a.lower() == "n":

                return 'n'
            elif a.lower() == "y":

                return 'y'
            elif a == 'i':
                self.view_inventory()

            if a in '123456789010':
                item_slot = self.slots_to_number[int(a)]
                print(item_slot)
                self.view_item(item_slot)

    def view_item(self, item='Gloves'):
        list_of_options = ['[#]Different Item', '[D]equip']
        if self.slots[item] is not None:
            print(self.slots[item].print())
            for option in list_of_options:
                print('| ' + option)
            choice = input('-->')
            choice = str(choice.lower())
            if choice not in '123456789010':
                if choice == 'd':
                    self.inventory.append(self.slots[item])
                    self.slots[item] = None
                    print('Unequipped Item!')
                    time.sleep(2)
        else:
            print("You don't have an item in that slot!")

    def view_inventory(self):
        if not self.inventory:
            print("You don't have any items in your inventory!")
            time.sleep(2)
        for item in self.inventory:
            item.print()
            a = input('Next Item [Y] or [N] or [E]quip Item')
            if a == 'n':
                return
            if a == 'e':
                if item.armor_type == 'Leather' and\
                        self.player_class == 'Knight' or \
                        (item.armor_type == 'Bow' and self.player_class
                         == 'Knight'):
                    print('You can not equip this item.')

                elif (
                        item.armor_type == 'Plate' and self.player_class ==
                        'Archer') or \
                        (
                                item.armor_type == 'Sword' and
                                self.player_class == 'Archer'):
                    print('You can not equip this item.')

                elif self.slots[item.slot] is None:
                    print(
                        "Are you sure you want to equip"
                        " this item? The current slot is empty.")
                    a = input("[E]quip or [C]ancel")
                    if a == "E" or a == "e":
                        self.slots[item.slot] = item
                        self.inventory.remove(item)
                        print("Equipped!")
                        self.update_stats()

                else:
                    print(
                        "You already have an item with the same slot"
                        " Are you sure you want to equip this item?")
                    print("Equipped:")
                    self.slots[item.slot].print()
                    print("New Item:")
                    item.print()
                    b = input("[R]eplace? or [C]ancel")
                    if b == 'R' or b == 'r':
                        old_item = self.slots[item.slot]
                        self.slots[item.slot] = item
                        self.inventory.append(old_item)
                        self.inventory.remove(item)
                    self.update_stats()
        self.view_player()
        if not self.inventory:
            print("You don't have any more items.")
            time.sleep(2)
