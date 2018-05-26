from termcolor import cprint, colored
import random
import time


class Tavern:

    def __init__(self, player):
        self.player = player
        # self.locations = {'Main': 0,
        #                   'Bar': 1,
        #                   'Booth': 2,
        #                   'Inn': 3,
        #                   'Profile': 4,
        #                   'Save Game': 5,
        #                   'Load Game': 6,
        #                   'Exiting': 7}

        self.choices = ['[B]eer',
                        '[R]ide',
                        '[I]nn',
                        '[V]iew Stats',
                        '[S]ave Game',
                        '[L]oad Game',
                        '[E]xit',
                        ]

        # self.current_location = self.locations['Main']

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

    def price_check(self, coins: int):
        """
        Checks if the player has enough coins
        :param coins: If the player has more coins than this, return true
        :return: True or False
        """
        if self.player.coins >= coins:
            return True

    def beer(self):
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
            return 'exit'
        elif self.price_check(10) is False and 'y' in confirmation:
            cprint(
                "You can't afford a damn drink get out of here!",
                'yellow')
            return 'exit'

        else:
            cprint('Never-mind.', 'green')
            return 'exit'

    def main(self):
        print('The bar tender greets you and asks what do you need.')
        left = False
        while left is False:
            cprint("Aye, ya look like 'er in desperate needs of"
                   " a drink! What can I do ya for?", 'yellow')

            for option in self.choices:
                cprint("| " + option, 'yellow')
            choice = self.get_input()
            if choice == 'beer' or 'b':
                return self.beer()
            elif 'ride' or 'r':
                return self.booth_entrance()

    def booth_entrance(self):
        cprint('A ride? You can talk to that gentleman'
               ' over there, he has a wolf that you can use.',
               'yellow')
        cprint('How much will it cost?', 'green')
        cprint('Around hundred coins per ride.', 'yellow')
        print('Continue?')
        choice = self.get_input()
        if 'y' in choice:
            self.booth()
        else:
            cprint('Never mind, I am good thanks.', 'green')
            time.sleep(2)
            return 'exit'

    def ride(self):
        if self.price_check(100):
            cprint('-100 coins', 'yellow')
            self.player.coins -= 100
            return 'menu'
        else:
            cprint('What do you mean you do '
                   'not have enough? Get out of here!',
                   'blue')
            return 'exit'

    def booth(self):

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
                self.ride()
            else:
                cprint('Quit wasting my time and '
                       'get out of my sight.', 'blue')
        else:
            self.boss_ride()

    def boss_ride(self):
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
            return 'boss'

        if 'c' in choice:

            print('Are you sure you want'
                  ' to spend 100 coins? You have ' + str(
                   self.player.coins) + ' coins')
            choice = input('-->')
            choice = choice.lower()
            if 'y' in choice:
                self.ride()
            else:
                cprint('Quit wasting my time'
                       ' and get out of my sight.', 'blue')
