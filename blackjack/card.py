class Card(object):
    """A representation of a playing card."""

    def __init__(self, rank, suit):
        """Creates a new card instance.

        Args:
            rank: String of the rank of the card.
            suit: Strint of the suit of the card.
        """
        self.rank = rank
        self.suit = suit

    def value(self):
        """Returns the blackjack value of a card."""
        if self.rank in ['T','J','Q','K']:
            return 10
        elif self.rank == 'A':
            return 11  # possible value of 1 accounted for by Hand class
        else:
            return int(self.rank)

    def is_ace(self):
        """Returns true if the card is an ace, false otherwise."""
        if self.rank == 'A':
            return True
        else:
            return False