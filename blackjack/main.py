import time_interface
import card
import deck
import shoe
import hand
import round
import bankroll
import player_input

time = time_interface.Time()
input = player_input.PlayerInput(time)
buy_in = input.welcome_and_get_buyin()
bankroll = bankroll.Bankroll(buy_in)
deck = deck.Deck()
shoe = shoe.Shoe(deck)

while True:
    rebuy = input.rebuy(bankroll.balance)
    if rebuy:
        rebuy_amount = input.rebuy_amount()
        bankroll.adjust_balance(rebuy_amount)
        print "\nYour updated bankroll balance is: %s" % (bankroll.balance)
    while bankroll.rebuy_necessary():
        print ("\nYour current bankroll balance is too low to continue playing. "
               "Please rebuy.")
        rebuy_amount = input.rebuy_amount()
        bankroll.adjust_balance(rebuy_amount)
        print "\nYour updated bankroll balance is: %s" % (bankroll.balance)

    if shoe.shoe_finished():
        shoe = shoe.Shoe(deck)

    current_round = round.Round(time, input, bankroll)
    current_round.place_bet()
    current_round.deal_hands(shoe)
    current_round.display_player_hands()
    current_round.display_dealer_hand(False)
    if current_round.player_natural:
        print "\nYou were dealt a natural!"
        amount_won = current_round.showdown()
    elif current_round.dealer_natural:
        print "\nDealer was dealt a natural."
        amount_won = current_round.showdown()
    else:
        skip_dealer = current_round.play_through_player_hands(shoe)
        if not skip_dealer:
            current_round.play_through_dealer_hand(shoe)
        amount_won = current_round.showdown()
    bankroll.adjust_balance(amount_won)
    another_round = input.play_another_round(bankroll.balance)
    if not another_round:
        break