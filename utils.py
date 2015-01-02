import random

def ini_random_cards(whose_card, p_card_list, num_of_total_card, num_of_player_card):
    all_card_list = range(0, num_of_total_card)
    random.shuffle(all_card_list)
    for x in xrange(0, 4):
        p_card_list[x] = all_card_list[4*x:4*x+num_of_player_card-1]
    for x in xrange(0, num_of_total_card):
        whose_card[all_card_list[x]] = (int)(x / num_of_player_card)