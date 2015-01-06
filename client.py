import socket
import select
import sys
import os
import time
from threading import Thread
from config import CLIENT_HEAD, SERVER_HEAD


'''
net mode:   connect to server
local mode: play with AI
'''
def login(hostname = 'localhost', port=10086, nickname='huang'):
    return poker_client(hostname, port, nickname)


class poker_client:

    # before game starts: -1; distributing cards: 0; game starts: 1; game over: 2
    game_status = -1

    my_id = -1
    players_images = [-1] * 4
    seats_status = [-1] * 4 # empty: -1; seated: 0; ready: 1

    cards_received_num = 0
    my_cards = [-1] * 13

    boundaries = [-1] * 8
    last_card = -1
    whose_turn = -1
    players_disposable_cards_num = [13] * 4
    players_discarded_cards_num = [0] * 4
    my_cards_status = [-1] * 13 # 0: disposable-card(common); 1: valid-card(change color); 2: displayed-card; 3: discarded-card
    valid_cards_num = 0

    result = [-1] * 8

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
        print("Currently in the poker room:", self.input.readline().decode('utf-8').strip())

        #self.run()
    
    def send_msg(self, text):
        self.output.write((text + '\r\n').encode('utf-8'))


    def run(self):
        ''' Start a seperate thread to receive message from the server
        '''
        s_listener = self.server_listener(self.input)
        s_listener.start()


    def recv_msg(self, message):
        msg = message.split(";");
        if msg[0] == "0" and len(msg) == 4:
            self.game_status = -1
            if self.my_id < 0:
                self.my_id = int(msg[1])
            self.players_images = [int(x) for x in msg[2].split(":")]
            self.seats_status = [int(x) for x in msg[3].split(":")]
        elif msg[0] == "0" and len(msg) == 2:
            self.game_status = -1
            self.seats_status = [int(x) for x in msg[1].split(":")]
        elif msg[0] == "1" and len(msg) == 5:
            self.game_status = 0
            self.my_cards = [int(x) for x in msg[self.my_id + 1].split(":")]
            #for x in xrange(0, len(self.my_cards)):
                #time.sleep(0.5)
                #self.my_cards_status[x] = 0 # disposable card
                #self.cards_received_num = x + 1
            self.my_cards_status = [0] * len(self.my_cards)
            self.cards_received_num = len(self.my_cards)
        elif msg[0] == "2" and len(msg) == 5:
            self.game_status = 1
            last_player = [int(x) for x in msg[1].split(":")]
            self.boundaries = [int(x) for x in msg[2].split(":")]
            self.players_disposable_cards_num = [int(x) for x in msg[3].split(":")]
            self.players_discarded_cards_num = [int(x) for x in msg[4].split(":")]
            if len(last_player) == 3 and len(self.boundaries) == 8:
                update_display = last_player[0]
                self.whose_turn = (last_player[1] + 1) % 4
                self.last_card = last_player[2]
                if update_display == 0:
                    self.compute_and_show_valid_cards(self.boundaries)
        elif msg[0] == "3" and len(msg) == 2:
            self.game_status = 2
            self.result = [int(x) for x in msg[1].split(":")]
        else:
            print CLIENT_HEAD + "cannot parse the server message: " + message


    def compute_and_show_valid_cards(self, boundaries):
        self.valid_cards_num = 0
        for x in xrange(0, len(self.my_cards)):
            if self.my_cards_status[x] == 0: # disposable card
                color = int((self.my_cards[x] - 1) / 13)
                number = (self.my_cards[x] - 1) % 13 + 1
                if number < 7:
                    if boundaries[color * 2] == number + 1:
                        self.my_cards_status[x] = 1 # valid card
                        self.valid_cards_num += 1
                elif number > 7:
                    if boundaries[color * 2 + 1] == number - 1:
                        self.my_cards_status[x] = 1 # valid card
                        self.valid_cards_num += 1
                else:
                    self.my_cards_status[x] = 1 # valid card
                    self.valid_cards_num += 1

    ### dianji chupai, diaoyong zhege hanshu
    def card_played(self, card_id):
        if self.valid_cards_num == 0:
            discarded_card = card_id
            self.my_cards_status[discarded_card] = 3
            send_text = "%d;%d" % (2, self.my_cards[discarded_card])
            self.send_msg(send_text)
        elif self.valid_cards_num > 0 and self.my_cards_status[card_id] == 1:
            played_card = card_id
            self.my_cards_status[played_card] = 2
            send_text = "%d;%d" % (1, self.my_cards[played_card])
            self.send_msg(send_text)
        else:
            return

    ### dianji ready zhihou, diaoyong zhege hanshu
    def ready_clicked(self):
        send_text = "%d;%d" % (0, self.my_id)
        self.send_msg(send_text)
        return


class server_listener(Thread):
        """A inner class that receive message from the poker server
        until it's told to stop."""

        def __init__(self):
            """Make this thread a daemon thread, so that if the Python
            interpreter needs to quit it won't be held up waiting for this
            thread to die."""
            Thread.__init__(self)
            self.setDaemon(True)
            self.p_client = login()
            #self.input = server_input
            self.done = False

        def run(self):
            while not self.done:
                server_text = self.p_client.input.readline().decode('utf-8')
                if server_text:
                    print SERVER_HEAD + server_text.strip()
                    self.p_client.recv_msg(server_text)
                    print CLIENT_HEAD + "Waiting server message..."