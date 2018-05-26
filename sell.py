import random
from items.item import Item


def price_of_treasure(treasure: Item):
    """
    RPM = Rarity Price Modifier
    :param treasure: Treasure Item to be priced,
     has to be a Item class instance.
    :return: returns a string that pretty prints
     the amount and the amount of coins it was worth.
    """
    price = (random.randint(25, 50) * (int(treasure.level) / 2))
    rpm = {'Common': price / 2, 'Uncommon': price / 1.5, 'Rare': price * 1.5,
           'Epic': price * 2, 'Legendary': price * 5,
           }
    return (str(rpm[treasure.rarity]) + ' Coins', 'yellow'),\
        rpm[treasure.rarity]
