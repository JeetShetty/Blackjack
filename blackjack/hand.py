_MAX_SPLITS_ALLOWED = 1


class Hand(object):
    """A representation of a blackjack hand."""

    def __init__(self, split=False, split_card=None, split_count=0):
        """Deals a new blackjack hand and stores it as a tuple.

        Args:
            shoe: A blackjack shoe interface.
            split: A boolean indicating whether the hand is a result of a split
            split_card: The card that was in the split hand that will now make
                up the new hand.
        """
        self.split_count = split_count
        self.split_aces = False
        self._ace_count = 0
        self._doubled_down = False
        self._cards = ()

        if split:
            self._cards = split_card,
            if self._cards[0].rank == 'A':
                self._ace_count += 1
                self.split_aces = True
            self.split_count += 1

    def deal_hand(self, shoe):
        """Deals a new 2 card blackjack hand.

        Args:
            shoe: Blackjack shoe that cards are dealt from.
        """
        self._cards = (shoe.deal_card(), shoe.deal_card())
        for card in self._cards:
            if card.rank == 'A':
                self._ace_count += 1

    def hit(self, shoe):
        """Adds a card to the hand when the player or dealer hits.

        Args:
            shoe: Blackjack shoe that cards are dealt from.
        """
        self._cards += shoe.deal_card(),
        if self._cards[-1].rank == 'A':
            self._ace_count += 1

    def hand_value(self):
        """Returns the blackjack hand value."""
        hand_value = 0
        for card in self._cards:
            hand_value += card.value()
        if hand_value > 21 and self._ace_count > 0:
            aces_left = self._ace_count
            while aces_left > 0:
                hand_value -= 10
                if hand_value <= 21:
                    break
                aces_left -= 1
        return hand_value

    def display_hand(self):
        """Returns the cards in the hand in the form of 'RsRs...'."""
        cards = ""
        for card in self._cards:
            cards += card.rank + card.suit
        return cards

    def display_one_dealer_card(self):
        """Returns the first card as a string in the form 'Rs'"""
        return self._cards[0].rank + self._cards[0].suit

    def split(self):
        """Splits a two card hand and returns two one card hands."""
        card_one = self._cards[0]
        card_two = self._cards[1]
        hand_one = Hand(True, card_one, self.split_count)
        hand_two = Hand(True, card_two, self.split_count)
        return hand_one, hand_two

    def split_allowed(self):
        """Returns True if split is allowed, otherwise False."""
        if len(self._cards) == 2 and (
            self.split_count < _MAX_SPLITS_ALLOWED) and (
            self._cards[0].rank == self._cards[1].rank):
                return True
        else:
            return False

    def double_down_allowed(self):
        """Returns True if double down is allowed, False otherwise."""
        if len(self._cards) == 2 and self.split_count == 0 and (
            self._doubled_down is False):
                return True
        else:
            return False