import random, os
import time 
import pygame
from pygame.locals import *
from sys import exit
from client import server_listener
from utils import ini_random_cards
from config import CLIENT_HEAD

DEFAULT_MSG = "SPADE SEVEN"

'''
Location info
'''
SCREEN_SIZE = (1280, 667) 
PLAYER_NUM = 4

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
AVATAR_PRE = "player_"
icon_filename = IMAGE_DIR + "poker_icon.jpg"
init_image_filename = "images/init.jpg"
background_image_filename = 'images/background.jpg'
back_card_filename = 'images/back.jpg'

'''
Button info
'''
login_image_filename = "images/login.png"
login_hover_filename = "images/login_hover.png"
start_image_filename = "images/start.png"
start_hover_filename = "images/start_hover.png"
ready_image_filename = "images/ready.png"
ready_hover_filename = "images/ready_hover.png"
ok_image_filename = "images/ok.png"
ok_hover_filename = "images/ok_hover.png"
turn_flag_filename = "images/flag.jpg"


'''
Error info
'''
error_0_filename = IMAGE_DIR + "error_0.png"
error_1_filename = IMAGE_DIR + "error_1.png"
error_2_filename = IMAGE_DIR + "error_2.png"


'''
network status
'''
NETWORK_MODE = 0
NETWORK_CON = object()
    

'''
Card color
'''
WHITE = (248,252,248)
GRAY = (180,180,180)
SHADOW = (184,244,240)


'''
Initialize game
'''
pygame.init()

pygame.display.set_icon(pygame.image.load(icon_filename))
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)#SCREEN_SIZE, FULLSCREEN, 32)
pygame.display.set_caption("Poker Game")


'''
Load images
'''
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
ok_button = pygame.image.load(ok_image_filename).convert()
ok_hover = pygame.image.load(ok_hover_filename).convert()
turn_flag = pygame.image.load(turn_flag_filename).convert()

error_text_0 = pygame.image.load(error_0_filename).convert()
error_text_1 = pygame.image.load(error_1_filename).convert()
error_text_2 = pygame.image.load(error_2_filename).convert()

background = pygame.image.load(background_image_filename).convert()
back_card = pygame.image.load(back_card_filename).convert()
back_card_90 = pygame.transform.rotate(back_card , 90)
back_card_anti_90 = pygame.transform.rotate(back_card , -90)

table_card_row_list = [-1] * 4

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
READY_X_1 = 100
READY_X_2 = READY_X
READY_X_3 = SCREEN_WIDTH - READY_X_1 - ready_button.get_width()
READY_Y_1 = SCREEN_HEIGHT/2 - ready_button.get_height()/2
READY_Y_2 = SCREEN_HEIGHT - READY_Y - ready_button.get_height()
READY_Y_3 = READY_Y_1
OK_X = SCREEN_WIDTH/2 - ok_button.get_width()/2
OK_Y = SCREEN_HEIGHT/2 - ok_button.get_height()/2
AVATAR_SIZE = (64,64)


'''
Table card position
'''
START_POS_X = 360
START_POS_Y = SCREEN_HEIGHT/2 - POKER_HEIGHT/2
DISTANCE_X = POKER_WIDTH + 50


'''
Player position
'''
ready_pos_list = list()
ready_pos_list.append((READY_X, READY_Y))
ready_pos_list.append((READY_X_1, READY_Y_1))
ready_pos_list.append((READY_X_2, READY_Y_2))
ready_pos_list.append((READY_X_3, READY_Y_3))

gap_flag = 10

turn_flag_pos_list = list()
turn_flag_pos_list.append((READY_X + ready_button.get_width()/2 - 25, 534 - 50 - gap_flag))
turn_flag_pos_list.append((ORG_PLAYER_CARD_X - 50 + gap_flag, READY_Y_1 + ready_button.get_height()/2 - 25))
turn_flag_pos_list.append((READY_X_2 + ready_button.get_width()/2 - 25, TOP_MARGIN + POKER_HEIGHT + gap_flag))
turn_flag_pos_list.append((ORG_PLAYER_CARD_X+(13+1)*POKER_WIDTH/2 - gap_flag, READY_Y_3 + ready_button.get_height()/2 - 25))


players_avatars = [0] * 4
avatars_pos_list = list()
avatars_pos_list.append((READY_X + ready_button.get_width() + 100, READY_Y))
avatars_pos_list.append((READY_X_1, READY_Y_1 + ready_button.get_height() + 50))
avatars_pos_list.append((READY_X_2 - AVATAR_SIZE[0] - 100, READY_Y_2))
avatars_pos_list.append((READY_X_3, READY_Y_3 - AVATAR_SIZE[1] - 50))


'''
Function definition
'''
def display_all(player_card_list, player_card_rect, num_of_current_card, card_status, boundary):  
    fill_background()
    display_player_turn(player_card_rect)
    #
    set_player_card_x_by_status(card_status, player_card_list, player_card_rect, num_of_current_card[NETWORK_CON.p_client.my_id])
    
    discard_card_list = list()

    for i in xrange(0, num_of_player_card):
        if card_status[i] == 0: # common
            display_cards_by_status(player_card_list[i], (player_card_rect[i]["x"], player_card_rect[i]["y"]), 0)
        elif card_status[i] == 1: # valid
            display_cards_by_status(player_card_list[i],  (player_card_rect[i]["x"], player_card_rect[i]["y"]), 1)
        elif card_status[i] == 2: #table card
            continue
        elif card_status[i] == 3: #discard
            discard_card_list.append(player_card_list[i])
        else:
            print CLIENT_HEAD + "card status error"
    
    # show message on the screen
    num_of_opposite_card = num_of_current_card[(NETWORK_CON.p_client.my_id + 2) % 4]
    num_of_left_card = num_of_current_card[(NETWORK_CON.p_client.my_id + 1) % 4]
    num_of_right_card = num_of_current_card[(NETWORK_CON.p_client.my_id + 3) % 4]
    display_other_players_cards(num_of_opposite_card, num_of_left_card, num_of_right_card)
    #
    display_cards_on_table(boundary)
    #
    
    display_cards_on_panel(discard_card_list)


'''
display players' cards one by one 
'''
def display_all_one_by_one(player_card_list, player_card_rect):
    fill_background()
    
    for num_of_current_card in xrange(1, num_of_player_card + 1):
        set_player_card_x(player_card_rect, num_of_current_card)
                
        display_num_of_player_cards(player_card_list, player_card_rect, num_of_current_card)
        # show message on the screen
        display_other_players_cards(num_of_current_card, num_of_current_card, num_of_current_card)
        #
        pygame.display.update()
        time.sleep(0.25)


def write_to_screen(msg=DEFAULT_MSG, color=FONT_DEFAULT_COLOR, size=FONT_SIZE):    
    myfont = pygame.font.Font(FONT_FILE, size)
    mytext = myfont.render(msg, True, color)
    mytext = mytext.convert_alpha()
    return mytext   



def change_single_card_color(num, old_color, color):
    for x in xrange(0, POKER_WIDTH):
        for y in xrange(0, POKER_HEIGHT):
            card_color = num_to_poker_cards(num).get_at((x,y))
            if card_color[0] >= old_color[0] and card_color[1] >= old_color[1] and card_color[2] >= old_color[2]:
                num_to_poker_cards(num).set_at((x,y),color)


def display_cards_by_status(num, pos, status=0):
    if status == 1:
        change_single_card_color(num, WHITE, SHADOW)
    elif status == 0:
        change_single_card_color(num, SHADOW, WHITE)
    else:
        print CLIENT_HEAD+"card status error!"
    screen.blit(num_to_poker_cards(num), pos)
    return


def regulize_card_color():
    for i in xrange(1, num_of_card+1):
        change_single_card_color(i, GRAY, WHITE)


def set_player_card_x(player_card_rect, num_of_current_card):
    player_card_x = ORG_PLAYER_CARD_X+(13-num_of_current_card)*POKER_WIDTH/4 
    for i in xrange(0, num_of_current_card):
        player_card_rect[i]["x"] = player_card_x+i*POKER_WIDTH/2


def set_player_card_x_by_status(card_status, player_card_list, player_card_rect, num_of_current_card):
    player_card_x = ORG_PLAYER_CARD_X+(13-num_of_current_card)*POKER_WIDTH/4 
    count = 0
    right_most = 0
    for i in xrange(0, num_of_player_card):
        if card_status[i] < 2: # if card is common or valid
            player_card_rect[i]["x"] = player_card_x+count*POKER_WIDTH/2
            count += 1
            right_most = i
        else:
            player_card_rect[i]["x"] = 0
            player_card_rect[i]["y"] = 0
    return i


def display_num_of_player_cards(card_list, player_card_rect, num):
    # player's card
    for i in xrange(0, num):
        screen.blit(num_to_poker_cards(card_list[i]), (player_card_rect[i]["x"], player_card_rect[i]["y"]))
    return


def display_other_players_cards(num_of_opposite_card, num_of_left_card, num_of_right_card):
    # opposite
    player_card_x = ORG_PLAYER_CARD_X+(13-num_of_opposite_card)*POKER_WIDTH/4
    for i in xrange(0, num_of_opposite_card):
        screen.blit(back_card, (player_card_x+i*POKER_WIDTH/2, TOP_MARGIN))

    gap_x = 50
    # left
    player_card_y_left = SCREEN_HEIGHT/5+(13-num_of_left_card)*POKER_WIDTH/4
    for i in xrange(0, num_of_left_card):
        screen.blit(back_card_90, (ORG_PLAYER_CARD_X-gap_x-POKER_HEIGHT, player_card_y_left+i*POKER_WIDTH/3))
    # right
    player_card_y_right = SCREEN_HEIGHT/5+(13-num_of_right_card)*POKER_WIDTH/4
    for i in xrange(0, num_of_right_card):
        screen.blit(back_card_anti_90, (ORG_PLAYER_CARD_X+(13+1)*POKER_WIDTH/2+gap_x, player_card_y_right+i*POKER_WIDTH/3))
    return


def display_single_row_on_table(color_id, row_x, low, high):
    card_id = high
    for i in xrange(0, high-low+1):
        num = 13*color_id + card_id
        pos_y = START_POS_Y - (card_id-7)*POKER_HEIGHT/7
        if NETWORK_CON.p_client.last_card == num:
            display_cards_by_status(num,  (row_x, pos_y), 1)
        else:
            display_cards_by_status(num,  (row_x, pos_y), 0)
        card_id -= 1


def display_cards_on_table(boundary = []):
    # TODO
    global table_card_row_list
    if len(boundary) == 8:
        i = 0
        for count in xrange(0, 4):
            cur_max_row = max(table_card_row_list)

            if boundary[i] == boundary[i+1] == -1:
                i += 2
            elif boundary[i] <= 7 and boundary[i+1] >= 7:
                color_id = i/2
                if table_card_row_list[color_id] == -1:
                    table_card_row_list[color_id] = cur_max_row+1
                display_single_row_on_table(color_id, START_POS_X+table_card_row_list[color_id]*DISTANCE_X, boundary[i], boundary[i+1])
                i += 2
                #print START_POS_X+table_card_row_list[color_id]*DISTANCE_X

    #test
    # for i in xrange(0, 13):
    #     num = (12-i)*4 + 1
    #     pos_y = START_POS_Y + (i-7)*POKER_HEIGHT/7
    #     screen.blit(num_to_poker_cards(num), (START_POS_X, pos_y)) 
    # # current_color
    # screen.blit(num_to_poker_cards(26), (START_POS_X+DISTANCE_X, START_POS_Y)) 
    # screen.blit(num_to_poker_cards(27), (START_POS_X+2*DISTANCE_X, START_POS_Y)) 
    # #screen.blit(num_to_poker_cards(28), (START_POS_X+3*DISTANCE_X, START_POS_Y))  
    # display_cards_by_status(28, (START_POS_X+3*DISTANCE_X, START_POS_Y), 1)
    return 


def display_cards_on_panel(discard_card_list):
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
    discard_num = len(discard_card_list)
    for i in xrange(0,discard_num):
        #change_single_card_color(discard_card_list[i], SHADOW, WHITE)
        screen.blit(pygame.transform.scale(num_to_poker_cards(discard_card_list[i]), (scale_w, scale_h)), 
            ( panel_x+(i%5)*scale_w+((i+1)%5)*gap_y, panel_y+i/5*scale_h+(i/5+1)*gap_y ) )

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
        print CLIENT_HEAD + "not found key " + str(num)
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


def display_ok_select_status():
    mos_x, mos_y = pygame.mouse.get_pos()
    if detect_mouse_in_rect(OK_X, OK_Y, ok_button.get_width(), ok_button.get_height(), mos_x, mos_y):
        ok_hover.set_colorkey((0,0,0))
        screen.blit(ok_hover, (OK_X, OK_Y))
    else:
        ok_button.set_colorkey((0,0,0))
        screen.blit(ok_button, (OK_X, OK_Y))

def display_game_select_status(player_card_rect, num_of_current_card, pos):
    choose_flag = False
    choose_card = -1
    delta_y = 20
    mos_x, mos_y = pos
    right_most = set_player_card_x_by_status(NETWORK_CON.p_client.my_cards_status, 
                                                NETWORK_CON.p_client.my_cards, 
                                                player_card_rect, 
                                                num_of_current_card)
    for i in xrange(0, num_of_player_card):
        if i == right_most:
            if detect_mouse_in_rect(player_card_rect[i]["x"], player_card_rect[i]["y"], POKER_WIDTH, POKER_HEIGHT, mos_x, mos_y) and player_card_rect[i]["y"] == ORG_PLAYER_CARD_Y:
                player_card_rect[i]["y"] = ORG_PLAYER_CARD_Y - delta_y
                choose_card = i
                choose_flag = True
            else:
                player_card_rect[i]["y"] = ORG_PLAYER_CARD_Y
        else:
            if detect_mouse_in_rect(player_card_rect[i]["x"], player_card_rect[i]["y"], POKER_WIDTH/2, POKER_HEIGHT, mos_x, mos_y) and player_card_rect[i]["y"] == ORG_PLAYER_CARD_Y:
                player_card_rect[i]["y"] = ORG_PLAYER_CARD_Y - delta_y
                choose_card = i
                choose_flag =  True
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
    regulize_card_color()
    while True:
        display_init_select_status()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if detect_mouse_in_rect(LOGIN_X, LOGIN_Y, login_button.get_width(), login_button.get_height(), event.pos[0], event.pos[1]):
                    try:
                        NETWORK_CON  = server_listener()
                        NETWORK_CON.start()
                        if NETWORK_CON:
                            NETWORK_MODE = 1
                            init_flag = 1
                        else:
                            display_error_shade(error_text_0, (SCREEN_WIDTH/2-error_text_0.get_width()/2, SCREEN_HEIGHT/2-100))
                            fill_init_screen()
                    except Exception as err:
                        print err
                        display_error_shade(error_text_0, (SCREEN_WIDTH/2-error_text_0.get_width()/2, SCREEN_HEIGHT/2-100))
                        fill_init_screen()
                if detect_mouse_in_rect(START_X, START_Y, start_button.get_width(), start_button.get_height(), event.pos[0], event.pos[1]):
                    init_flag = 1
            if event.type == KEYDOWN:
                ###print event.key
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
    # fill_background()
    # ready_button.set_colorkey((0,0,0))
    # screen.blit(ready_button, (READY_X, READY_Y))
    print NETWORK_CON.p_client.my_id
    while True:
        #display_ready_select_status()
        # draw avatar
        set_user_info(NETWORK_CON.p_client.my_id, NETWORK_CON.p_client.players_images, NETWORK_CON.p_client.seats_status)
        display_user_info(NETWORK_CON.p_client.my_id, NETWORK_CON.p_client.seats_status)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if detect_mouse_in_rect(READY_X, READY_Y, ready_button.get_width(), ready_button.get_height(), event.pos[0], event.pos[1]):
                    # send ready status to server
                    NETWORK_CON.p_client.ready_clicked()
                    is_ready_flag = True
            if event.type == KEYDOWN:
                ###print event.key
                if event.key == 13 or event.key == 32:
                    is_ready_flag = True
        if is_ready_flag:
            break
    # set ready status, wait until all users are ready
    while True:
        set_user_info(NETWORK_CON.p_client.my_id, NETWORK_CON.p_client.players_images, NETWORK_CON.p_client.seats_status)
        display_user_info(NETWORK_CON.p_client.my_id, NETWORK_CON.p_client.seats_status)
        ready_hover.set_colorkey((0,0,0))
        screen.blit(ready_hover, (READY_X, READY_Y))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            # TODO: add code to cancel ready status
        if NETWORK_CON.p_client.game_status >= 0: 
            print CLIENT_HEAD + "Game Start!\n"
            return True


def set_user_info(player_id, players_images, player_status):
    global players_avatars
    for i in xrange(0,PLAYER_NUM):   
        real_id = (player_id+i)%PLAYER_NUM 
        if player_status[real_id] >= 0 and players_avatars[i] == 0: 
            # avoid client crush caused by avatar
            if players_images[real_id] < 0 or players_images[real_id] > 14:
                players_images[real_id] = 0
            path = IMAGE_DIR + AVATAR_PRE + str(players_images[real_id]) + ".jpg"
            avatar = pygame.image.load(path).convert()
            avatar = pygame.transform.scale(avatar, AVATAR_SIZE)
            players_avatars[i] = avatar
    return


def display_user_info(player_id, player_status):
    # display the other users' info
    fill_background()
    for i in xrange(0, PLAYER_NUM):
        real_id = (player_id+i)%PLAYER_NUM
        if players_avatars[i]:
            if player_status[real_id] == 0:
                ready_button.set_colorkey((0,0,0))
                screen.blit(ready_button, ready_pos_list[i])    
                display_ready_select_status()            
                screen.blit(players_avatars[i], avatars_pos_list[i])
            elif player_status[real_id] == 1:
                ready_hover.set_colorkey((0,0,0))
                screen.blit(ready_hover, ready_pos_list[i])
                screen.blit(players_avatars[i], avatars_pos_list[i])
            else:
                continue

def display_user_avatar(player_id, player_status):
    #print "avatar b"
    fill_background()
    for i in xrange(0, PLAYER_NUM):
        real_id = (player_id+i)%PLAYER_NUM
        if players_avatars[i]:
            if player_status[real_id] == 1:
                screen.blit(players_avatars[i], avatars_pos_list[i])
            else:
                continue
    #print "avatar e"


'''
Display error info
'''
def display_error_shade(error_text, pos):
    s = pygame.Surface(SCREEN_SIZE)
    (b,g,r) = (0,0,0)
    s.fill((b,g,r))
    s.set_alpha(100)  
    screen.blit(s,(0,0)) 
    error_text.set_colorkey((0,0,0))
    screen.blit(error_text, pos)
    ok_button.set_colorkey((0,0,0))
    screen.blit(ok_button, (OK_X, OK_Y)) 
    while True:
        click_flag = False
        display_ok_select_status()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == MOUSEBUTTONDOWN:
                click_flag = True
        if click_flag:
            break
    return False


def initialize_player_card():
    ''' card_list: card original number
        card_rect: card position
    '''
    #player_card_list  = [0] * num_of_player_card
    player_card_rect  = list()

    #all_card_list    = [0] * num_of_total_card

    player_card_x     = ORG_PLAYER_CARD_X
    player_card_y     = ORG_PLAYER_CARD_Y

    
    #random.seed()
    #player_card_list = ini_random_cards(all_card_list, player_card_list, num_of_total_card, num_of_player_card)
    
    screen.blit(background, (0,0))

     
    for i in xrange(0, num_of_player_card): 
        player_card_rect.append({"x":player_card_x+i*POKER_WIDTH/2, "y":player_card_y})
    
    # Block until all cards received
    while True:
        if NETWORK_CON.p_client.cards_received_num == num_of_player_card: 
            break
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

    # display_user_avatar(NETWORK_CON.p_client.my_id, NETWORK_CON.p_client.seats_status)

    #NETWORK_CON.p_client.my_cards.sort()
    display_all_one_by_one(NETWORK_CON.p_client.my_cards, player_card_rect)
    
    #player_card_list.sort()    
    return NETWORK_CON.p_client.my_cards, player_card_rect


def display_player_turn(player_card_rect):
    player_id = NETWORK_CON.p_client.whose_turn
    my_id = NETWORK_CON.p_client.my_id
    screen_id = (player_id - my_id + 4) % 4
    print screen_id
    print turn_flag.get_width(), turn_flag.get_height()
    turn_flag.set_colorkey((0,0,0))
    screen.blit(turn_flag, turn_flag_pos_list[screen_id])
    print player_card_rect
    print turn_flag_pos_list
    return


def display_result_on_panel():
    panel_height = 270
    panel_width = panel_height/0.618
    # panel_x = ORG_PLAYER_CARD_X-panel_width-3*TOP_MARGIN
    # panel_y = SCREEN_HEIGHT-TOP_MARGIN-panel_height
    panel_x = SCREEN_WIDTH/3 - 40
    panel_y = SCREEN_HEIGHT/3
    panel_x_1 = panel_x + 10
    panel_x_2 = panel_x + 20 + (panel_width - 40)/3
    panel_x_3 = panel_x + 30 + (panel_width - 40)*2/3
    s = pygame.Surface((panel_width, panel_height))
    (b,g,r) = (255,255,255)
    s.fill((b,g,r))
    s.set_alpha(100)
    # draw panel
    screen.blit(s, (panel_x, panel_y))
    # draw cards
    # (scale_w, scale_h) = (POKER_WIDTH/12*5, POKER_HEIGHT/12*5)
    # gap_x = POKER_WIDTH/5
    # gap_y = 5
    # discard_num = len(discard_card_list)
    result = NETWORK_CON.p_client.result
    screen.blit(write_to_screen("penalty", (255,255,0), 36),(panel_x_2, panel_y))
    screen.blit(write_to_screen("score", (255,255,0), 36),(panel_x_3, panel_y))
    for i in xrange(0, 4):
        if i == NETWORK_CON.p_client.my_id:
            screen.blit(write_to_screen("player "+str(i+1), (0,255,255), 36),(panel_x_1, panel_y + (i+1)*50))
            screen.blit(write_to_screen(str(result[2*i]), (0,255,255), 36),(panel_x_2, panel_y + (i+1)*50))
            screen.blit(write_to_screen(str(result[2*i+1]), (0,255,255), 36),(panel_x_3, panel_y + (i+1)*50))
        else:
            screen.blit(write_to_screen("player "+str(i+1), (255,0,255), 36),(panel_x_1, panel_y + (i+1)*50))
            screen.blit(write_to_screen(str(result[2*i]), (255,255,0), 36),(panel_x_2, panel_y + (i+1)*50))
            screen.blit(write_to_screen(str(result[2*i+1]), (255,255,0), 36),(panel_x_3, panel_y + (i+1)*50))
    # for i in xrange(0,discard_num):
    #     #change_single_card_color(discard_card_list[i], SHADOW, WHITE)
    #     screen.blit(pygame.transform.scale(num_to_poker_cards(discard_card_list[i]), (scale_w, scale_h)), 
    #         ( panel_x+(i%5)*scale_w+((i+1)%5)*gap_y, panel_y+i/5*scale_h+(i/5+1)*gap_y ) )


def handle_screen_msg(player_card_list, player_card_rect):
    loop_number = 5   
    choose_flag = False 
    choose_card = -1
    while NETWORK_CON.p_client.game_status:  
    
        for event in pygame.event.get():
            if event.type == QUIT:
                if display_error_shade(error_text_1, (SCREEN_WIDTH/2-error_text_0.get_width()/2, SCREEN_HEIGHT/2-100)):
                    exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    choose_flag, choose_card = display_game_select_status(player_card_rect, 
                        NETWORK_CON.p_client.players_disposable_cards_num[NETWORK_CON.p_client.my_id], 
                        event.pos)
                    # choose_card_index = -1
                    # for x in xrange(0, num_of_player_card):
                    #     if NETWORK_CON.p_client.my_cards_status[x] < 2:
                    #         choose_card_index += 1
                    #         if choose_card_index == choose_card:
                    #             choose_card = x
                    #             break
                if event.button == 3: 
                    if choose_flag and choose_card > -1 and NETWORK_CON.p_client.my_id == NETWORK_CON.p_client.whose_turn: 
                        choose_flag = False
                        #send_message('player select card: '+str(player_card_list[choose_card]))  
                        #NETWORK_CON.p_client.card_played(player_card_list[choose_card]) 
                        print CLIENT_HEAD + 'player select card: ' + str(choose_card)
                        NETWORK_CON.p_client.card_played(choose_card) 
                        choose_card = -1          
            if event.type == KEYDOWN:
                print event.key
                if event.key == K_ESCAPE :
                    exit()     
            
        # Sdisplay_user_avatar(NETWORK_CON.p_client.my_id, NETWORK_CON.p_client.seats_status)        
        display_all(NETWORK_CON.p_client.my_cards, 
                    player_card_rect, 
                    NETWORK_CON.p_client.players_disposable_cards_num, 
                    NETWORK_CON.p_client.my_cards_status,
                    NETWORK_CON.p_client.boundaries)
        # pygame.display.update()

        if NETWORK_CON.p_client.game_status == 2:
            display_result_on_panel()
            pygame.display.update()
            time.sleep(10)

        if NETWORK_CON.p_client.game_status < 1:
            break


def send_message(text):
    # send to server
    print text 
    if NETWORK_MODE:
        NETWORK_CON.p_client.send_msg(text)

    return


def main():
    try:
        #
        display_init_screen()
        #
        while True:
            if is_user_ready():
                player_card_list, player_card_rect = initialize_player_card()
                #
                handle_screen_msg(player_card_list, player_card_rect)
                
        # exit the game
        exit()
    except Exception as err:
        print err		


if __name__ == "__main__":
    main()