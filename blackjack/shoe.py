import random
import deck


class Shoe(object):
    """A blackjack shoe interface."""

    def __init__(self, deck, shoe_size=6, shuffle_function=random.shuffle):
        """Creates a new shuffled shoe.

        Args:
            deck: An instance of a deck of playing cards.
            shoe_size: An int between 4 and 8 indicating the number of decks
                that will be in the shoe.
            shuffle_function: An in-place shuffling function.
        """
        self._shoe_size = shoe_size
        self._cards = shoe_size * deck.cards
        shuffle_function(self._cards)

    def deal_card(self):
        """Deals a card out of the shoe."""
        return self._cards.pop()

    def shoe_finished(self):
        """Returns True if shoe is finished, False otherwise."""
        if len(self._cards) <= (0.25 * 52 * self._shoe_size):
            print ("The current shoe is finished! We'll shuffle and continue "
                   "with a new one.")
            return True
        else:
            return False