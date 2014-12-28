import random, os
import time 
import pygame
from pygame.locals import *
from sys import exit

SCREEN_SIZE = (1080, 667) 
pygame.init()

pygame.display.set_icon(pygame.image.load("images/poker_icon.jpg"))
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)#SCREEN_SIZE, FULLSCREEN, 32)
pygame.display.set_caption("Poker Game")

background_image_filename = 'images/Nostalgy.gif'
back_card_filename = 'images/back.jpg'

IMAGE_DIR = "images/"
poker_filename = dict()
poker_dict = dict()
for i in xrange(1,54):
    path = IMAGE_DIR + str(i) + ".jpg"
    poker_filename[i] = path
    poker_dict[i] = pygame.image.load(path).convert()
    
poker_width = poker_dict[1].get_width()
pokrt_height = poker_dict[1].get_height()


background = pygame.image.load(background_image_filename).convert()
back_card = pygame.image.load(back_card_filename).convert()

def display_all(put_card_alreay):
    global player_card_x
    global player_card_rect
    
    fill_background()
    if put_card_alreay == 1:              
        put_card_alreay = 0
        player_card_x = org_player_card_x+(13-num_of_card)*poker_width/4 
        for x in range(0, num_of_card):
            player_card_rect[x][0] = player_card_x+x*poker_width/2
                
    display_num_of_cards(player_card_list, num_of_card)


def display_num_of_cards(list, num):
    for x in range(0, num):
        screen.blit(num_to_cards(list[x]), (player_card_rect[x][0], player_card_rect[x][1]))
    return


def ini_random_cards(all_card_list, p_card_list, p_id):
    for x in range(0, 13):
        start = random.randint(0, 51)
        i = start
        while i != -1 :
            if 0 == all_card_list[start]:
                if i != 0:
                    start += 1
                    start %= 52
                    i -= 1
                else:
                    break
            else:
                start += 1
                start %= 52

        all_card_list[start] = 1
        p_card_list[x] = start
    return p_card_list
        
def num_to_cards(num):
    return poker_dict[num]


def fill_background():
    for y in range(0, screen_height, background.get_height()):
        for x in range(0, screen_width, background.get_width()):
            screen.blit(background, (x, y))


def main(loop_num = -1):
  

    global player_card_list 
    global player_card_rect        
    
    global org_player_card_x 
    global player_card_x     
    global player_card_y        
          
    
    global num_of_card     
       
    global screen_width, screen_height
    
    print "start"

    if loop_num > 0:
        loop_number = loop_num
    else:
        loop_number = 1
    


    player_card_list  = [0] * 13
    player_card_rect  = [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]]

    all_card_list    = [0] * 52

    org_player_card_x = SCREEN_SIZE[0]/2-4*poker_width
    player_card_x     = SCREEN_SIZE[0]/2-4*poker_width
    player_card_y     = 250

    put_card_alreay = 0

    num_of_card     = 13

    
    random.seed()
    player_card_list = ini_random_cards(all_card_list, player_card_list, 1)

        

    screen.blit(background, (0,0))
     
    screen_width, screen_height = SCREEN_SIZE
     
    for i in range(0, 13): 
        player_card_rect[i][1] = player_card_y
        player_card_rect[i][0] = player_card_x+i*poker_width/2

	
    display_all(put_card_alreay)
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
                    
            
        if num_of_card != 0 :
                put_card_alreay = 1 
        
        display_all(put_card_alreay)
        pygame.display.update()

    exit()
		
if __name__ == "__main__":
    main()