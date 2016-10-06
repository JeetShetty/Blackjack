import card


class Deck(object):
    """A representation of a deck of playing cards."""

    def __init__(self, card=card.Card):
        """Creates a new unshuffled deck.

        Args:
            card: A playing card representation.
        """
        self.cards = []
        suits = ['s', 'h', 'd', 'c']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q',
                 'K']

        for suit in suits:
            for rank in ranks:
                self.cards.append(card(rank,suit))
