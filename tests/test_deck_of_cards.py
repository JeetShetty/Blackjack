import unittest

import mock

from blackjack import deck_of_cards


class DeckTest(unittest.TestCase):

    def test_unshuffled_deck(self):
        mock_card = mock.Mock()
        mock_card.side_effect = lambda x,y: (x, y)
        unshuffled_deck = deck_of_cards.Deck(mock_card)

        self.assertEqual(len(unshuffled_deck.cards), 52)
        self.assertEqual(unshuffled_deck.cards[5][0], '6')
        self.assertEqual(unshuffled_deck.cards[5][1], 's')
        self.assertEqual(unshuffled_deck.cards[19][0], '7')
        self.assertEqual(unshuffled_deck.cards[19][1], 'h')
        self.assertEqual(unshuffled_deck.cards[38][0], 'K')
        self.assertEqual(unshuffled_deck.cards[38][1], 'd')
        self.assertEqual(unshuffled_deck.cards[49][0], 'J')
        self.assertEqual(unshuffled_deck.cards[49][1], 'c')
