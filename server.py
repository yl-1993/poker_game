"""
message type:
  user:   login, ready
  poker:  random, shuffle
"""

import SocketServer
import re
import socket
import time
import random
from utils import ini_random_cards

login_player_num = 0
num_of_total_card = 52
num_of_player_card = 13
whose_turn = -1
cards_played = 0
player_penalty = [0] * 4
player_score = [0] * 4
boundaries = [-1] * 8
whose_card = [-1] * num_of_total_card
seats_status = [-1] * 4
ready_num = 0
super_seven = 0
players_disposable_cards_num = [13] * 4
players_discarded_cards_num = [0] * 4
players_images = [-1] * 4
player_id = dict()

class ClientError(Exception):
  "An exception thrown because the client gave bad input to the server."
  pass

class python_poker_server(SocketServer.ThreadingTCPServer):
  "the server class"
  
  def __init__(self, server_address, RequestHandlerClass):
    """Set up an initially empty mapping between a user' s nickname
    and the file-like object used to send data to that user."""
    SocketServer.ThreadingTCPServer.__init__(self, server_address, RequestHandlerClass)
    self.users = {}

class RequestHandler(SocketServer.StreamRequestHandler):
  """Handles the life cycle of a user's connection to the poker server: connecting,
  sending message, running server commands, and disconnecting."""

  def handle(self):
    """Handles a connection: gets the user's nickname, then
    processes input from the user until they quit or drop the
    connection."""

    global login_player_num
    global num_of_total_card
    global num_of_player_card
    global whose_turn
    global cards_played
    global player_penalty
    global player_score
    global boundaries
    global whose_card
    global seats_status
    global ready_num
    global super_seven
    global players_disposable_cards_num
    global players_discarded_cards_num
    global players_images
    global player_id

    self.nickname = None
    self.private_message("Is Wqf handsome?")
    nickname=self._readline()
    done = False
    try:
      self.nick_command(nickname)
      if login_player_num == 4:
        self.private_message('Sorry %s, the Python poker Server has filled up.' % self.nickname)
        return
      self.private_message('Hello %s, welcome to the Python poker Server.' % self.nickname)
      self.broadcast('%s has joined the poker.' % self.nickname)
      player_id[self.nickname] = -1
      for x in xrange(0, 4):
        if seats_status[x] == -1:
          player_id[self.nickname] = x
          seats_status[x] = 0
          login_player_num += 1
          players_images[x] = random.randint(x*4, x*4+3)
          if players_images[x] == 15:
            players_images[x] = random.randint(12, 14)
          # new player come: send 0
          newstr = '%d;%d;' % (0, player_id[self.nickname])
          newstr += '%d:%d:' % (players_images[0], players_images[1])
          newstr += '%d:%d;' % (players_images[2], players_images[3])
          newstr += '%d:%d:' % (seats_status[0], seats_status[1])
          newstr += '%d:%d' % (seats_status[2], seats_status[3])
          self.broadcast(newstr)
          break
      #print('%s has joined the poker.' %nickname) #print in server
    except (ClientError) as error:
      self.private_message(error.args[0])
      done = True
    except socket.error:
      done = True

    #Now they're logged in, let them poker
    while not done:
      try:
        done = self.process_input()
      except (ClientError) as error: #wrong:ClientError(error)
        self.private_message(str(error))
      except socket.error:
        done = True
        
  def finish(self):
    """Automatically called when handle() is done!!!"""

    global login_player_num
    global num_of_total_card
    global num_of_player_card
    global whose_turn
    global cards_played
    global player_penalty
    global player_score
    global boundaries
    global whose_card
    global seats_status
    global ready_num
    global super_seven
    global players_disposable_cards_num
    global players_discarded_cards_num
    global players_images
    global player_id

    if self.nickname:
      #The user successfully connected before disconnecting.
      #Broadcast that they're quitting to everyone else.
      try:
        message = '%s has quit.' % self.nickname
        if hasattr(self, 'partingWords'):
          message = '%s has quit: %s' % (self.nickname, self.partingWords)
        self.broadcast(message, False)

        if player_id[self.nickname] >= 0 and player_id[self.nickname] <= 3:
          if ready_num == 4: #game already started
            ready_num = 0
            seats_status = [0] * 4
          elif seats_status[player_id[self.nickname]] == 1:
            seats_status[player_id[self.nickname]] = -1
            ready_num -= 1
          elif seats_status[player_id[self.nickname]] == 0:
            seats_status[player_id[self.nickname]] = -1
          login_player_num -= 1
          newstr = '%d;' % 0
          newstr += '%d:%d:' % (seats_status[0], seats_status[1])
          newstr += '%d:%d' % (seats_status[2], seats_status[3])
          self.broadcast(newstr, False)
      except Exception as err:
        print err
        login_player_num = 0
        ready_num = 0
        for x in xrange(0, 4):
          seats_status[x] = -1
      whose_turn = -1
      cards_played = 0
      player_penalty = [0] * 4
      player_score = [0] * 4
      boundaries = [-1] * 8
      whose_card = [-1] * num_of_total_card
      super_seven = 0
      players_disposable_cards_num = [13] * 4
      players_discarded_cards_num = [0] * 4
      player_id[self.nickname] = -1

      
      #Remove the user from the list so we don't keep trying
      #to send them messages.
      if self.server.users.get(self.nickname):
        del(self.server.users[self.nickname])
    self.request.shutdown(2)
    self.request.close()
    
  def process_input(self):
    """Reads a line from the socket input and either runs it as a
    command, or broadcasts it as poker text."""

    global login_player_num
    global num_of_total_card
    global num_of_player_card
    global whose_turn
    global cards_played
    global player_penalty
    global player_score
    global boundaries
    global whose_card
    global seats_status
    global ready_num
    global super_seven
    global players_disposable_cards_num
    global players_discarded_cards_num
    global players_images
    global player_id

    done = False
    l = self._readline()
    command, arg = self._parse_command(l)
    if command:
      done = command(arg)
    else:

      msg = l.split(";")
      # new player ready: receive 0
      if msg[0] == "0" and len(msg) == 2:
        this_player = int(msg[1])
        seats_status[this_player] = 1
        ready_num += 1
        print ready_num
        # new player ready: send 0
        newstr = '%d;' % 0
        newstr += '%d:%d:' % (seats_status[0], seats_status[1])
        newstr += '%d:%d' % (seats_status[2], seats_status[3])
        self.broadcast(newstr)
        # all players ready
        if ready_num == 4:
          p_card_list = dict()
          ini_random_cards(whose_card, p_card_list, num_of_total_card, num_of_player_card)
          for x in xrange(0, num_of_player_card):
            time.sleep(0.5)
            # distribute cards: send 1
            newstr = '%d;%d;%d;%d;%d;%d' % (1, x, p_card_list[0][x], p_card_list[1][x], p_card_list[2][x], p_card_list[3][x])
            self.broadcast(newstr)
          boundaries[6] = 6
          boundaries[7] = 6
          whose_turn = whose_card[13*7+6]
          players_disposable_cards_num[whose_turn] -= 1
          # display cards: send 2
          newstr = '%d;%d:%d:%d;' % (2, 0, whose_turn, 13*7+6)
          newstr += '%d:%d:' % (boundaries[0], boundaries[1])
          newstr += '%d:%d:' % (boundaries[2], boundaries[3])
          newstr += '%d:%d:' % (boundaries[4], boundaries[5])
          newstr += '%d:%d;' % (boundaries[6], boundaries[7])
          newstr += '%d:%d:' % (players_disposable_cards_num[0], players_disposable_cards_num[1])
          newstr += '%d:%d;' % (players_disposable_cards_num[2], players_disposable_cards_num[3])
          newstr += '%d:%d:' % (players_discarded_cards_num[0], players_discarded_cards_num[1])
          newstr += '%d:%d' % (players_discarded_cards_num[2], players_discarded_cards_num[3])
          self.broadcast(newstr)
          whose_turn = (whose_turn + 1) % 4
          cards_played += 1
      # played a card: receive 1
      elif msg[0] == "1":
        this_card = int(msg[1])
        card_color = int(this_card / 13)
        card_number = this_card % 13
        if card_number < 6:
          boundaries[card_color*2] = card_number
        elif card_number > 6:
          boundaries[card_color*2+1] = card_number
        else:
          boundaries[card_color*2] = boundaries[card_color*2+1] = card_number
        # display cards: send 2
        newstr = '%d;%d:%d:%d;' % (2, 0, whose_turn, this_card)
        newstr += '%d:%d:' % (boundaries[0], boundaries[1])
        newstr += '%d:%d:' % (boundaries[2], boundaries[3])
        newstr += '%d:%d:' % (boundaries[4], boundaries[5])
        newstr += '%d:%d;' % (boundaries[6], boundaries[7])
        newstr += '%d:%d:' % (players_disposable_cards_num[0], players_disposable_cards_num[1])
        newstr += '%d:%d;' % (players_disposable_cards_num[2], players_disposable_cards_num[3])
        newstr += '%d:%d:' % (players_discarded_cards_num[0], players_discarded_cards_num[1])
        newstr += '%d:%d' % (players_discarded_cards_num[2], players_discarded_cards_num[3])
        self.broadcast(newstr)
        whose_turn = (whose_turn + 1) % 4
        cards_played += 1
        if card_number == 6 and cards_played >= 49:
          super_seven = 1
      # failed to play a card: receive 2
      elif msg[0] == "2":
        this_card = int(msg[1])
        card_number = this_card % 13
        player_penalty[whose_turn] += card_number + 1
        # display cards: send 2
        newstr = '%d;%d:%d:%d;' % (2, 1, whose_turn, this_card)
        newstr += '%d:%d:' % (boundaries[0], boundaries[1])
        newstr += '%d:%d:' % (boundaries[2], boundaries[3])
        newstr += '%d:%d:' % (boundaries[4], boundaries[5])
        newstr += '%d:%d;' % (boundaries[6], boundaries[7])
        newstr += '%d:%d:' % (players_disposable_cards_num[0], players_disposable_cards_num[1])
        newstr += '%d:%d;' % (players_disposable_cards_num[2], players_disposable_cards_num[3])
        newstr += '%d:%d:' % (players_discarded_cards_num[0], players_discarded_cards_num[1])
        newstr += '%d:%d' % (players_discarded_cards_num[2], players_discarded_cards_num[3])
        self.broadcast(newstr)
        whose_turn = (whose_turn + 1) % 4
        cards_played += 1
      if cards_played == num_of_total_card:
        # game over: send 3
        times = 1
        if super_seven == 1:
          times = 8
        else:
          for x in xrange(0, 4):
            if player_penalty[x] == 0:
              times *= 2
        penalty_sum = 0
        for x in xrange(0, 4):
          penalty_sum += player_penalty[x]
        for x in xrange(0, 4):
          player_score[x] = (penalty_sum - player_penalty[x] * 4) * times
        newstr = '%d;' % 3
        newstr += '%d:%d:' % (player_penalty[0], player_score[0])
        newstr += '%d:%d:' % (player_penalty[1], player_score[1])
        newstr += '%d:%d:' % (player_penalty[2], player_score[2])
        newstr += '%d:%d' % (player_penalty[3], player_score[3])
        self.broadcast(newstr)
        whose_turn = -1
        cards_played = 0
        player_penalty = [0] * 4
        player_score = [0] * 4
        boundaries = [-1] * 8
        whose_card = [-1] * num_of_total_card
        seats_status = [0] * 4
        ready_num = 0
        super_seven = 0
        players_disposable_cards_num = [13] * 4
        players_discarded_cards_num = [0] * 4

      l = '<%s> %s\n' % (self.nickname, l)
      print l
      self.broadcast(l)
    return done
    
  def nick_command(self, nickname):
    "Attempts to change a user's nickname."
    if not nickname:
      raise ClientError('No nickname provided.')
    # if not self.NICKNAME.match(nickname):
    #   raise ClientError('Invalid nickname: %s' % nickname)
    if nickname == self.nickname:
      raise ClientError('You\'re already known as %s.' % nickname)
    while self.server.users.get(nickname,None):
      nickname = nickname + str(random.randint(0,10))
      #raise ClientError('There\'s already a user named "%s" here.' %nickname)
    print nickname
    oldNickname = None
    if self.nickname:
      oldNickname=self.nickname
      del(self.server.users[self.nickname])
    self.server.users[nickname]=self.wfile
    self.nickname=nickname
    if oldNickname:
      self.broadcast('%s is now known as %s' % (oldNickname, self.nickname))
    
  def quit_command(self, partingWords):
    """Tells the other users that this user has quit, then makes
    sure the handler will close this connection."""
    if partingWords:
      self.partingWords = partingWords
    #Returning True makes sure the user will be disconnected.
    return True
    
  def names_command(self, ignored):
    "Returns a list of the users in this poker room."
    self.private_message(', '.join(self.server.users.keys()))
    
  #Below are helper methods
  
  def broadcast(self, message, include_this_user=True):
    """Send a message to every connected user, possibly exempting the
    user who's the cause of the message."""
    message = self._ensure_newline(message)
    for user, output in self.server.users.items():
      if include_this_user or user != self.nickname:
        output.write(message.encode('utf-8'))
  
  def private_message(self, message):
    "Send a private message to this user."
    self.wfile.write(self._ensure_newline(message).encode('utf-8')) #must encode before send
    
  def _readline(self):
    "Reads a line, removing any whitespace."
    return self.rfile.readline().strip().decode('utf-8') #must decode after rec
    
  def _ensure_newline(self, s):
    "Makes sure a string ends in a newline."
    if s and s[-1] !='\n':
      s += '\r\n'
    return s
    
  def _parse_command(self, input):
    """Try to parse a string as a command to the server.If it's an
    implemented command, run the corresponding method.
    input /xxx, runs xxxCommand"""
    commandMethod, arg = None, None
    if input and input[0]=='/':
      if len(input) < 2:
        raise ClientError('Invalid command: "%s"' % input)
      commandAndArg = input[1:].split(' ',1)
      if len(commandAndArg) == 2:
        command, arg = commandAndArg
      else:
        command = commandAndArg[0] #can not without [],otherwise it's list ,which just has one member.
      commandMethod = getattr(self, command + 'Command', None)
      if not commandMethod:
        raise ClientError('No such command: "%s"' %command)
    #if input[0]!='/', which means input is not a command
    #then commandMethod will be None
    return commandMethod, arg


'''
unit test
'''
if __name__ == '__main__':
  #import sys
  # if len(sys.argv) < 3:
  #   print('Usage: %s [hostname] [port number]' %sys.argv[0])
  #   sys.exit(1)
  # hostname = sys.argv[1]
  # port = int(sys.argv[2])
  hostname = 'localhost'
  port = 10086
  python_poker_server((hostname,port),RequestHandler).serve_forever()