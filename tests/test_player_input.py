import unittest

import mock

from blackjack import player_input


class TestPlayerAction(unittest.TestCase):

    def setUp(self):
        self.mock_time = mock.Mock()

    def test_action_double_down_and_split_allowed(self):
        mock_hand = mock.Mock()
        mock_input_func = mock.Mock()
        mock_hand.double_down_allowed.return_value = True
        mock_hand.split_allowed.return_value = True
        mock_hand.display_hand.return_value = ''
        mock_input_func.side_effect = ['t', 'q', 'r', 'd']
        input = player_input.PlayerInput(self.mock_time)
        action = input.action(mock_hand, mock_input_func)

        self.assertEqual(mock_input_func.call_count, 4)
        self.assertEqual(action, 'd')

    def test_action_double_down_allowed_split_not(self):
        mock_hand = mock.Mock()
        mock_input_func = mock.Mock()
        mock_hand.double_down_allowed.return_value = True
        mock_hand.split_allowed.return_value = False
        mock_hand.display_hand.return_value = ''
        mock_input_func.side_effect = ['t', 'q', 'sp', 'd']
        input = player_input.PlayerInput(self.mock_time)
        action = input.action(mock_hand, mock_input_func)

        self.assertEqual(mock_input_func.call_count, 4)
        self.assertEqual(action, 'd')

    def test_action_neither_double_down_nor_split_allowed(self):
        mock_hand = mock.Mock()
        mock_input_func = mock.Mock()
        mock_hand.double_down_allowed.return_value = False
        mock_hand.split_allowed.return_value = False
        mock_hand.display_hand.return_value = ''
        mock_input_func.side_effect = ['t', 'd', 'sp', 'h']
        input = player_input.PlayerInput(self.mock_time)
        action = input.action(mock_hand, mock_input_func)

        self.assertEqual(mock_input_func.call_count, 4)
        self.assertEqual(action, 'h')

    def test_bet(self):
        mock_input_func = mock.Mock()
        mock_input_func.side_effect = [12, 2000, 250]
        input = player_input.PlayerInput(self.mock_time)
        bet = input.bet(mock_input_func)
        self.assertEqual(bet, 250)
        self.assertEqual(mock_input_func.call_count, 3)

    def test_welcome_and_get_buyin(self):
        mock_input_func = mock.Mock()
        mock_input_func.side_effect = [499, 50001, 1000]
        input = player_input.PlayerInput(self.mock_time)
        buy_in = input.welcome_and_get_buyin(mock_input_func)
        self.assertEqual(buy_in, 1000)
        self.assertEqual(mock_input_func.call_count, 3)

    def test_keep_playing(self):
        mock_input_func = mock.Mock()
        mock_input_func.side_effect = [5, 'z', 'y']
        bankroll_balance = 5000
        input = player_input.PlayerInput(self.mock_time)
        self.assertTrue(input.play_another_round(bankroll_balance,
                                                 mock_input_func))
        self.assertEqual(mock_input_func.call_count, 3)

    def test_stop_playing(self):
        mock_input_func = mock.Mock()
        mock_input_func.side_effect = [5, 'z', 'n']
        bankroll_balance = 5000
        input = player_input.PlayerInput(self.mock_time)
        self.assertFalse(input.play_another_round(bankroll_balance,
                                                  mock_input_func))
        self.assertEqual(mock_input_func.call_count, 3)


