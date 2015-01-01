def ini_random_cards(all_card_list, p_card_list, num_of_total_card, num_of_player_card):
    for x in xrange(0, num_of_player_card):
        start = random.randint(0, num_of_total_card - 1)
        step = start
        while step > -1 :
            if all_card_list[start] == 0:
                if step > 0:
                    start += 1
                    start %= num_of_total_card
                    step -= 1
                else:
                    break
            else:
                start += 1
                start %= num_of_total_card

        all_card_list[start] = 1
        p_card_list[x] = start + 1

    return p_card_list