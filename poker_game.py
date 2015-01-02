import random, os
import time 
import pygame
from pygame.locals import *
from sys import exit
from client import login
from utils import ini_random_cards

DEFAULT_MSG = "SPADE SEVEN"

'''
Location info
'''
SCREEN_SIZE = (1280, 667) 


'''
Card info
'''
num_of_card = 52
num_of_player_card = 13
num_of_total_card = 52


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
ready_image_filename = "images/ready.png"
ready_hover_filename = "images/ready_hover.png"
background_image_filename = 'images/background.jpg'
back_card_filename = 'images/back.jpg'


'''
network status
'''
NETWORK_MODE = 0
NETWORK_CON = object()
    


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
ready_button = pygame.image.load(ready_image_filename).convert()
ready_hover = pygame.image.load(ready_hover_filename).convert()

background = pygame.image.load(background_image_filename).convert()
back_card = pygame.image.load(back_card_filename).convert()
back_card_90 = pygame.transform.rotate(back_card , 90)
back_card_anti_90 = pygame.transform.rotate(back_card , -90)




SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE
POKER_WIDTH = poker_dict[1].get_width()
POKER_HEIGHT = poker_dict[1].get_height()
TOP_MARGIN = 10
ORG_PLAYER_CARD_X = SCREEN_WIDTH/2-4*POKER_WIDTH
ORG_PLAYER_CARD_Y = SCREEN_HEIGHT - POKER_HEIGHT - TOP_MARGIN
LOGIN_X = SCREEN_WIDTH-login_button.get_width()-100
LOGIN_Y = 100
START_X = SCREEN_WIDTH-start_button.get_width()-100
START_Y = LOGIN_Y + 120
READY_X = SCREEN_WIDTH/2 - ready_button.get_width()/2
READY_Y = SCREEN_HEIGHT - ready_button.get_height() - 50



'''
Function definition
'''

def display_all(player_card_list, player_card_rect, put_card_alreay):  
    fill_background()
    if put_card_alreay == 1:              
        put_card_alreay = 0
        set_player_card_x(player_card_rect)
                
    display_num_of_player_cards(player_card_list, player_card_rect, num_of_player_card)
    # show message on the screen
    display_other_players_cards()
    #
    boundary = list()
    display_cards_on_table(player_card_list, boundary)
    #
    display_cards_on_panel()


def write_to_screen(msg=DEFAULT_MSG, color= FONT_DEFAULT_COLOR):    
    myfont = pygame.font.Font(FONT_FILE, FONT_SIZE)
    mytext = myfont.render(msg, True, FONT_DEFAULT_COLOR)
    mytext = mytext.convert_alpha()
    return mytext   


def set_player_card_x(player_card_rect):
    player_card_x = ORG_PLAYER_CARD_X+(13-num_of_player_card)*POKER_WIDTH/4 
    for i in xrange(0, num_of_player_card):
        player_card_rect[i]["x"] = player_card_x+i*POKER_WIDTH/2


def display_num_of_player_cards(card_list, player_card_rect, num):
    # player's card
    for i in xrange(0, num):
        screen.blit(num_to_poker_cards(card_list[i]), (player_card_rect[i]["x"], player_card_rect[i]["y"]))
    return


def display_other_players_cards():
    # opposite
    player_card_x = ORG_PLAYER_CARD_X+(13-num_of_player_card)*POKER_WIDTH/4
    for i in xrange(0, num_of_player_card):
        screen.blit(back_card, (player_card_x+i*POKER_WIDTH/2, TOP_MARGIN))
    player_card_y = SCREEN_HEIGHT/5+(13-num_of_player_card)*POKER_WIDTH/4
    gap_x = 50
    # left
    for i in xrange(0, num_of_player_card):
        screen.blit(back_card_90, (ORG_PLAYER_CARD_X-gap_x-POKER_HEIGHT, player_card_y+i*POKER_WIDTH/3))
    # right
    for i in xrange(0, num_of_player_card):
        screen.blit(back_card_anti_90, (ORG_PLAYER_CARD_X+(13+1)*POKER_WIDTH/2+gap_x, player_card_y+i*POKER_WIDTH/3))
    return


def display_cards_on_table(table_card_list, boundary = []):
    start_pos_x = 360
    start_pos_y = SCREEN_HEIGHT/2 - POKER_HEIGHT/2
    distance_x = POKER_WIDTH + 50
    for i in xrange(0, 13):
        num = (12-i)*4 + 1
        pos_y = start_pos_y + (i-7)*POKER_HEIGHT/7
        screen.blit(num_to_poker_cards(num), (start_pos_x, pos_y)) 
    #screen.blit(num_to_poker_cards(25), (start_pos_x, start_pos_y)) 
    screen.blit(num_to_poker_cards(26), (start_pos_x+distance_x, start_pos_y)) 
    screen.blit(num_to_poker_cards(27), (start_pos_x+2*distance_x, start_pos_y)) 
    screen.blit(num_to_poker_cards(28), (start_pos_x+3*distance_x, start_pos_y))  
    return 

def display_cards_on_panel():
    panel_height = 110
    panel_width = panel_height/0.618
    panel_x = ORG_PLAYER_CARD_X-panel_width-3*TOP_MARGIN
    panel_y = SCREEN_HEIGHT-TOP_MARGIN-panel_height
    s = pygame.Surface((panel_width, panel_height))
    (b,g,r) = (255,255,255)
    s.fill((b,g,r))
    s.set_alpha(100)
    # draw panel
    screen.blit(s, (panel_x, panel_y))
    # draw cards
    (scale_w, scale_h) = (POKER_WIDTH/12*5, POKER_HEIGHT/12*5)
    gap_x = POKER_WIDTH/5
    gap_y = 5
    screen.blit(pygame.transform.scale(num_to_poker_cards(26), (scale_w, scale_h)), (panel_x+gap_y, panel_y+gap_y))
    screen.blit(pygame.transform.scale(num_to_poker_cards(27), (scale_w, scale_h)), (panel_x+scale_w+2*gap_y, panel_y+gap_y))

'''
Fill screen
'''
def fill_background():
    for y in xrange(0, SCREEN_HEIGHT, background.get_height()):
        for x in xrange(0, SCREEN_WIDTH, background.get_width()):
            screen.blit(background, (x, y))
    # show message on the screen
    screen.blit(write_to_screen(DEFAULT_MSG),(SCREEN_WIDTH/2 - 80, SCREEN_HEIGHT/3))


def fill_init_screen():
    for y in xrange(0, SCREEN_HEIGHT, background.get_height()):
        for x in xrange(0, SCREEN_WIDTH, background.get_width()):
            screen.blit(init_screen, (x, y))
    login_button.set_colorkey((0,0,0))
    start_button.set_colorkey((0,0,0))
    screen.blit(login_button, (LOGIN_X, LOGIN_Y))
    screen.blit(start_button, (START_X, START_Y))

'''
Map number to card object
'''
def num_to_poker_cards(num):
    if poker_dict.has_key(num):
        return poker_dict[num]
    else:
        print num
        return poker_dict[num]


'''
Detect mouse position
'''
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

'''
Display select status
'''
def display_init_select_status():
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


def display_ready_select_status():
    mos_x, mos_y = pygame.mouse.get_pos()
    if detect_mouse_in_rect(READY_X, READY_Y, ready_button.get_width(), ready_button.get_height(), mos_x, mos_y):
        ready_hover.set_colorkey((0,0,0))
        screen.blit(ready_hover, (READY_X, READY_Y))
    else:
        ready_button.set_colorkey((0,0,0))
        screen.blit(ready_button, (READY_X, READY_Y))


def display_game_select_status(player_card_rect, pos):
    choose_flag = False
    choose_card = -1
    delta_y = 20
    mos_x, mos_y = pos
    set_player_card_x(player_card_rect)
    for i in xrange(0, num_of_player_card-1):
        if detect_mouse_in_rect(player_card_rect[i]["x"], player_card_rect[i]["y"], POKER_WIDTH/2, POKER_HEIGHT, mos_x, mos_y) and player_card_rect[i]["y"] == ORG_PLAYER_CARD_Y:
            player_card_rect[i]["y"] = ORG_PLAYER_CARD_Y - delta_y
            choose_card = i
            choose_flag =  True
        else:
            player_card_rect[i]["y"] = ORG_PLAYER_CARD_Y
    # rightmost card
    i = num_of_player_card-1
    if detect_mouse_in_rect(player_card_rect[i]["x"], player_card_rect[i]["y"], POKER_WIDTH, POKER_HEIGHT, mos_x, mos_y) and player_card_rect[i]["y"] == ORG_PLAYER_CARD_Y:
        player_card_rect[i]["y"] = ORG_PLAYER_CARD_Y - delta_y
        choose_card = i
        choose_flag = True
    else:
        player_card_rect[i]["y"] = ORG_PLAYER_CARD_Y
    return choose_flag, choose_card


'''
Initialize screen
- Click Login or press enter to connect to server and start the game
- Click Start or press space to start the local game
'''
def display_init_screen():
    init_flag = 0
    global NETWORK_CON 
    global NETWORK_MODE
    fill_init_screen()
    pygame.display.update()
    while True:
        display_init_select_status()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if detect_mouse_in_rect(LOGIN_X, LOGIN_Y, login_button.get_width(), login_button.get_height(), event.pos[0], event.pos[1]):
                    NETWORK_CON = login()
                    NETWORK_MODE = 1
                    init_flag = 1
                if detect_mouse_in_rect(START_X, START_Y, start_button.get_width(), start_button.get_height(), event.pos[0], event.pos[1]):
                    init_flag = 1
            if event.type == KEYDOWN:
                print event.key
                if event.key == 13: # enter
                    NETWORK_CON = login()
                    NETWORK_MODE = 1
                    init_flag = 1
                elif event.key == 32: # space
                    init_flag = 1
        if init_flag == 1:
            break


def is_user_ready():
    is_ready_flag = False
    fill_background()
    ready_button.set_colorkey((0,0,0))
    screen.blit(ready_button, (READY_X, READY_Y))
    while True:
        display_ready_select_status()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if detect_mouse_in_rect(READY_X, READY_Y, ready_button.get_width(), ready_button.get_height(), event.pos[0], event.pos[1]):
                    is_ready_flag = True
            if event.type == KEYDOWN:
                print event.key
                if event.key == 13 or event.key == 32:
                    is_ready_flag = True
        if is_ready_flag:
            break
    return True


def initialize_player_card():
    ''' card_list: card original number
        card_rect: card position
    '''
    player_card_list  = [0] * num_of_player_card
    player_card_rect  = list()

    all_card_list    = [0] * num_of_total_card

    player_card_x     = ORG_PLAYER_CARD_X
    player_card_y     = ORG_PLAYER_CARD_Y

    put_card_alreay = 0

    
    random.seed()
    player_card_list = ini_random_cards(all_card_list, player_card_list, num_of_total_card, num_of_player_card)
        

    screen.blit(background, (0,0))

     
    for i in xrange(0, num_of_player_card): 
        player_card_rect.append({"x":player_card_x+i*POKER_WIDTH/2, "y":player_card_y})
    
    display_all(player_card_list, player_card_rect, put_card_alreay)
    pygame.display.update()
    
    player_card_list.sort()    
    return player_card_list, player_card_rect


def handle_screen_msg(player_card_list, player_card_rect):
    loop_number = 5   
    choose_flag = False 
    choose_card = -1
    while loop_number > 0:       
        for event in pygame.event.get():
            
            if event.type == QUIT:
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    choose_flag, choose_card = display_game_select_status(player_card_rect, event.pos)
                if event.button == 3: 
                    if choose_flag and choose_card > -1: 
                        choose_flag = False
                        send_message('player select card: '+str(player_card_list[choose_card]))   
                        choose_card = -1          
            if event.type == KEYDOWN:
                print event.key
                if event.key == K_ESCAPE :
                    exit()     
            
        if num_of_player_card != 0 :
                put_card_alreay = 1 
        
        display_all(player_card_list, player_card_rect, put_card_alreay)
        pygame.display.update()


def send_message(text):
    # send to server
    print text 
    if NETWORK_MODE:
        NETWORK_CON.send_msg(text)

    return


def main():
    try:
        #
        display_init_screen()
        #
        if is_user_ready():
            player_card_list, player_card_rect = initialize_player_card()
            #
            handle_screen_msg(player_card_list, player_card_rect)
            #
            exit()
    except Exception as err:
        print err		


if __name__ == "__main__":
    main()