import socket
import select
import sys
import os
from threading import Thread

my_id = -1
my_cards = [-1] * 13
# 0: possessed card; 1: valid card; 2: displayed card; 3: useless card
my_cards_state = [-1] * 13
valid_cards_num = 0

'''
net mode:   connect to server
local mode: play with AI
'''
def login(hostname = 'localhost', port=10086, nickname='lei'):
    return poker_client(hostname, port, nickname)


class poker_client:

    def __init__(self, host, port, nickname):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.input = self.socket.makefile('rb', 0)
        self.output = self.socket.makefile('wb', 0)

        #Send the given nickname to the server.
        authenticationDemand = self.input.readline().decode('utf-8')
        if not authenticationDemand.startswith("Is Wqf handsome?"):
            raise Exception ("This doesn't seem to be a Python poker Server.")
        self.output.write((nickname + '\r\n').encode('utf-8'))
        response = self.input.readline().strip().decode('utf-8')
        if not response.startswith("Hello"):
            raise Exception (response)
        print(response)

        #Start out by printing out the list of members.
        self.output.write(('/names\r\n').encode('utf-8'))
        print("Currently in the poker room:", self.input.readline().decode('utf-8').strip())

        self.run()
    
    def send_msg(self, text):
        self.output.write((text + '\r\n').encode('utf-8'))


    def run(self):
        ''' Start a seperate thread to receive message from the server
        '''
        s_listener = self.server_listener(self.input)
        s_listener.start()


    class server_listener(Thread):
            """A inner class that receive message from the poker server
            until it's told to stop."""

            def __init__(self, server_input):
                """Make this thread a daemon thread, so that if the Python
                interpreter needs to quit it won't be held up waiting for this
                thread to die."""
                Thread.__init__(self)
                self.setDaemon(True)
                self.input = server_input
                self.done = False

            def run(self):
                while not self.done:
                    server_text = self.input.readline().decode('utf-8')
                    if server_text:
                        print server_text.strip()
                        recv_msg(server_text)

def recv_msg(msg):
    msg = msg.split(";");
    if msg[0] == "0" and len(msg) == 2:
        if msg[1] >= 0 && msg[1] <= 3:
            my_id = (int)msg[1]
    elif msg[0] == "1" and len(msg) == 6:
        if not my_id == -1:
            my_cards[(int)msg[1]] = (int)msg[my_id+2]
            my_cards_state[(int)msg[1]] = 0 # possessed card
    elif msg[0] == "2" and len(msg) == 3:
        last_player = [int(x) for x in msg[1].split(":")]
        boundaries = [int(x) for x in msg[2].split(":")]
        if len(last_player) == 3 and len(boundaries) == 8:
            update_display = last_player[0]
            last_player_id = last_player[1]
            last_card = last_player[2]
            if update_display == 0:
                compute_and_show_valid_cards(boundaries)
                display_cards(boundaries, last_card)
            turn_to_player((last_player_id + 1) % 4)
    elif msg[0] == "3" and len(msg) == 2:
        result = [int(x) for x in msg[1].split(":")]
        show_result(result)
        my_cards_state = [-1] * 13

def compute_and_show_valid_cards(boundaries):
    valid_cards_num = 0
    for x in my_cards:
        if my_cards_state[x] == 0: # possessed card
            color = (int)(my_cards[x] / 13)
            number = my_cards[x] % 13
            if number < 6:
                if boundaries[color * 2] == number + 1:
                    my_cards_state[x] = 1 # valid card
                    valid_cards_num++
            elif number > 6:
                if boundaries[color * 2 + 1] == number - 1:
                    my_cards_state[x] = 1 # valid card
                    valid_cards_num++
            else:
                my_cards_state[x] = 1 # valid card
                valid_cards_num++
    for x in my_cards_state:
        if my_cards_state[x] == 1:
            ### show the valid card

def display_cards(boundaries, last_card):
    ### display cards

def turn_to_player(current_player_id):
    if current_player_id == my_id:
        if valid_cards_num == 0:
            ### now you should cover a card
            ### re-display my useless cards and possessed cards
            useless_card = 00
            send_msg(2, useless_card)
        else:
            ### now you should play a card
            ### re-display my possessed cards
            played_card = 00
            send_msg(1, played_card)

def show_result(result):
    # player 0 penalty: result[0]; player 0 score: result[1]; and the like

def ready_clicked():
    send_msg(0, my_id)

def send_msg(msg_type, msg_para):
    send_text = "%d;%d" % (msg_type, msg_para)
    ### send...
