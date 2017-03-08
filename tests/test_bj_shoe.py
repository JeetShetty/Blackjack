from __future__ import absolute_import
import unittest

import mock

from blackjack import bj_shoe


class TestShoe(unittest.TestCase):

    def shuffle(self, x):
        x[0], x[-1] = x[-1], x[0]

    def test_shoe_creation(self):
        mock_deck = mock.Mock()
        shoe_size = 2
        mock_shuffle_function = mock.Mock()
        mock_deck.cards = [0, 1, 2]
        mock_shuffle_function.side_effect = self.shuffle
        shoe = bj_shoe.Shoe(mock_deck, shoe_size, mock_shuffle_function)

        self.assertEqual(shoe._cards, [2, 1, 2, 0, 1, 0])

    def test_deal_card(self):
        mock_deck = mock.Mock()
        shoe_size = 2
        mock_shuffle_function = mock.Mock()
        mock_deck.cards = [0, 1, 2]
        shoe = bj_shoe.Shoe(mock_deck, shoe_size, mock_shuffle_function)

        self.assertEqual(shoe.deal_card(), 2)