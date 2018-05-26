from termcolor import cprint


class Item:

    def __init__(self, slot, name, armor_type, level, rarity, color_rarity,
                 armor_stats, damage):
        self.kwargs = f'{slot}, {name}, {armor_type}, {level}, {rarity},' \
                      f' {color_rarity}, {armor_stats}, {damage}'
        self.slot = slot
        self.name = name
        self.armor_type = armor_type
        self.level = level
        self.rarity = rarity
        self.color_rarity = color_rarity
        self.armor_stats = armor_stats
        self.damage = damage

    def __repr__(self):
        return 'Item(' + self.kwargs + ')'

    def print(self):
        if self.slot == "Hand":
            if self.armor_type == "Sword":
                slot = "Sword     Hand Slot"
            else:
                slot = "Bow       Hand Slot"
        else:
            slot = self.slot

        string = """
--LVL: {3}---
{1} {0}
{2}
        """.format(slot, self.name, self.armor_type, self.level)
        cprint(string, color=self.color_rarity)
        for l in self.armor_stats:
            string3 = l + ": " + str(self.armor_stats[l])
            cprint(string3, color=self.color_rarity)
        string2 = """
{0}
---------------
                """.format(self.rarity)
        cprint(string2, color=self.color_rarity)
