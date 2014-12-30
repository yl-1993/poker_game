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
init_image_filename = "images/init.jpg"
login_image_filename = "images/login.png"
login_hover_filename = "images/login_hover.png"
start_image_filename = "images/start.png"
start_hover_filename = "images/start_hover.png"
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

init_screen = pygame.image.load(init_image_filename).convert()
login_button = pygame.image.load(login_image_filename).convert()
login_hover = pygame.image.load(login_hover_filename).convert()
start_button = pygame.image.load(start_image_filename).convert()
start_hover = pygame.image.load(start_hover_filename).convert()

background = pygame.image.load(background_image_filename).convert()
back_card = pygame.image.load(back_card_filename).convert()



SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE
POKER_WIDTH = poker_dict[1].get_width()
POKER_HEIGHT = poker_dict[1].get_height()
ORG_PLAYER_CARD_X = SCREEN_SIZE[0]/2-4*POKER_WIDTH
LOGIN_X = SCREEN_WIDTH-login_button.get_width()-100
LOGIN_Y = 100
START_X = SCREEN_WIDTH-start_button.get_width()-100
START_Y = LOGIN_Y + 100



def display_all(player_card_list, player_card_rect, put_card_alreay):  
    fill_background()
    if put_card_alreay == 1:              
        put_card_alreay = 0
        player_card_x = ORG_PLAYER_CARD_X+(13-num_of_player_card)*POKER_WIDTH/4 
        for i in xrange(0, num_of_player_card):
            player_card_rect[i]["x"] = player_card_x+i*POKER_WIDTH/2
                
    display_num_of_player_cards(player_card_list, player_card_rect, num_of_player_card)

    screen.blit(write_to_screen("Joker1 join the game"),(SCREEN_WIDTH -280,SCREEN_HEIGHT - 250))
    screen.blit(write_to_screen("Joker2 join the game"), (SCREEN_WIDTH -280,SCREEN_HEIGHT - 225))
    screen.blit(write_to_screen("Game start!"),(SCREEN_WIDTH -280,SCREEN_HEIGHT - 200))
    screen.blit(write_to_screen("Joker1 and Joker2 win the game!"),(SCREEN_WIDTH -280,SCREEN_HEIGHT - 175))


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
    screen.blit(back_card, (player_card_rect[12]["x"]+POKER_WIDTH/2, player_card_rect[12]["y"]))
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
    for y in xrange(0, SCREEN_HEIGHT, background.get_height()):
        for x in xrange(0, SCREEN_WIDTH, background.get_width()):
            screen.blit(background, (x, y))


def fill_init_screen():
    for y in xrange(0, SCREEN_HEIGHT, background.get_height()):
        for x in xrange(0, SCREEN_WIDTH, background.get_width()):
            screen.blit(init_screen, (x, y))
    login_button.set_colorkey((0,0,0))
    start_button.set_colorkey((0,0,0))
    screen.blit(login_button, (LOGIN_X, LOGIN_Y))
    screen.blit(start_button, (START_X, START_Y))


def detect_mouse_in_rect(button_x, button_y, len_x, len_y, mos_x, mos_y):
    if mos_x>button_x and (mos_x<button_x+len_x):
        x_inside = True
    else: 
        return False
    if mos_y>button_y and (mos_y<button_y+len_y):
        y_inside = True
    else: 
        return False
    if x_inside and y_inside:
        return True


def display_select_status():
    mos_x, mos_y = pygame.mouse.get_pos()
    if detect_mouse_in_rect(LOGIN_X, LOGIN_Y, login_button.get_width(), login_button.get_height(), mos_x, mos_y):
        login_hover.set_colorkey((0,0,0))
        screen.blit(login_hover, (LOGIN_X, LOGIN_Y))
    else:
        login_button.set_colorkey((0,0,0))
        screen.blit(login_button, (LOGIN_X, LOGIN_Y))
    if detect_mouse_in_rect(START_X, START_Y, start_button.get_width(), start_button.get_height(), mos_x, mos_y):
        start_hover.set_colorkey((0,0,0))
        screen.blit(start_hover, (START_X, START_Y))
    else:
        start_button.set_colorkey((0,0,0))
        screen.blit(start_button, (START_X, START_Y))


def display_init_screen():
    init_flag = 0
    fill_init_screen()
    pygame.display.update()
    while True:
        display_select_status()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if detect_mouse_in_rect(LOGIN_X, LOGIN_Y, login_button.get_width(), login_button.get_height(), event.pos[0], event.pos[1]):
                    login()
                    init_flag = 1
                if detect_mouse_in_rect(START_X, START_Y, start_button.get_width(), start_button.get_height(), event.pos[0], event.pos[1]):
                    init_flag = 1
            if event.type == KEYDOWN:
                print event.key
                if event.key == 13: # enter
                    login()
                    init_flag = 1
                elif event.key == 32: # space
                    init_flag = 1
        if init_flag == 1:
            break


'''
net mode:   connect to server
local mode: play with AI
'''
def login():
    return


def main():

    display_init_screen()

  
    loop_number = 24    

    player_card_list  = [0] * num_of_player_card
    player_card_rect  = list()

    all_card_list    = [0] * num_of_total_card

    player_card_x     = SCREEN_SIZE[0]/2-4*POKER_WIDTH
    player_card_y     = 250

    put_card_alreay = 0

    
    random.seed()
    player_card_list = ini_random_cards(all_card_list, player_card_list)
        

    screen.blit(background, (0,0))

     
    for i in xrange(0, num_of_player_card): 
        player_card_rect.append({"x":player_card_x+i*POKER_WIDTH/2, "y":player_card_y})

	
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
            if event.type == KEYDOWN:
                print event.key
                if event.key == K_ESCAPE :
                    exit()     
            
        if num_of_player_card != 0 :
                put_card_alreay = 1 
        
        display_all(player_card_list, player_card_rect, put_card_alreay)
        pygame.display.update()

    exit()
		
if __name__ == "__main__":
    main()