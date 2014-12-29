import random, os
import time 
import pygame
from pygame.locals import *
from sys import exit

DEFAULT_MSG = "Welcome to poker game"

'''
Location info
'''
SCREEN_SIZE = (1280, 667) 


'''
Card info
'''
num_of_card = 54
num_of_player_card = 13
num_of_total_card = 54


'''
Font info
'''
FONT_FILE = "font/PAPYRUS.ttf"
FONT_SIZE = 18
FONT_DEFAULT_COLOR = (255,255,255)

'''
Image info
'''
IMAGE_DIR = "images/"
icon_filename = "images/poker_icon.jpg"
background_image_filename = 'images/background.jpg'
back_card_filename = 'images/back.jpg'

    

pygame.init()

pygame.display.set_icon(pygame.image.load(icon_filename))
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)#SCREEN_SIZE, FULLSCREEN, 32)
pygame.display.set_caption("Poker Game")



poker_filename = dict()
poker_dict = dict()
for i in xrange(1,num_of_card+1):
    path = IMAGE_DIR + str(i) + ".jpg"
    poker_filename[i] = path
    poker_dict[i] = pygame.image.load(path).convert()

background = pygame.image.load(background_image_filename).convert()
back_card = pygame.image.load(back_card_filename).convert()


screen_width, screen_height = SCREEN_SIZE
poker_width = poker_dict[1].get_width()
pokrt_height = poker_dict[1].get_height()
org_player_card_x = SCREEN_SIZE[0]/2-4*poker_width



def display_all(player_card_list, player_card_rect, put_card_alreay):  
    fill_background()
    if put_card_alreay == 1:              
        put_card_alreay = 0
        player_card_x = org_player_card_x+(13-num_of_player_card)*poker_width/4 
        for i in xrange(0, num_of_player_card):
            player_card_rect[i]["x"] = player_card_x+i*poker_width/2
                
    display_num_of_player_cards(player_card_list, player_card_rect, num_of_player_card)

    screen.blit(write_to_screen("Joker1 join the game"),(screen_width -280,screen_height - 250))
    screen.blit(write_to_screen("Joker2 join the game"), (screen_width -280,screen_height - 225))
    screen.blit(write_to_screen("Game start!"),(screen_width -280,screen_height - 200))
    screen.blit(write_to_screen("Joker1 and Joker2 win the game!"),(screen_width -280,screen_height - 175))


def write_to_screen(msg=DEFAULT_MSG, color= FONT_DEFAULT_COLOR):    
    myfont = pygame.font.Font(FONT_FILE, FONT_SIZE)
    mytext = myfont.render(msg, True, FONT_DEFAULT_COLOR)
    mytext = mytext.convert_alpha()
    return mytext   


def display_num_of_player_cards(card_list, player_card_rect, num):
    # upside
    for i in xrange(0, num):
        screen.blit(num_to_cards(card_list[i]), (player_card_rect[i]["x"], player_card_rect[i]["y"]))
    # backside
    screen.blit(back_card, (player_card_rect[12]["x"]+poker_width/2, player_card_rect[12]["y"]))
    return


def ini_random_cards(all_card_list, p_card_list):
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
        

def num_to_cards(num):
    if poker_dict.has_key(num):
        return poker_dict[num]
    else:
        print num
        return poker_dict[num]


def fill_background():
    for y in xrange(0, screen_height, background.get_height()):
        for x in xrange(0, screen_width, background.get_width()):
            screen.blit(background, (x, y))


def main():
  
    loop_number = 24    


    player_card_list  = [0] * num_of_player_card
    player_card_rect  = list()

    all_card_list    = [0] * num_of_total_card

    player_card_x     = SCREEN_SIZE[0]/2-4*poker_width
    player_card_y     = 250

    put_card_alreay = 0

    
    random.seed()
    player_card_list = ini_random_cards(all_card_list, player_card_list)
        

    screen.blit(background, (0,0))

     
    for i in xrange(0, num_of_player_card): 
        player_card_rect.append({"x":player_card_x+i*poker_width/2, "y":player_card_y})

	
    display_all(player_card_list, player_card_rect, put_card_alreay)
    pygame.display.update()
    
    player_card_list.sort()

    while loop_number > 0:        
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    print 'left button'
                if event.button == 3:
                    print 'right button'                
                    
            
        if num_of_player_card != 0 :
                put_card_alreay = 1 
        
        display_all(player_card_list, player_card_rect, put_card_alreay)
        pygame.display.update()

    exit()
		
if __name__ == "__main__":
    main()