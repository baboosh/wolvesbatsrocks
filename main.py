import random
import sys
import time
import pickle
import os

from termcolor import cprint, colored

from Combat import Combat
from items.loot import Loot
from sell import price_of_treasure
from Monster import Monster
from Player import Player
from items.item import Item

from Locations.tavern import Tavern


# Test thing with flake8 [python file]
# Test thing with pylint [python file]


class Main:
    def __init__(self):
        self.player = None
        self.flags = {'kragold bounty': False,
                      'kragold killed': False,
                      'shop open': False,
                      'Godking Defeated': False}
        self.taken_boss_one_paper = False

        self.left = False
        self.locations = {"Town": 0, "Wilderness": 1, "Cemetery": 2, "Exit": 3}
        self.town_locations = {"Blacksmith": 0, "Merchant": 1, "Brewery": 2,
                               "Tavern": 2}
        self.wilderness_locations = {"Carold Mountains": 0,
                                     "The Elder Forests": 1,
                                     "Dominant Plains": 2,
                                     "Orcish Camps": 3,
                                     "Exit": 4}

    def generate_character(self, name, player_class):

        self.player = Player(name=name, player_class=player_class)
        self.player.give_starting_gear()

    def menu(self, welcome_sign):
        cprint(welcome_sign, "blue")
        for location in self.locations:
            if location == "Exit":
                cprint("| Exit", "red", attrs=["bold"])
            else:
                print("| " + location)

        destination = input("-->")

        if destination == "Exit":
            cprint('Gone so soon? (This will end the game. Yes or No)', 'blue')
            confirmation = input('-->')
            confirmation = confirmation.lower()
            if 'y' in confirmation:
                sys.exit('The adventurer left.')
            else:
                self.menu('Try again, where would you like to go')
        elif destination == "Town":
            self.town()  # Stores
        elif destination == "Cemetery":
            self.cemetery()  # Gravestone
        elif destination == "Wilderness":
            self.wilderness()  # Combat
        else:
            string = "? I've never heard of that place, try something I know."
            cprint(destination + string, 'blue')
            self.menu('Try again, where would you like to go')

    def town(self):
        print("""
________.   .________________________________.
(///(////\  ///(///(///(///(///(///(///(//// |
///(///(  \///(///(///(///(///(///(///(///(  |
//(///(   ///(///(///(///(///(///(///(///(   |
/(///(  .///(//  [TAVERN] //(///(///(///(  . |
    | .' |         ___    ___   _____  | .'| |
    | |.'|        |_|_|  |_|_| |__|__| | |.' |
    | '  |        |_|_|  |_|_| |__|__| | ' . ||'--:|
__  |  .'|    __   _____    _ %%%____  | .'| |  .|
__| | |.'|   |  | |__|__|  |_%%%%%___| ||.' .'.|   .'         .'
__| | '.'|   | .| |__|__|  |%%%:%%___| |' .'.|   .'         .'
____|.'  |___|__|___________%%::%______|.'.|   .'         .'
       .|   '-=-.'            :'       .|    .'         .'
     .|   '   .               :      .|    .'         .'
   .|   '   .                       .|   .'         .'
  |'--'|==||'--'|'--'|'--'|'--'|'-'|   .'         .'
======================================'         .'
             #
    #       ..
================================.
                ///            .'         .'
      ///      ////         .'         .'

        """)
        print("""
 ______________________________________________
|                                              |
|            Calmatian for Dummies             |
|                                              |
| [S]hop    [B]ounty Board      ##[Q]uests##   |
|                                              |
| [T]avern  ##[A]rmour Smith##  ##[W]eapon Smi |
|                                              |
 ----------------------------------------------
        """)
        choice = input('-->')
        choice = choice.lower()
        if 'sh' in choice or 'st' in choice or choice == 's':
            self.shop()

        if 'tav' in choice or 'beer' in choice or choice == 't':
            self.tavern()

        if 'bou' in choice or 'boa' in choice or choice == 'b':
            self.bounty()

        if 'armor' in choice or 'armor' in choice or 'a' in choice:
            self.armour_smith()
        else:
            self.town()

    def populate_armor_smith(self):
        items_for_sale = {}
        if self.player.level - 1 == 0:
            level = 1
        else:
            level = self.player.level - 1
        loot_generator = Loot(level)
        items_in_shop = random.randint(2, 4)
        for _ in range(items_in_shop):
            if self.player.player_class == 'Knight':
                loot = loot_generator.random_loot(self.player.player_class,
                                                  restrict_slot=['Hand',
                                                                 'Cape',
                                                                 'Trinket',
                                                                 'Necklace'],
                                                  force_type=True)
            else:
                loot = loot_generator.random_loot(self.player.player_class,
                                                  restrict_slot=['Hand',
                                                                 'Cape',
                                                                 'Trinket',
                                                                 'Necklace'],
                                                  force_type=False)
            statement, buy_price = price_of_treasure(loot)
            items_for_sale[loot] = int(buy_price * 2)
        return items_for_sale

    def armour_smith(self):
        string = '''
        The road you are walking upon seems more worn
        then the others.
        You smell coal and metal, upon turning a
        corner you see a building completely made out of stone.
        Inside a single blacksmith was hammering away
        at a piece of red hot metal.
        '''
        print(string)
        print('Continue?')
        confirmation = input()
        if confirmation != 'n':
            cprint("Do you have any armor currently for sale?", 'green')
            time.sleep(1)
            cprint("Yeah, I'll show you around.", 'cyan')
            time.sleep(1)

            print('He stops hammering away and leads you'
                  ' inside a smallish section')
            print('of the building.')
            time.sleep(2)
            index = 0
            index_to_items = {}
            items_for_sale = self.populate_armor_smith()
            choice_made = False
            while choice_made is False:
                for item in items_for_sale:
                    item.print()
                    index_to_items[index] = item
                    print('Price for Item: ' + str(items_for_sale[item]))
                    print('ID: ' + str(index))
                    print('[#] Buy Item')
                    index += 1

                print("Current Coins: " + str(self.player.coins))
                print("[V]iew Player")
                print('[Q] Return to Town Square')
                choice = input('-->')

                print(index_to_items)
                if choice in '1234567890':
                    choice = int(choice)
                    item = index_to_items[choice]
                    choice_made = self.buy_item(item, items_for_sale[item])
                    if choice_made is True:
                        self.town()
                elif choice == 'q':
                    choice_made = True
                    self.town()
                elif choice == 'v':
                    self.player.view_player()
                else:
                    cprint('What?', 'cyan')

        else:
            print('You turn away, the blacksmith gives'
                  ' you a weird look as you return')
            print('to the center square.')

    def buy_item(self, item: Item, cost: int):
        """
        Buys an item.
        :param item: The item to be bought
        :param cost: The cost of the item
        :return: If the purchase is successful return a true
        """
        if self.price_check(cost):
            self.player.inventory.append(item)
            self.player.coins -= cost
            print("You bought the item, It's been placed in your inventory.")
            cprint("-" + str(cost) + ' Coins', 'yellow')
            return True
        else:
            print("You can't afford that item.")

    @staticmethod
    def travel_to_boss_one():
        print('You are dropped off in dominant plains near a goblin camp.')
        # TODO BOSS FIGHT WITH KRAGOLD

    def bounty(self):
        if self.player.boss_one != 'dead':
            print('You walk over to the bounty board, a'
                  ' single piece of paper is hammered onto the wooden board')
            print("""
 ______________________
|                      |
|   -!! WANTED !!-     |
|                      |
|       KRAGOLD        |
|                      |
|    GOBLIN THIEF      |
|   LOCATION: DOMINANT |
|   PLAINS             |
|                      |
|   FREE RIDE BY       |
|   WOLF RIDER THANO   |
|   REWARD: 500 COINS  |
 ----------------------
            """)
            if self.player.level < 5:
                print('Do you take the bounty? This will'
                      ' be hard. LVL 5 recommended.')
            elif self.player.level > 6:
                print('Do you take the bounty? This might be easy.')
            else:
                print('Do you take the bounty? This should be normal.')
            choice = input('-->')
            choice = choice.lower()
            if 'n' not in choice:
                print('You take the piece of paper.')
                self.taken_boss_one_paper = True

    def price_check(self, coins: int):
        """
        Checks if the player has enough coins
        :param coins: If the player has more coins than this, return true
        :return: True or False
        """
        if self.player.coins >= coins:
            return True

    @staticmethod
    def get_input():
        """
        Gets the input of the player
        :return: A lower-cased version of whatever the player typed.
        """
        print('-->')
        choice = input()
        choice = choice.lower()
        return choice

    def tavern(self):
        # tavern = Tavern(self.player)
        # choice = tavern.main()

        print('You follow the sign down a main road littered with'
              ' street lamps and people shuffling about')
        print('The building was a remodeled victorian-like'
              ' two story house with a large bar in the middle')
        print('The top floor houses rooms for stays.')
        print('The wolf rider sits at a booth surrounded by knights.')
        print('Continue inside?')
        choice = self.get_input()
        if 'n' in choice:
            self.town()
        if 'n' not in choice:
            print('The bar tender greets you and asks what do you need.')
            left = False
            while left is False:
                cprint("Aye, ya look like 'er in desperate needs of"
                       " a drink! What can I do ya for?", 'yellow')
                choices = ['[B]eer',
                           '[R]ide',
                           '[I]nn',
                           '[V]iew Stats',
                           '[S]ave Game',
                           '[L]oad Game',
                           '[E]xit',
                           ]
                for option in choices:
                    cprint("| " + option, 'yellow')
                choice = input('-->')
                choice = choice.lower()
                if 's' in choice:
                    cprint("I've got some stuff I want in"
                           " safe keeping.", 'green')
                    cprint("You want me to keep track of"
                           " your stuff ey?", 'yellow')
                    cprint("Yes, Thank you.", 'green')
                    cprint("What name do you want me to "
                           "write on the name tag ay?", 'yellow')
                    choice = self.get_input()
                    cprint("Consider it done!", 'yellow')
                    with open('./saves/' + str(choice) + '.pkl', 'wb') \
                            as output:
                        pickle.dump(self.player, output,
                                    pickle.HIGHEST_PROTOCOL)
                    cprint('The game has been saved', 'blue')

                elif 'l' in choice:
                    cprint('Do you have my stuff here?', 'green')
                    save_list = os.listdir('./saves/')
                    if save_list is not []:
                        cprint('You came looking for your stuff?', 'yellow')
                        cprint('Yes.', 'green')
                        cprint("Well I've got some bags here,"
                               " just tell me which one is yours.")

                        for l in save_list:
                            print(l[:-4])
                        file = self.get_input()
                        print("WARNING Loading a save game will"
                              " delete any unsaved progress. Continue?")
                        choice = self.get_input()
                        if 'y' in choice:
                            if file in save_list or file + '.pkl' in save_list:
                                if '.pkl' not in file:
                                    file += '.pkl'
                                with open('./saves/' + file,
                                          'rb') as save_game:
                                    self.player = pickle.load(save_game)
                                    cprint('Thank you.', 'green')
                                    print('Save game', file, 'loaded.')
                                    time.sleep(3)
                                    self.town()

                            else:
                                cprint(
                                    "I don't have one with that name on it.",
                                    'yellow')
                                cprint("Apologies.", 'green')
                        else:
                            cprint('Never-mind. Just keep it safe', 'green')
                            cprint('You got it.', 'yellow')

                    else:
                        cprint("No, I haven't got anyone's"
                               " stuff here. Sorry mate.", 'yellow')
                        cprint("Darn.", 'green')

                elif 'e' in choice:
                    self.town()

                elif 'b' in choice:
                    cprint("A beer it is then! It's gonna be"
                           " 10 coins! Are you sure?", 'yellow')
                    confirmation = input('-->')
                    confirmation = confirmation.lower()
                    if self.price_check(10) and 'y' in confirmation:
                        print('You drink for an hour or so talking'
                              ' to other patrons. It gets late and you leave.')
                        mana_gain = random.randint(30, 60)
                        self.player.mana += mana_gain
                        if self.player.mana > self.player.mana_boost:
                            self.player.mana = self.player.mana_boost
                        cprint('+' + str(mana_gain) + ' Mana', 'blue')
                        time.sleep(5)
                        self.town()
                        left = True
                    else:
                        cprint(
                            "You can't afford a damn drink get out of here!",
                            'yellow')
                        self.town()
                        left = True
                elif 'r' in choice:

                    cprint('A ride? You can talk to that gentleman'
                           ' over there, he has a wolf that you can use.',
                           'yellow')
                    cprint('How much will it cost?', 'green')
                    cprint('Around hundred coins per ride.', 'yellow')
                    print('Continue?')
                    choice = self.get_input()
                    if 'y' in choice:
                        print('You walk over to the booth.'
                              ' The patrons around the table stop talking.')
                        cprint('I need a ride.', 'green')
                        cprint("You again? It's gonna cost you hundred.",
                               'blue')
                        if self.player.taken_boss_one_paper is False:
                            print('Are you sure you want to'
                                  ' spend 100 coins? You have ' + str(
                                   self.player.coins) + ' coins')
                            choice = self.get_input()
                            if 'y' in choice:
                                if self.price_check(100):
                                    cprint('-100 coins', 'yellow')
                                    self.player.coins -= 100
                                    self.menu('')
                                    left = True
                                else:
                                    cprint('What do you mean you do '
                                           'not have enough? Get out of here!',
                                           'blue')
                                    self.town()
                                    left = True
                            else:
                                cprint('Quit wasting my time and '
                                       'get out of my sight.', 'blue')
                        else:
                            cprint('I need a ride.', 'green')
                            cprint("You again? It's gonna cost you a hundred.",
                                   'blue')
                            print('[S]how Bounty [C]oins')
                            choice = self.get_input()
                            if 's' in choice:
                                cprint('I have this bounty for the '
                                       'goblin thief Kragold.'
                                       ' It says a free ride.', 'green')
                                cprint("I'll take you to Dominant Plains"
                                       " if you take down that goblin thief.",
                                       'blue')
                                cprint("Yes... That's why I showed you it.",
                                       'green')
                                cprint("It wasn't very obvious.", 'blue')
                                cprint("Just take me there.", 'green')
                                time.sleep(3)
                                self.travel_to_boss_one()
                                left = True
                            if 'c' in choice:

                                print('Are you sure you want'
                                      ' to spend 100 coins? You have ' + str(
                                       self.player.coins) + ' coins')
                                choice = input('-->')
                                choice = choice.lower()
                                if 'y' in choice:
                                    if self.price_check(100):
                                        cprint('-100 coins', 'yellow')
                                        self.player.coins -= 100
                                        self.menu('')
                                        left = True
                                    else:
                                        cprint('What do you mean you do not'
                                               ' have enough?'
                                               ' Get out of here!',
                                               'blue')
                                        self.town()
                                        left = True
                                else:
                                    cprint('Quit wasting my time'
                                           ' and get out of my sight.', 'blue')
                    else:
                        cprint('Never mind, I am good thanks.', 'green')
                        time.sleep(2)
                        self.town()
                        left = True
                elif 'i' in choice:
                    cprint('You want a room huh?', 'yellow')
                    cprint('Yes. How much will it cost me?', 'green')
                    cprint('Thirty coins for the night, Eighty for three.',
                           'yellow')
                    print('For each night you stay in a '
                          'room you heal a quarter of your health')
                    print('Do you wish to continue?')
                    print('[O]ne Night  [T]hree Nights')
                    choice = self.get_input()
                    if 'o' in choice and 'n' not in choice:
                        if self.price_check(30):
                            print('You walk up creaking stairs into '
                                  'a low roof floor, the man '
                                  'leads you into a room.')
                            cprint("This'll be your room for the night.",
                                   'yellow')
                            cprint("Thank you sir.", 'green')
                            print('You sleep for one day.')
                            time.sleep(5)
                            self.player.hp += self.player.max_hp / 4
                            if self.player.hp > self.player.max_hp:
                                self.player.hp = self.player.max_hp
                            cprint("+" + str(int(self.player.max_hp / 1.33)) +
                                   ' HP', 'green')
                            time.sleep(3)
                            self.town()
                        else:
                            cprint("You can't afford a single"
                                   " night! Get out of here!", 'yellow')
                            time.sleep(3)
                            self.town()
                    if 't' in choice and 'n' not in choice:
                        if self.price_check(80):
                            print(
                                'You walk up creaking stairs '
                                'into a roofed floor, the man leads'
                                ' you into a large room')
                            cprint('One of the finest rooms we'
                                   ' have, it is yours for three nights.',
                                   'yellow')
                            cprint('Thank you very much.', 'blue')
                            print('You sleep for three days.')
                            time.sleep(5)
                            self.player.hp += self.player.max_hp / 1.33
                            if self.player.hp > self.player.max_hp:
                                self.player.hp = self.player.max_hp
                            print("+" + str(int(self.player.max_hp / 1.33)) +
                                  ' HP', 'green')
                            self.town()
                elif 'v' in choice:
                    self.player.view_player()

    def shop(self):
        print('You follow the sign down a winding road,'
              ' through a garden of rotting tulips.')
        print(
            'You arrive in a rickety building with a large'
            ' sign out in front. The scent of beer clouds your nostrils.')
        print('Continue?')
        choice = self.get_input()
        if 'n' not in choice:
            if self.player.boss_one != 'dead':
                print('The windows are all boarded up and the door'
                      ' bolted with metal. A scribbled on sign says:')
                print('WiLL nOt Open Until KragOld is DeaD!!!')
                print('The handwriting is insane as if'
                      ' written by a fanatic old guy. '
                      'You might want to check the bounty board')
                print('Head to the bounty board?')
                choice = self.get_input()
                if choice == 'y':
                    self.bounty()
                else:
                    print('You leave the shop.')
                    time.sleep(2)
                    self.town()
            else:
                print('You enter the shop, the man'
                      ' thanks you again for getting rid of Kragold.')

        else:
            self.town()

    def wilderness(self):
        print("""
                ,@@@@@@@,
       ,,,.   ,@@@@@@/@@,  .oo8888o.
    ,&%%&%&&%,@@@@@/@@@@@@,8888\88/8o
   ,%&\%&&%&&%,@@@\@@@/@@@88\88888/88'
   %&&%&%&/%&&%@@\@@/ /@@@88888\88888'
   %&&%/ %&%%&&@@\ V /@@' `88\8 `/88'
   `&%\ ` /%&'    |.|        \ '|8'
       |o|        | |         | |
       |.|        | |         | |
      / ._\//_/__/  ,\_//__  /.  \_//__/_
        """)
        cprint("This place gives me the creeps."
               " Alright, where you wanna go from 'ere", "blue")
        for location in self.wilderness_locations:
            if location == "Exit":
                cprint("| Exit", "red", attrs=["bold"])
            else:
                print("| " + location)
        cprint("I'd recommend the forests if your new to"
               " this whole killin' monsters bizz", 'blue')
        cprint('The plains are dangerous because of them'
               ' goblins patrolling and the mountains hold golems', 'blue')
        cprint('The orcish camps are alright they have been'
               ' scattered recently after Kragold came out, probably the '
               'thing you can do after the forest.', 'blue')
        destination = input("-->")
        if 'f' in destination or 'F' in destination:
            self.forest_travel()
            self.player.location_in_wild = 'forest'
        elif destination == "Exit":
            cprint("I'll take you back to town then"
                   " I don't even want to be here.", "blue")
            self.town()
        else:
            self.wilderness()

    def cemetery(self):
        print("""
                 _  /)
                 mo / )
                 |/)\)
                  /\_
                  \__|=
                 (    )
                 __)(__
_________+______/      \______+__________
  __--   |       R.I.P.       |-_-- __
_-- -    | ___ __________ ___ |
-_-- __  || | | | {|    /| | || __---  -_
 --__-   || | | | {|   /|| | ||--        -
         || | | | {|  /||| | ||__--
 __-- -__|| | | | {| |}||| | ||--   __--
         ||_|_|_|_{| |}|||_|_||  -__
 --__-  -|| | | | {& |}||/ | ||---   __--
         || | | | {| |}|/| | ||-__
--   __--|| | | | {| |}/|| | ||__-- -__
  --     || | | | {| &}||| | ||   __
---   __-|| | | | {| |}||| | ||_---__-  --
 -  -_   || | | | {| |}||| | || --
 __-- __ || | | | {| |}||| | ||_--__-   _---
_________||_|_|_|_{| |}|||_|_||______________
        """)
        cprint('You really wanted to go here?', 'blue')
        cprint('Yeah.', 'green')
        time.sleep(2)
        print('You feel a cold dreaded feeling here when you enter the gate.')
        if self.flags['Godking Defeated'] is False:
            print('A voice burned inside your skull')
            time.sleep(1)
            cprint('Defeat The Godking and then return to me.', 'red')
            time.sleep(3)
            self.menu("Back so soon?")
        else:
            print('Welcome.', 'red')

    def do_combat(self):

        monster = Monster(self.player.level,
                          location=self.player.location_in_wild)
        monster.generate_char(boss=False)
        combat = Combat(monster, player=self.player)
        leave = combat.combat()
        return leave

    def forest_travel(self):
        print('The rider will be making patrol trips around'
              ' these parts in case you need to get back.')
        print('You arrive at the entrance of the elder forests.')
        print('Continue?')
        choice = self.get_input()
        if choice != 'n':
            leave_forest = False
            print(
                'You travel down a loose path scattered with'
                ' leaves, howls and tweets from birds scramble your ears')
            print('When out of combat and adventuring you'
                  ' can type [Q] to leave the area.')
            while leave_forest is False:
                time.sleep(3)
                leave_forest = self.test_monster_fight(location='Forest')

    def test_monster_fight(self, location: str):
        if location == 'Forest':
            leave_forest = False
            random_occurences = ['You hear the thumps of a large'
                                 ' creature behind you. Do you dare look?',
                                 'Some foul cry was heard from'
                                 ' behind you. Do you dare look?']

            random_saves = ['You look behind and see some rocks'
                            ' fell off a hill',
                            'You look behind and see a cute'
                            ' deer was prancing around']
        else:
            leave_forest = False
            random_occurences = ['You hear the thumps of a'
                                 ' large creature behind '
                                 'you. Do you dare look?',
                                 'Some foul cry was heard'
                                 ' from behind you. Do you dare look?']

            random_saves = ['You look behind and see '
                            'some rocks fell off a hill',
                            'You look behind and see a '
                            'cute deer was prancing around']

        print(random.choice(random_occurences))
        monster_chance = random.randint(1, 100)
        choice = self.get_input()
        if 'y' in choice:
            if monster_chance > 50:
                print('You notice a monster attacking you! ')
                leave_forest = self.do_combat()
            else:
                print(random.choice(random_saves))
        elif 'give me a monster' in choice:
            monster_chance = 100
            if monster_chance > 50:
                print('You notice a monster attacking you! ')
                leave_forest = self.do_combat()
        elif 'q' in choice:

            print('You leave the', location)
            print(
                'It takes several hours before you see the rider '
                'again, it is 100 coins to get back or you can walk at')
            print('the cost having a chance of losing half of your HP.')
            self.left = False
            while self.left is False:
                choice = input('--> [W]alk [R]ide')
                choice = choice.lower()
                if 'w' in choice:
                    self.walk(False)

                if 'r' in choice:
                    self.ride()
        else:
            monster_chance += 10
            if monster_chance > 50:
                dmg = self.player.hp / 4
                print('You are ambushed by a monster. You take ' + str(dmg) +
                      ' damage!')
                self.player.hp -= dmg
                leave_forest = self.do_combat()
            else:
                print('You carry on and keep calm.')

        return leave_forest

    def ride(self):
        if self.price_check(100):
            self.player.coins -= 100
            cprint('-100 Coins', 'yellow')
            self.menu('')
        else:
            cprint("You can't afford the ride!?"
                   " What have you been doing out here!")
            self.walk(True)

    def walk(self, failed_price_check: bool):
        if failed_price_check is False:
            cprint("You don't want a ride? You might hurt yourself out there.",
                   'blue')
            cprint("No. I can walk it.", 'green')
        lose_hp_chance = random.randint(1, 100)
        if lose_hp_chance > 40:
            print('You lose half of your HP on the'
                  ' walk back to the town. You take ' + str(
                   self.player.hp / 2) + ' damage')
            self.player.hp /= 2
            self.town()
            self.left = True
        else:
            print('You make it back to town without a scratch!')
            self.town()
            self.left = True

    def story(self):
        colored_quote_one = colored("You seem lost", 'blue')
        colored_quote_two = colored("This here is Calmatian, a"
                                    " forest that houses the "
                                    "largest city in the northwest",
                                    'blue')
        colored_quote_three = colored("Would ya like a ride?", 'blue')
        colored_quote_four = colored("What is your name sir?", 'blue')
        colored_quote_five = colored("Do you have any "
                                     "proficiency in fighting? ", 'blue')
        # colored_quote_six = colored
        # ("Now, the first travel is free but afterwards
        #  you better start giving some coins.")
        # colored_quote_seven = colored("You can take
        #  a job from the townspeople or the bounty boards in town.")
        player_quote_one = colored("Where am I?", 'green')
        player_quote_two = colored("Yes I was a [Archer] or [Knight]", 'green')
        # player_quote_three = colored("How will I get more coins?")

        # print("It's been a very long time since the days of the crackening.")
        # time.sleep(3)
        # print("The world tore asunder from the Godking Uvera's Blade.")
        # time.sleep(3)
        # print("You once were an archangel working for
        # Uvera until he turned and betrayed his fellow kings.")
        # time.sleep(3)
        # print("Thrown out of the heavens you land upon
        #  the earthen realm. Your realms and gear torn into shreds and",
        #       "worthless, your weapon bent and blunt.")
        # time.sleep(6.3)
        cprint(
            'A clopping of wolves meets your attention. ' + colored_quote_one +
            ' the rider said, he wore leather and iron clad armor.')
        time.sleep(3)
        print(
            '' + player_quote_one +
            ', you barely got the words out of your mouth ' +
            colored_quote_two + '')
        time.sleep(3)
        print('You rose to your knees. The rider spoke again ' +
              colored_quote_three + ' you grunted.')
        time.sleep(3)
        cprint(colored_quote_four)
        name_in = input()
        cprint(colored_quote_five + player_quote_two)
        player_class_in = input()
        player_class_in = player_class_in.lower()
        while player_class_in != 'archer' and player_class_in != 'knight':
            print('Pick a real class, Archer or Knight')
            player_class_in = input()
            player_class_in = player_class_in.lower()
        if player_class_in == 'archer':
            player_class_in = 'Archer'
        else:
            player_class_in = 'Knight'
        self.generate_character(name_in, player_class_in)


if __name__ == '__main__':
    WELCOME = """
 -------------------------------
|                               |
|      Wolves Bats Rocks        |
|                               |
|   The Wolf Rider Greets You.  |
|                               |
 -------------------------------
    """
    print(WELCOME)
    MAIN = Main()
    MAIN.story()
    MAIN.menu(welcome_sign="Alright, where would you like to go")
