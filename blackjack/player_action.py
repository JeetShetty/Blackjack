def action(hand, input_func=raw_input):
    """Acquires and returns desired player action.

    Args:
        hand: The hand for which the action is being requested.
        input_func: Function to receive input from the user.
    """
    print "Hand: " + hand.display_hand()
    if hand.double_down_allowed() and hand.split_allowed():
        allowed_actions = ['h', 'st', 'sp', 'd']
        print "Hand: " + hand.display_hand()
        action = input_func("Would you like to [h]it, [st]and, [sp]lit, or "
                            "[d]ouble down? ")
        while action not in allowed_actions:
            action = input_func("Please choose your action from the following "
                                "options: 'h' to hit, 'st' to stand, 'sp' to "
                                "split, or 'd' to double down: "

    if hand.double_down_allowed() and not hand.split_allowed():
        allowed_actions = ['h', 'st', 'd']
        print "Hand: " + hand.display_hand()
        action = input_func("Would you like to [h]it, [st]and, or [d]ouble "
                            "down? ")
        while action not in allowed_actions:
            action = input_func("Please choose your action from the following "
                                "options: 'h' to hit, 'st' to stand, or 'd' to "
                                "double down: ")

    if not hand.double_down_allowed() and not hand.split_allowed():
        allowed_actions = ['h', 'st']
        print "Hand: " + hand.display_hand()
        action = input_func("Would you like to [h]it or [st]and?")
        while action not in allowed_actions:
            action = input_func("Please choose your action from the following ""
                                "options: 'h' to hit or 'st' to stand. ")

    return action