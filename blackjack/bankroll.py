MIN_BET = 25
MAX_BET = 1000


class Bankroll(object):
    """Representation of the player's bankroll."""

    def __init__(self, buy_in):
        """Creates a new bankroll.

        Args:
            buy_in: An int of the amount that the player buys in for.
        """
        self.balance = buy_in

    def adjust_balance(self, amount):
        """Adds to or subtracts from the bankroll balance.

        Args:
            amount: Amount to be added to the bankroll balance.
        """
        self.balance += amount

    def rebuy_necessary(self):
        """Returns True if the player must rebuy, false otherwise."""
        if self.balance < MIN_BET:
            return True
        else:
            return False

