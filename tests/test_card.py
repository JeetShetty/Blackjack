from __future__ import absolute_import
import unittest

from blackjack import card


class CardTest(unittest.TestCase):

    def test_blackjack_values(self):
        jack_of_hearts = card.Card('J', 'h')
        ace_of_spades = card.Card('A', 's')
        five_of_hearts = card.Card('5', 'h')

        self.assertEqual(jack_of_hearts.value(), 10)
        self.assertEqual(ace_of_spades.value(), 11)
        self.assertEqual(five_of_hearts.value(), 5)

    def test_is_ace(self):
        ace = card.Card('A', 's')
        non_ace = card.Card('5', 's')

        self.assertTrue(ace.is_ace())
        self.assertFalse(non_ace.is_ace())
