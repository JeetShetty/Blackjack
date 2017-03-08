import unittest

import mock

from blackjack import hand


class TestHand(unittest.TestCase):

    def test_deal_hand(self):
        mock_shoe = mock.Mock()
        mock_card_one = mock.Mock()
        mock_card_two = mock.Mock()
        bj_hand = hand.Hand()
        mock_shoe.deal_card.side_effect = [mock_card_one, mock_card_two]
        bj_hand.deal_hand(mock_shoe)
        self.assertEqual(bj_hand._cards, (mock_card_one, mock_card_two))

    def test_hit(self):
        mock_shoe = mock.Mock()
        mock_card = mock.Mock()
        mock_shoe.deal_card.return_value = mock_card
        bj_hand = hand.Hand()
        bj_hand.hit(mock_shoe)
        self.assertEqual(bj_hand._cards, (mock_card,))

    def test_ace_count(self):
        mock_shoe = mock.Mock()
        mock_non_ace = mock.Mock()
        mock_ace_one = mock.Mock()
        mock_ace_two = mock.Mock()
        mock_ace_one.rank = 'A'
        mock_ace_two.rank = 'A'
        mock_shoe.deal_card.side_effect = [mock_non_ace, mock_ace_one,
                                           mock_ace_two]
        bj_hand = hand.Hand()
        bj_hand.deal_hand(mock_shoe)
        self.assertEqual(bj_hand._ace_count, 1)

        bj_hand.hit(mock_shoe)
        self.assertEqual(bj_hand._ace_count, 2)

    def test_split(self):
        mock_shoe = mock.Mock()
        mock_card_one = mock.Mock()
        mock_card_two = mock.Mock()
        mock_shoe.deal_card.side_effect = [mock_card_one, mock_card_two]
        bj_hand = hand.Hand()
        bj_hand.deal_hand(mock_shoe)

        new_hand_one, new_hand_two = bj_hand.split()
        self.assertEqual(new_hand_one._cards, (mock_card_one,))
        self.assertEqual(new_hand_two._cards, (mock_card_two,))

    def test_hand_value_without_aces(self):
        mock_shoe = mock.Mock()
        mock_card_one = mock.Mock()
        mock_card_two = mock.Mock()
        mock_card_one.value.return_value = 8
        mock_card_two.value.return_value = 7
        mock_shoe.deal_card.side_effect = [mock_card_one, mock_card_two]
        bj_hand = hand.Hand()
        bj_hand.deal_hand(mock_shoe)

        hand_value = bj_hand.hand_value()
        self.assertEqual(hand_value, 15)

    def test_hand_value_with_ace(self):
        mock_shoe = mock.Mock()
        mock_card_one = mock.Mock()
        mock_card_two = mock.Mock()
        mock_card_one.rank = 'A'
        mock_card_one.value.return_value = 11
        mock_card_two.value.return_value = 12
        mock_shoe.deal_card.side_effect = [mock_card_one, mock_card_two]
        bj_hand = hand.Hand()
        bj_hand.deal_hand(mock_shoe)

        hand_value = bj_hand.hand_value()
        self.assertEqual(hand_value, 13)

    def test_hand_value_with_multiple_aces(self):
        mock_shoe = mock.Mock()
        mock_card_one = mock.Mock()
        mock_card_two = mock.Mock()
        mock_card_three = mock.Mock()
        mock_card_one.rank = 'A'
        mock_card_two.rank = 'A'
        mock_card_one.value.return_value = 11
        mock_card_two.value.return_value = 11
        mock_card_three.value.return_value = 8
        mock_shoe.deal_card.side_effect = [mock_card_one, mock_card_two,
                                           mock_card_three]
        bj_hand = hand.Hand()
        bj_hand.deal_hand(mock_shoe)
        bj_hand.hit(mock_shoe)

        hand_value = bj_hand.hand_value()
        self.assertEqual(hand_value, 20)

    def test_hand_value_with_multiple_aces(self):
        mock_shoe = mock.Mock()
        mock_card_one = mock.Mock()
        mock_card_two = mock.Mock()
        mock_card_three = mock.Mock()
        mock_card_one.rank = 'A'
        mock_card_two.rank = 'A'
        mock_card_one.value.return_value = 11
        mock_card_two.value.return_value = 11
        mock_card_three.value.return_value = 15
        mock_shoe.deal_card.side_effect = [mock_card_one, mock_card_two,
                                           mock_card_three]
        bj_hand = hand.Hand()
        bj_hand.deal_hand(mock_shoe)
        bj_hand.hit(mock_shoe)

        hand_value = bj_hand.hand_value()
        self.assertEqual(hand_value, 17)

    def test_number_of_splits(self):
        mock_shoe = mock.Mock()
        mock_card = mock.Mock()
        mock_shoe.deal_card.return_value = mock_card
        bj_hand = hand.Hand()
        bj_hand.deal_hand(mock_shoe)
        bj_hand_two, dummy = bj_hand.split()
        bj_hand_two.hit(mock_shoe)
        # first split should be allowed, second should not.
        self.assertEqual(2, len(bj_hand._cards), len(bj_hand_two._cards))
        self.assertTrue(bj_hand.split_allowed())
        self.assertFalse(bj_hand_two.split_allowed())

    def test_number_of_cards_for_split(self):
        mock_shoe = mock.Mock()
        mock_card = mock.Mock()
        mock_shoe.deal_card.return_value = mock_card
        bj_hand = hand.Hand()
        bj_hand.deal_hand(mock_shoe)
        #two card hand can split
        self.assertLess(bj_hand._split_count, 2)
        self.assertTrue(bj_hand.split_allowed())
        bj_hand.hit(mock_shoe)
        #three card hand cannot split
        self.assertLess(bj_hand._split_count, 2)
        self.assertFalse(bj_hand.split_allowed())

    def test_rank_equal_split_allowed(self):
        mock_shoe = mock.Mock()
        mock_card_one = mock.Mock()
        mock_card_two = mock.Mock()
        mock_card_one.rank = '5'
        mock_card_two.rank = '5'
        mock_shoe.deal_card.side_effect = [mock_card_one, mock_card_two]
        bj_hand = hand.Hand()
        bj_hand.deal_hand(mock_shoe)

        self.assertLess(bj_hand._split_count, 2)
        self.assertEqual(2, len(bj_hand._cards))
        self.assertTrue(bj_hand.split_allowed())

    def test_rank_unequal_split_not_allowed(self):
        mock_shoe = mock.Mock()
        mock_card_one = mock.Mock()
        mock_card_two = mock.Mock()
        mock_card_one.rank = '5'
        mock_card_two.rank = '6'
        mock_shoe.deal_card.side_effect = [mock_card_one, mock_card_two]
        bj_hand = hand.Hand()
        bj_hand.deal_hand(mock_shoe)

        self.assertLess(bj_hand._split_count, 2)
        self.assertEqual(2, len(bj_hand._cards))
        self.assertFalse(bj_hand.split_allowed())

    def test_double_down_allowed(self):
        mock_shoe = mock.Mock()
        mock_card = mock.Mock()
        mock_shoe.deal_card.return_value = mock_card
        bj_hand = hand.Hand()
        bj_hand.deal_hand(mock_shoe)
        self.assertTrue(bj_hand.double_down_allowed())

    def test_double_down_not_allowed_after_split(self):
        mock_shoe = mock.Mock()
        mock_card = mock.Mock()
        mock_shoe.deal_card.return_value = mock_card
        bj_hand = hand.Hand()
        bj_hand.deal_hand(mock_shoe)
        split_hand, dummy = bj_hand.split()
        split_hand.hit(mock_shoe)
        self.assertFalse(split_hand.double_down_allowed())

    def test_double_down_not_allowed_after_hit(self):
        mock_shoe = mock.Mock()
        mock_card = mock.Mock()
        mock_shoe.deal_card.return_value = mock_card
        bj_hand = hand.Hand()
        bj_hand.deal_hand(mock_shoe)
        bj_hand.hit(mock_shoe)
        self.assertFalse(bj_hand.double_down_allowed())
