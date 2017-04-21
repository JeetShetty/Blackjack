import unittest

import mock

from blackjack import round


class TestRound(unittest.TestCase):

    def setUp(self):
        self.mock_time = mock.Mock()
        self.mock_shoe = mock.Mock()
        self.mock_bankroll = mock.Mock()

    def test_deal_hands_dealer_natural(self):
        mock_player_input = mock.Mock()
        mock_hand_generator = mock.Mock()
        mock_hand_one = mock.Mock()
        mock_hand_two = mock.Mock()
        mock_hand_generator.side_effect = [mock_hand_one, mock_hand_two]
        mock_hand_one.hand_value.return_value = 21
        mock_hand_two.hand_value.return_value = 15
        bj_round = round.Round(self.mock_time, mock_player_input,
                               self.mock_bankroll)
        bj_round.deal_hands(self.mock_shoe, mock_hand_generator)
        self.assertEqual(bj_round._dealer_hand, mock_hand_one)
        self.assertEqual(bj_round._player_hands, [mock_hand_two])
        self.assertTrue(bj_round.dealer_natural)
        self.assertFalse(bj_round.player_natural)

    def test_deal_hands_player_natural(self):
        mock_player_input = mock.Mock()
        mock_hand_generator = mock.Mock()
        mock_hand_one = mock.Mock()
        mock_hand_two = mock.Mock()
        mock_hand_generator.side_effect = [mock_hand_one, mock_hand_two]
        mock_hand_one.hand_value.return_value = 15
        mock_hand_two.hand_value.return_value = 21
        bj_round = round.Round(self.mock_time, mock_player_input,
                               self.mock_bankroll)
        bj_round.deal_hands(self.mock_shoe, mock_hand_generator)
        self.assertEqual(bj_round._dealer_hand, mock_hand_one)
        self.assertEqual(bj_round._player_hands, [mock_hand_two])
        self.assertFalse(bj_round.dealer_natural)
        self.assertTrue(bj_round.player_natural)

    def test_double_down(self):
        mock_player_input = mock.Mock()
        mock_player_input.bet.return_value = 250
        mock_hand = mock.Mock()
        bj_round = round.Round(self.mock_time, mock_player_input,
                               self.mock_bankroll)
        bj_round._player_hands = [mock_hand]
        bj_round.place_bet()
        bj_round._double_down()
        self.assertEqual(bj_round._bet, 500)

    def test_play_through_split_hand(self):
        mock_player_input = mock.Mock()
        mock_hand_one = mock.Mock()
        mock_hand_two = mock.Mock()
        mock_hand_three = mock.Mock()
        mock_hand_one.split_aces = mock_hand_two.split_aces = (
            mock_hand_three.split_aces) = False

        bj_round = round.Round(self.mock_time, mock_player_input,
                               self.mock_bankroll)
        bj_round._player_hands = [mock_hand_one]
        mock_player_input.action.side_effect = ['sp', 'h', 'st', 'st']
        mock_hand_one.split.return_value = mock_hand_two, mock_hand_three
        mock_hand_two.hand_value.return_value = 15
        mock_hand_three.hand_value.return_value = 15
        mock_hand_one.display_hand.return_value = ''
        mock_hand_two.display_hand.return_value = ''
        mock_hand_three.display_hand.return_value = ''
        bj_round._bet = 1
        bj_round.play_through_player_hands(self.mock_shoe)

        self.assertEqual(bj_round._player_hands,
                         [mock_hand_two, mock_hand_three])
        self.assertEqual(mock_hand_two.hit.call_count, 1)
        self.assertFalse(mock_hand_three.hit.called)

    def test_play_through_stand(self):
        mock_player_input = mock.Mock()
        mock_hand = mock.Mock()
        mock_hand.split_aces = False
        bj_round = round.Round(self.mock_time, mock_player_input,
                               self.mock_bankroll)
        bj_round._player_hands = [mock_hand]
        mock_hand.hand_value.return_value = 15
        mock_hand.display_hand.return_value = ''
        mock_player_input.action.return_value = 'st'
        bj_round.play_through_player_hands(self.mock_shoe)

        self.assertFalse(mock_hand.hit.called)
        self.assertFalse(mock_hand.split.called)

    def test_play_through_hit_once_and_bust(self):
        mock_player_input = mock.Mock()
        mock_hand = mock.Mock()
        mock_hand.split_aces = False
        bj_round = round.Round(self.mock_time, mock_player_input,
                               self.mock_bankroll)
        bj_round._player_hands = [mock_hand]
        mock_hand.hand_value.return_value = 22
        mock_hand.display_hand.return_value = ''
        mock_player_input.action.return_value = 'h'
        bj_round.play_through_player_hands(self.mock_shoe)

        self.assertFalse(mock_hand.split.called)
        self.assertEqual(mock_hand.hit.call_count, 1)

    def test_play_through_split_aces(self):
        mock_hand_one = mock.Mock()
        mock_hand_two = mock.Mock()
        mock_hand_one.split_aces = mock_hand_two.split_aces = True
        bj_round = round.Round(self.mock_time, None, self.mock_bankroll)
        bj_round._player_hands = [mock_hand_one, mock_hand_two]
        bust = bj_round.play_through_player_hands(self.mock_shoe)

        self.assertFalse(bust)
        mock_hand_one.hit.assert_called_once()
        mock_hand_two.hit.assert_called_once()

    def increase_hand_value(self, x):
        self.hand_value += 5

    def test_play_through_dealer_hand_dealer_hits(self):
        mock_player_input = mock.Mock()
        mock_hand = mock.Mock()
        bj_round = round.Round(self.mock_time, mock_player_input,
                               self.mock_bankroll)
        bj_round._dealer_hand = mock_hand
        self.hand_value = 15
        mock_hand.hand_value.side_effect = lambda: self.hand_value
        mock_hand.display_hand.return_value = ''
        mock_hand.hit.side_effect = self.increase_hand_value
        bj_round.play_through_dealer_hand(self.mock_shoe)

        self.assertEqual(mock_hand.hit.call_count, 1)

    def test_play_through_dealer_stands(self):
        mock_player_input = mock.Mock()
        mock_hand = mock.Mock()
        bj_round = round.Round(self.mock_time, mock_player_input,
                               self.mock_bankroll)
        bj_round._dealer_hand = mock_hand
        mock_hand.hand_value.return_value = 19
        mock_hand.display_hand.return_value = ''
        bj_round.play_through_dealer_hand(self.mock_shoe)

        self.assertFalse(mock_hand.hit.called)

    def test_amount_won_player_busts(self):
        mock_player_input = mock.Mock()
        mock_hand_one = mock.Mock()
        mock_hand_one.hand_value.return_value = 25
        mock_hand_two = mock.Mock()
        mock_hand_two.hand_value.return_value = 22
        bj_round = round.Round(self.mock_time, mock_player_input,
                               self.mock_bankroll)
        bj_round._dealer_hand = mock_hand_one
        bj_round._player_hands = [mock_hand_two]
        bj_round._bet = 250

        self.assertEqual(bj_round.showdown(), -250)

    def test_amount_won_player_natural_no_dealer_natural(self):
        mock_player_input = mock.Mock()
        bj_round = round.Round(self.mock_time, mock_player_input,
                               self.mock_bankroll)
        bj_round.player_natural = True
        bj_round._bet = 250

        self.assertEqual(bj_round.showdown(), 375)

    def test_amount_won_player_and_dealer_naturals(self):
        mock_player_input = mock.Mock()
        bj_round = round.Round(self.mock_time, mock_player_input,
                               self.mock_bankroll)
        bj_round.player_natural = True
        bj_round.dealer_natural = True
        bj_round._bet = 250

        self.assertEqual(bj_round.showdown(), 0)

    def test_amount_won_dealer_busts(self):
        mock_player_input = mock.Mock()
        mock_hand_one = mock.Mock()
        mock_hand_one.hand_value.return_value = 25
        mock_hand_two = mock.Mock()
        mock_hand_two.hand_value.return_value = 15
        bj_round = round.Round(self.mock_time, mock_player_input,
                               self.mock_bankroll)
        bj_round._dealer_hand = mock_hand_one
        bj_round._player_hands = [mock_hand_two]
        bj_round._bet = 250

        self.assertEqual(bj_round.showdown(), 250)

    def test_amount_won_player_wins(self):
        mock_player_input = mock.Mock()
        mock_hand_one = mock.Mock()
        mock_hand_one.hand_value.return_value = 19
        mock_hand_two = mock.Mock()
        mock_hand_two.hand_value.return_value = 20
        bj_round = round.Round(self.mock_time, mock_player_input,
                               self.mock_bankroll)
        bj_round._dealer_hand = mock_hand_one
        bj_round._player_hands = [mock_hand_two]
        bj_round._bet = 250

        self.assertEqual(bj_round.showdown(), 250)

    def test_amount_won_dealer_wins(self):
        mock_player_input = mock.Mock()
        mock_hand_one = mock.Mock()
        mock_hand_one.hand_value.return_value = 20
        mock_hand_two = mock.Mock()
        mock_hand_two.hand_value.return_value = 19
        bj_round = round.Round(self.mock_time, mock_player_input,
                               self.mock_bankroll)
        bj_round._dealer_hand = mock_hand_one
        bj_round._player_hands = [mock_hand_two]
        bj_round._bet = 250

        self.assertEqual(bj_round.showdown(), -250)

    def test_amount_won_two_player_hands(self):
        mock_player_input = mock.Mock()
        mock_hand_one = mock.Mock()
        mock_hand_one.hand_value.return_value = 19
        mock_hand_two = mock.Mock()
        mock_hand_three = mock.Mock()
        mock_hand_two.hand_value.return_value = 20
        mock_hand_three.hand_value.return_value = 20
        bj_round = round.Round(self.mock_time, mock_player_input,
                               self.mock_bankroll)
        bj_round._dealer_hand = mock_hand_one
        bj_round._player_hands = [mock_hand_two, mock_hand_three]
        bj_round._bet = 250

        self.assertEqual(bj_round.showdown(), 500)
