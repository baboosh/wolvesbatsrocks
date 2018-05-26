import random


class StatGenerator:

    def __init__(self):
        self.strength = 0
        self.dexterity = 0
        self.health = 0
        self.armor = 0
        self.magic_power = 0
        self.mana_boost = 0
        self.num_of_stats = 0
        self.damage = 0

        self.common_stats = ['Strength', 'Dexterity', 'Armor']

        self.uncommon_stats = ['Strength', 'Dexterity', 'Armor', 'Health']

        self.rare_and_epic_stats = ['Strength', 'Dexterity', 'Armor', 'Health',
                                    'Magic Power']

        self.legendary_stats = ['Strength', 'Dexterity', 'Armor',
                                'Health', 'Magic Power', 'Mana Boost']

    def generate_stats(self, level, is_weapon, rarity):
        stats = {}
        common = rarity == 'Common'
        uncommon = rarity == 'Uncommon'
        rare_or_epic = rarity == 'Rare' or rarity == 'Epic'
        legendary = rarity == 'Legendary'

        if common:
            self.num_of_stats = 2
        elif uncommon:
            self.num_of_stats = 3
        elif rare_or_epic:
            self.num_of_stats = 5
        elif legendary:
            self.num_of_stats = 6

        self.num_of_stats = random.randint(int(self.num_of_stats / 2),
                                           self.num_of_stats)
        current_stats = []
        while len(current_stats) < self.num_of_stats:
            if is_weapon == 'Bow' and 'Dexterity' not in current_stats:
                current_stats.append('Dexterity')
            elif is_weapon == 'Sword' and 'Strength' not in current_stats:
                current_stats.append('Strength')

            if common:
                new_stat = random.choice(self.common_stats)
            elif uncommon:
                new_stat = random.choice(self.uncommon_stats)
            elif rare_or_epic:
                new_stat = random.choice(self.rare_and_epic_stats)
            elif legendary:
                new_stat = random.choice(self.legendary_stats)
            else:
                new_stat = random.choice(self.common_stats)
            if new_stat not in current_stats:
                current_stats.append(new_stat)

        if 'Dexterity' in current_stats and is_weapon == 'Sword':
            current_stats.remove('Dexterity')
        elif 'Strength' in current_stats and is_weapon == 'Bow':
            current_stats.remove('Strength')

        if 'Armor' in current_stats and is_weapon is not False:
            current_stats.remove('Armor')

        for statistic in current_stats:
            level = int(level)
            if statistic == 'Strength' and is_weapon == 'Sword':
                bonus = level * 2
            elif statistic == 'Dexterity' and is_weapon == 'Bow':
                bonus = level * 2
            else:
                bonus = 0
            stat_num = random.randint(level, (level * 3))
            if common:
                stat_num -= level * 2
            if uncommon:
                stat_num -= level * 1.5
            if rare_or_epic:
                stat_num += level * 2
            if legendary:
                stat_num += level * 5
            if stat_num <= 1:
                stat_num = 1
            stats[statistic] = stat_num
            stats[statistic] += bonus

        if is_weapon != '':
            if is_weapon == "Sword":
                self.damage = int(level * (stats['Strength'] * 0.25))
            elif is_weapon == 'Bow':
                self.damage = int(level * (stats['Dexterity'] * 0.25))
            stats['Damage'] = self.damage
        return stats


if __name__ == '__main__':
    stat = StatGenerator()
    print(stat.generate_stats(30, 'Sword', 'Legendary'))

    print('Legendary')
    print(stat.generate_stats(30, '', 'Epic'))
    print('Epic')
    print(stat.generate_stats(30, '', 'Uncommon'))
    print('Uncommon')
    print(stat.generate_stats(30, '', 'Common'))
    print('Common')
    print(stat.generate_stats(10, '', 'Common'))
    print('Common')
    print(stat.generate_stats(1, '', 'Common'))
    print('Common')
