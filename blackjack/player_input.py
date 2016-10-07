import bankroll


class PlayerInput(object):
    """Container for player input functions."""

    def __init__(self, time):
        """Creates a new player input container.

        Args:
            time: A time interface.
        """
        self._time = time

    def welcome_and_get_buyin(self, input_func=raw_input):
        """Welcomes the player to the game and returns buy-in amount.

        Args:
            input_func: Function to receive input from the user.
        """
        print ("\nWelcome to Shetty Casino blackjack! We're thrilled to take "
               "your mon...I mean...we're thrilled to have you here playing "
               "with us!\n")
        print ("The rules of blackjack can be found here: \n\n"
               "http://www.bicyclecards.com/how-to-play/blackjack/ \n\nIn "
               "addition, we have some house rules: We don't offer insurance, "
               "we only allow one split per hand, and we don't allow doubling "
               "down after a split.")
        while True:
            try:
                buy_in = int(input_func("\nHow much would you like to buy in "
                            "for? Please choose a whole dollar amount between "
                            "$500 and $50000: $"))
                break
            except ValueError:
                print "\nIntegers only, please!\n"
                self._time.sleep(2)


        while not 500 <= buy_in <= 50000:
            while True:
                try:
                    buy_in = int(input_func("Please enter a buy-in amount "
                                "between $500 and $50,000 only, please: $"))
                    break
                except ValueError:
                    print "\nIntegers, only, please.\n"
                    self._time.sleep(2)
        return buy_in


    def bet(self, input_func=raw_input):
        """Acquires and returns bet size from the user.

        Args:
            input_func: Function to receive input from the user.
        """
        while True:
            try:
                bet = int(input_func("\nHow much would you like to wager? Whole"
                                 " dollar amounts between %s and %s only, "
                                 "please: " % (
                                 bankroll.MIN_BET, bankroll.MAX_BET)))
                break
            except ValueError:
                print "\nInteger values only, please!\n"
                self._time.sleep(2)
        while not (bankroll.MIN_BET <= bet <= bankroll.MAX_BET):
            while True:
                try:
                    bet = int(input_func("Please enter your wager again. Only "
                                        "whole dollar amounts between %s and "
                                        "%s: " % (
                                        bankroll.MIN_BET, bankroll.MAX_BET)))
                    break
                except ValueError:
                    print "\n Integer values only, please!\n"
                    self._time.sleep(2)

        return bet

    def action(self, hand, input_func=raw_input):
        """Acquires and returns desired player action.

        Args:
            hand: The hand for which the action is being requested.
            input_func: Function to receive input from the user.
        """
        if hand.double_down_allowed() and hand.split_allowed():
            allowed_actions = ['h', 'st', 'sp', 'd']
            action = input_func("Would you like to [h]it, [st]and, [sp]lit, or "
                                "[d]ouble down? ")
            while action not in allowed_actions:
                action = input_func("Please choose your action from the "
                                    "following options: 'h' to hit, 'st' to "
                                    "stand, 'sp' to split, or 'd' to double "
                                    ": ")

        if hand.double_down_allowed() and not hand.split_allowed():
            allowed_actions = ['h', 'st', 'd']
            action = input_func("Would you like to [h]it, [st]and, or [d]ouble "
                                "down? ")
            while action not in allowed_actions:
                action = input_func("Please choose your action from the "
                                    "following options: 'h' to hit, 'st' to "
                                    "stand, or 'd' to double down: ")

        if not hand.double_down_allowed() and not hand.split_allowed():
            allowed_actions = ['h', 'st']
            action = input_func("Would you like to [h]it or [st]and? ")
            while action not in allowed_actions:
                action = input_func("Please choose your action from the "
                                    "following options: 'h' to hit or 'st' to "
                                    "stand. ")

        return action

    def play_another_round(self, bankroll_balance, input_func=raw_input):
        """Returns True if the player would like to continue playing.

        Args:
            bankroll_balance: Current bankroll balance.
            input_func: Function to receive input from the user.
        """
        print "\nAfter the last round, your current bankroll is $%s." % (
            bankroll_balance)
        keep_playing = input_func("\nWould you like to continue playing ([y]es "
                                  "or [n]o)? ")
        while keep_playing != 'y' and keep_playing != 'n':
            keep_playing = input_func("\nPlease enter 'y' to continue playing, "
                                      "or 'n' to quit: ")

        if keep_playing == 'y':
            return True
        elif keep_playing == 'n':
            return False


    def rebuy(self, bankroll_balance, input_func=raw_input):
        """Returns True if player wants to rebuy, false otherwise.

        Args:
            bankroll_balance: Current bankroll balance.
            input_func: Function to receive input from the user.
        """
        rebuy = input_func("\nYour current bankroll is $%s. Would you like to "
                           "rebuy ([y]es or [n]o)? " % (bankroll_balance))
        while rebuy != 'y' and rebuy != 'n':
            rebuy = input_func("\nPlease enter 'y' if you would like to rebuy, "
                               "or 'n' if you would not: ")
        if rebuy == 'y':
            return True
        elif rebuy == 'n':
            return False

    def rebuy_amount(self, input_func=raw_input):
        """Returns user-entered rebuy amount.

        Args:
            input_func: Function to receive input from the user.
        """
        while True:
            try:
                rebuy_amount = int(input_func("\nHow much would you like to "
                                          "rebuy for? Please enter a whole "
                                          "dollar amount between $500 and "
                                          " $50000: "))
                break
            except ValueError:
                print "\nIntegers only, please."

        while not 500 <= rebuy_amount <= 50000:
            while True:
                try:
                    rebuy_amount = int(input_func("\nPlease enter a rebuy amount "
                                "between $500 and $50,000 only, please: $"))
                    break
                except ValueError:
                    print "\nIntegers, only, please."
                    self._time.sleep(2)
        return rebuy_amount

    def wait_for_enter(self, input_func=raw_input):
        """Prompts the player to hit Enter before the game continues.

        Args:
            input_func: Function to receive input from the user.
        """
        input_func("\nPress Enter to continue.")
