import random
from termcolor import colored
import time
from items.item import Item
from items.stats import StatGenerator


class ArmorNames:

    def __init__(self):
        self.slot = None
        self.slots = ['Gloves', 'Bracers', 'Shoulders', 'Cape', 'Necklace',
                      'Trinket',
                      'Leggings', 'Boots', 'Chestplate', 'Helmet', "Hand"]

        self.common_sword_names = ['Blunt', "Rusted", "Terrible", 'Cracked',
                                   'Bent', 'Broken', 'Cursed']
        self.uncommon_sword_names = ['Clean', 'Ordinary', 'Standard Issue',
                                     'Torn Dragon', "Officer's"]
        self.rare_sword_names = ['Enchanted', 'Pristine', "Unusual",
                                 "Exceptional", "Dragon's", "Lunar"]
        self.epic_sword_names = ['Solar', 'Blessed', "King's", "Destroyer's",
                                 "Bringer Of Cataclysm's"]
        self.legendary_sword_names = ["Godking Uvera's Perisher",
                                      "Lightning King's Rod",
                                      "Calor's Smiting", "Void Born"]

        self.common_bow_names = ['Awful', 'Shoddy', 'Loose', 'Dusty',
                                 'Unimpressive', 'Cracked']
        self.uncommon_bow_names = ['Good', "Pitcher's", "Challenger's",
                                   "Animal Handler", "Ordinary"]
        self.rare_bow_names = ["Beast's", "Flame-weaver", "Frost-fire",
                               "Light's Hope", "Dark Born"]
        self.epic_bow_names = ["The Green Dragon's Own", "World Foraging",
                               "Embraced", "Luna'tharion"]
        self.legendary_bow_names = ["Godking Caliro's Own",
                                    "World Destroyer's", "Light and Dark"]

        self.common_plate_names = ['Rusty', 'Cursed', 'Old Standard Issue',
                                   "Old man's", 'Half-digested']
        self.uncommon_plate_names = ["Torn Dragon's", 'Clean',
                                     'Standard Issue', 'Ordinary', "Officer's"]
        self.rare_plate_names = ['Enchanted', 'Pristine', "Unusual",
                                 "Exceptional", "Dragon's", "Lunar"]
        self.epic_plate_names = ['Solar', 'Blessed', "King's", "Destroyer's",
                                 "Bringer Of Cataclysm's"]
        self.legendary_plate_names = ["Godking Uvera's", "Lightning King's",
                                      "Destruction's Hand", "Void Born"]

        self.common_leather_names = ['Patchwork', "Torn", "Dusty",
                                     "Unimpressing", "Flaky", 'Worn']
        self.uncommon_leather_names = ['Felted', 'Good', 'Challenger',
                                       'Animal Handler', 'Pitchfork']
        self.rare_leather_names = ['Beast', 'Flame-weaver', 'Frost-fire',
                                   "Light's Hope", "Dark Born"]
        self.epic_leather_names = ["The Green Dragon's Own", "World Foraging",
                                   "Embraced", "Luna'tharion"]
        self.legendary_leather_names = ["Godking Caliro's Own",
                                        "World Destroyer's", "Light and Dark"]


class Loot:

    def __init__(self, level):
        self.level = str(level)
        self.names = ArmorNames()
        self.name = ''
        self.slot = None
        self.armor_list = {True: 0, False: 0}
        self.loot_list = {"white": 0, "green": 0, "blue": 0, "magenta": 0,
                          "yellow": 0}
        self.rarities = {"Common": "white", "Uncommon": "green",
                         "Rare": "blue", "Epic": "magenta",
                         "Legendary": "yellow"}
        self.reversed_rarities = {"white": "Common", "green": "Uncommon",
                                  "blue": "Rare", "magenta": "Epic",
                                  "yellow": "Legendary"}
        self.rarity = self.rarities['Common']

    def random_loot(self, player_class, modifier=0, force_slot=False,
                    force_type=False, force_rarity=False,
                    force_name=False, restrict_slot=False):
        loot_chance = random.randint(1,
                                     1000) + modifier
        # EDIT THIS VALUE TO CHANGE THE CHANCE OF RARITY ^^

        plate_chance = 0

        if force_type is False:
            if player_class == 'Knight':
                plate_chance += 40
            else:
                plate_chance -= 40
            plate_chance = (random.randint(1, 100) + plate_chance)
            if plate_chance > 50:
                plate = True
            else:
                plate = False
        else:
            plate = force_type

        # print(loot_chance)
        if force_slot is False and restrict_slot is False:
            self.slot = random.choice(self.names.slots)
        elif force_slot is not False:
            self.slot = force_slot
        if restrict_slot is not False:
            self.slot = random.choice(self.names.slots)
            while self.slot in restrict_slot:
                self.slot = random.choice(self.names.slots)

        if self.slot == "Hand":
            if plate is True:
                sword = True
                self.slot = "Sword"
            else:
                sword = False
                self.slot = "Bow"
        else:
            sword = None
        if force_rarity is False:
            if loot_chance >= 1000:
                self.rarity = self.rarities['Legendary']
                if plate is True and sword is None:
                    self.name = str(
                        random.choice(self.names.legendary_plate_names))
                elif plate is False and sword is None:
                    self.name = str(
                        random.choice(self.names.legendary_leather_names))

                if sword is True:
                    self.name = str(
                        random.choice(self.names.legendary_sword_names))
                elif sword is False:
                    self.name = str(
                        random.choice(self.names.legendary_bow_names))

            elif loot_chance > 960:
                self.rarity = self.rarities['Epic']

                if plate is True and sword is None:
                    self.name = str(random.choice(self.names.epic_plate_names))
                elif plate is False and sword is None:
                    self.name = str(
                        random.choice(self.names.epic_leather_names))

                if sword is True:
                    self.name = str(random.choice(self.names.epic_sword_names))
                elif sword is False:
                    self.name = str(random.choice(self.names.epic_bow_names))
            elif loot_chance > 850:
                self.rarity = self.rarities['Rare']

                if plate is True and sword is None:
                    self.name = str(random.choice(self.names.rare_plate_names))
                elif plate is False and sword is None:
                    self.name = str(
                        random.choice(self.names.rare_leather_names))

                if sword is True:
                    self.name = str(random.choice(self.names.rare_sword_names))
                elif sword is False:
                    self.name = str(random.choice(self.names.rare_bow_names))
            elif loot_chance > 600:
                self.rarity = self.rarities['Uncommon']
                if plate is True and sword is None:
                    self.name = str(
                        random.choice(self.names.uncommon_plate_names))
                elif plate is False and sword is None:
                    self.name = str(
                        random.choice(self.names.uncommon_leather_names))

                if sword is True:
                    self.name = str(
                        random.choice(self.names.uncommon_sword_names))
                elif sword is False:
                    self.name = str(
                        random.choice(self.names.uncommon_bow_names))
            else:
                self.rarity = self.rarities['Common']
                if plate is True and sword is None:
                    self.name = str(
                        random.choice(self.names.common_plate_names))
                elif plate is False and sword is None:
                    self.name = str(
                        random.choice(self.names.common_leather_names))

                if sword is True:
                    self.name = str(
                        random.choice(self.names.common_sword_names))
                elif sword is False:
                    self.name = str(random.choice(self.names.common_bow_names))
        else:
            if force_rarity == 'common':
                self.rarity = self.rarities['Common']
                if plate is True and sword is None:
                    self.name = str(
                        random.choice(self.names.common_plate_names))
                elif plate is False and sword is None:
                    self.name = str(
                        random.choice(self.names.common_leather_names))

                if sword is True:
                    self.name = str(
                        random.choice(self.names.common_sword_names))
                elif sword is False:
                    self.name = str(random.choice(self.names.common_bow_names))
            elif force_rarity == 'uncommon':
                self.rarity = self.rarities['Uncommon']
                if plate is True and sword is None:
                    self.name = str(
                        random.choice(self.names.uncommon_plate_names))
                elif plate is False and sword is None:
                    self.name = str(
                        random.choice(self.names.uncommon_leather_names))

                if sword is True:
                    self.name = str(
                        random.choice(self.names.uncommon_sword_names))
                elif sword is False:
                    self.name = str(
                        random.choice(self.names.uncommon_bow_names))
            elif force_rarity == 'rare':
                self.rarity = self.rarities['Rare']

                if plate is True and sword is None:
                    self.name = str(random.choice(self.names.rare_plate_names))
                elif plate is False and sword is None:
                    self.name = str(
                        random.choice(self.names.rare_leather_names))

                if sword is True:
                    self.name = str(random.choice(self.names.rare_sword_names))
                elif sword is False:
                    self.name = str(random.choice(self.names.rare_bow_names))
            elif force_rarity == 'epic':
                self.rarity = self.rarities['Epic']

                if plate is True and sword is None:
                    self.name = str(random.choice(self.names.epic_plate_names))
                elif plate is False and sword is None:
                    self.name = str(
                        random.choice(self.names.epic_leather_names))

                if sword is True:
                    self.name = str(random.choice(self.names.epic_sword_names))
                elif sword is False:
                    self.name = str(random.choice(self.names.epic_bow_names))
            elif force_rarity == 'legendary':
                self.rarity = self.rarities['Legendary']
                if plate is True and sword is None:
                    self.name = str(
                        random.choice(self.names.legendary_plate_names))
                elif plate is False and sword is None:
                    self.name = str(
                        random.choice(self.names.legendary_leather_names))

                if sword is True:
                    self.name = str(
                        random.choice(self.names.legendary_sword_names))
                elif sword is False:
                    self.name = str(
                        random.choice(self.names.legendary_bow_names))

        if force_name is not False:
            self.name = force_name

        try:
            self.loot_list[self.rarity] += 1
        except KeyError:
            self.loot_list[self.rarity] = 1

        try:
            self.armor_list[plate] += 1
        except KeyError:
            self.armor_list[plate] = 1

        if plate is True and sword is None:
            armor_type = 'Plate'
            is_weapon = ''
        elif plate is False and sword is None:
            armor_type = 'Leather'
            is_weapon = ''
        elif sword is True:
            armor_type = 'Sword'
            is_weapon = 'Sword'
        elif sword is False:
            armor_type = 'Bow'
            is_weapon = 'Bow'
        else:
            is_weapon = ''
            armor_type = ''
        stat = StatGenerator()
        damage = None
        armor_stats = stat.generate_stats(str(self.level), is_weapon, str(
            self.reversed_rarities[self.rarity]))
        for stat in armor_stats:
            if stat == 'Damage':
                damage = armor_stats[stat]
        if self.slot == 'Sword':
            self.slot = 'Hand'
        elif self.slot == 'Bow':
            self.slot = 'Hand'
        loot_object = Item(self.slot, self.name, armor_type, self.level,
                           self.reversed_rarities[self.rarity],
                           self.rarity, armor_stats, damage)
        return loot_object


if __name__ == '__main__':

    while True:
        a = input("Player Class:")
        c = input("Player Level:")
        loot = Loot(c)
        b = input("Amount of tries: ")
        tries = b
        for x in range(int(tries)):
            loot.random_loot(player_class=a)

        print("After " + str(tries) + " tries")
        for loot_item in loot.loot_list:
            if loot_item == "white":
                string = colored("Common(s)", "white")
            elif loot_item == "green":
                string = colored("Uncommon(s)", "green")
            elif loot_item == "magenta":
                string = colored("Epic(s)", "magenta")
            elif loot_item == "blue":
                string = colored("Rare(s)", "blue")
            elif loot_item == "yellow":
                string = colored("Legendary(ies)", "yellow")
            else:
                string = None
            print(string + "  " + str(loot.loot_list[loot_item]))
        for l in loot.armor_list:
            if l is True:
                print(str(loot.armor_list[l]) + " " + ' Plate armor')
            else:
                print(str(loot.armor_list[l]) + " " + ' Leather armor')
        print('Class: ' + a)
        time.sleep(3)
