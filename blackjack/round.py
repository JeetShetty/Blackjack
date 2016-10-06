import time

import hand
import player_input


class Round(object):
    """A container for a round of blackjack hands."""

    def __init__(self, time, player_input, bankroll):
        """Creates a new round of blackjack hands.

        Args:
            time: A time interface.
            player_input: A container for player input functions.
            bankroll: Player bankroll.
        """
        self._time = time
        self._player_input = player_input
        self._bankroll = bankroll
        self._player_hands = []
        self._dealer_hand = None
        self._bet = None
        self.player_natural = False
        self.dealer_natural = False

    def place_bet(self):
        """Gets the dollar bet amount from the user."""
        self._bet = self._player_input.bet()
        if self._bet > self._bankroll.balance:
            print ("\nYou don't currently have enough money to make this bet, "
                   "but for such a good customer we'll provide you with a "
                   "marker for the remainder of the hand.")
        self._time.sleep(2)

    def deal_hands(self, shoe):
        """Deals hands to both the player and the dealer.

        Sets natural attributes to True if there are any.

        Args:
            shoe: The shoe in use for this round.
            hand_instantiator: Function to create a new hand instance.
        """
        self._dealer_hand = hand.Hand()
        self._dealer_hand.deal_hand(shoe)
        self._player_hands.append(hand.Hand())
        self._player_hands[0].deal_hand(shoe)

        self.dealer_natural = self._dealer_hand.hand_value() == 21
        self.player_natural = self._player_hands[0].hand_value() == 21

    def display_dealer_hand(self, player_action_finished):
        """Prints the dealer's hand.

        Args:
            player_action_finished: Boolean indicating if the player has
                finished acting on their hand.
        """
        print "\nDealer's hand: ",
        if player_action_finished:
            self._dealer_hand.display_hand()
        else:
            self._dealer_hand.display_one_dealer_card()

    def display_player_hands(self):
        """Prints player hands."""
        print "\nYour hand: ",
        for hand in self._player_hands:
            hand.display_hand()

    def _double_down(self):
        """Doubles the bet when the player doubles down."""
        self._bet *= 2
        if self._bet > self._bankroll.balance:
            print ("\nYou don't currently have enough money to make this bet, "
                   "but for such a good customer we'll provide you with a "
                   "marker for the remainder of the hand.")
            self._time.sleep(2)
        self._player_hands[0]._doubled_down = True

    def play_through_player_hands(self, shoe):
        """Plays through player hands so that they are ready for showdown.

        Returns a boolean indicating whether the playthrough of the dealer's
        hand can be skipped.

        Args:
            shoe: Blackjack shoe.
        """
        skip_dealer_playthrough = False
        print "\nHand: ",
        self._player_hands[0].display_hand()
        action = self._player_input.action(self._player_hands[0])

        if action == 'st':
            print "\nYour final hand value is %s" % (
                    self._player_hands[0].hand_value())
            return skip_dealer_playthrough

        elif action == 'sp':
            if self._bankroll.balance < 2 * self._bet:
                print ("\nYou don't currently have enough money to make this bet, "
                       "but for such a good customer we'll provide you with a "
                       "marker for the remainder of the hand.")
                self._time.sleep(2)
            new_hand_one, new_hand_two = self._player_hands[0].split()
            self._player_hands.remove(self._player_hands[0])
            self._player_hands.append(new_hand_one)
            self._player_hands.append(new_hand_two)

        elif action == 'd':
            self._double_down()
            self._player_hands[0].hit(shoe)
            hand_value = self._player_hands[0].hand_value()
            print "\nYour final hand is: ",
            self._player_hands[0].display_hand()
            print "\nYour final hand value is %s" % (hand_value)
            if hand_value > 21:
                skip_dealer_playthrough = True
            return skip_dealer_playthrough

        elif action == 'h':
            self._player_hands[0].hit(shoe)

        for hand in self._player_hands:
            while True:
                hand_value = hand.hand_value()
                if hand_value >= 21:
                    print "\nYour final hand is ",
                    self._player_hands[0].display_hand()
                    print "\nYour final hand value is %s" % (hand_value)
                    if hand_value > 21:
                        print "Unfortunately you busted."
                        if hand._split_count == 0:
                            skip_dealer_playthrough = True
                    break
                print "Hand: ",
                hand.display_hand()
                action = self._player_input.action(hand)
                if action == 'h':
                    hand.hit(shoe)
                elif action == 'st':
                    print "\nYour final hand value is %s" % (hand_value)
                    break

        return skip_dealer_playthrough

    def play_through_dealer_hand(self, shoe):
        """Plays through the dealer hand.

        Args:
            shoe: Blackjack shoe
        """
        self._player_input.wait_for_enter()
        print "\nDealer's hand: ",
        self._dealer_hand.display_hand()
        if self._dealer_hand.hand_value() >= 17:
            pass
        else:
            while self._dealer_hand.hand_value() < 17:
                self._dealer_hand.hit(shoe)
                print "Dealer hits."
                self._time.sleep(2)
                print "Dealer's hand: ",
                self._dealer_hand.display_hand()

        self._time.sleep(2)
        if self._dealer_hand.hand_value() <= 21:
            print "Dealer stands at %s." % (self._dealer_hand.hand_value())
        else:
            print "Dealer busts at %s." % (self._dealer_hand.hand_value())

    def showdown(self):
        """Shows down hands and returns amount won by player."""
        self._player_input.wait_for_enter()
        amount_won = 0

        if self.player_natural:
            if not self.dealer_natural:
                amount_won += 1.5 * self._bet
                print "You were dealt a natural and win!"
            else:
                print ("Both you and the dealer were dealt naturals. You get "
                       "your bet back.")
            return amount_won

        if self.dealer_natural:
            if not self.player_natural:
                amount_won -= self._bet
                print "Dealer was dealt a natural and wins this hand."
            return amount_won

        dealer_hand_value = self._dealer_hand.hand_value()
        for hand in self._player_hands:
            player_hand_value = hand.hand_value()
            if player_hand_value > 21:
                amount_won -= self._bet
            elif player_hand_value <= 21:
                if dealer_hand_value > 21:
                    amount_won += self._bet
                elif dealer_hand_value <= 21:
                    if player_hand_value > dealer_hand_value:
                        amount_won += self._bet
                        print ("\nCongratulations! Your hand value of %s beats "
                               "the dealer's hand value of %s" % (
                               player_hand_value, dealer_hand_value))
                    elif dealer_hand_value > player_hand_value:
                        print ("\nUnfortunately, your hand value of %s loses "
                              "to the dealer's hand value of %s." % (
                              player_hand_value, dealer_hand_value))
                        amount_won -= self._bet

        if amount_won == 0:
            print "\nYou broke even this round."
        elif amount_won > 0:
            print "\nYou won $%s this round." % (amount_won)
        elif amount_won < 0:
            print "\nYou lost $%s this round." % (-amount_won)
        return amount_won
