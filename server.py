"""
message type:
  user:   login, ready
  poker:  random, shuffle
"""

import SocketServer
import re
import socket
import time

login_player_num = 0
num_of_total_card = 52
num_of_player_card = 13
whose_turn = -1
cards_played = 0
player_penalty = [0] * 4
player_score = [0] * 4
boundaries = [-1] * 8
whose_card = [-1] * num_of_total_card
seats_state = [-1] * 4
ready_num = 0
super_seven = 0
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
  
  NICKNAME = re.compile('^[A-Za-z0-9_-]+$') #regex for a valid nickname
  
  def handle(self):
    """Handles a connection: gets the user's nickname, then
    processes input from the user until they quit or drop the
    connection."""
    if login_player_num == 4:
      return
    self.nickname = None
    self.private_message("Is Wqf handsome?")
    nickname=self._readline()
    done = False
    try:
      self.nick_command(nickname)
      self.private_message('Hello %s, welcome to the Python poker Server.' % nickname)
      self.broadcast('%s has joined the poker.' %nickname, False)
      #print('%s has joined the poker.' %nickname) #print in server
    except (ClientError) as error:
      self.private_message(error.args[0])
      done = True
    except socket.error:
      done = True
    
    if not done:
      player_id[nickname] = -1
      for x in xrange(0, 4):
        if seats_state[x] == -1:
          player_id[nickname] = x
          seats_state[x] = 0
      # new player come: send 0
      self.broadcast('%d;%d' % (0, player_id[nickname]), False)
      login_player_num+=1

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
    if self.nickname:
      #The user successfully connected before disconnecting.
      #Broadcast that they're quitting to everyone else.
      message = '%s has quit.' % self.nickname
      if hasattr(self, 'partingWords'):
        message = '%s has quit: %s' % (self.nickname, self.partingWords)
      self.broadcast(message, False)

      if player_id[self.nickname] >= 0 and player_id[self.nickname] <= 3:
        if seats_state[player_id[self.nickname]] == 1:
          ready_num-=1
        seats_state[player_id[self.nickname]] = -1
        player_id[self.nickname] = -1
        login_player_num-=1
      
      #Remove the user from the list so we don't keep trying
      #to send them messages.
      if self.server.users.get(self.nickname):
        del(self.server.users[self.nickname])
    self.request.shutdown(2)
    self.request.close()
    
  def process_input(self):
    """Reads a line from the socket input and either runs it as a
    command, or broadcasts it as poker text."""
    done = False
    l = self._readline()
    command, arg = self._parse_command(l)
    if command:
      done = command(arg)
    else:

      # p_id = player_id[self.nickname]
      msg = l.split(";")
      # new player ready: receive 0
      if msg[0] == "0":
        this_player = int(msg[1])
        seats_state[this_player] = 1
        ready_num+=1
        # all players ready
        if ready_num == 4:
          p_card_list = dict()
          ini_random_cards(whose_card, p_card_list, num_of_total_card, num_of_player_card)
          for x in xrange(0, num_of_player_card):
            time.sleep(0.5)
            # distribute cards: send 1
            newstr = '%d;%d;%d;%d;%d;%d' % (1, x, p_card_list[0][x], p_card_list[1][x], p_card_list[2][x], p_card_list[3][x])
            self.broadcast(newstr, False)
          boundaries[6] = 6
          boundaries[7] = 6
          whose_turn = whose_card[13*7+6]
          # display cards: send 2
          newstr = '%d;%d:%d:%d;' % (2, 0, whose_turn, 13*7+6)
          newstr += '%d:%d:' % (boundaries[0], boundaries[1])
          newstr += '%d:%d:' % (boundaries[2], boundaries[3])
          newstr += '%d:%d:' % (boundaries[4], boundaries[5])
          newstr += '%d:%d' % (boundaries[6], boundaries[7])
          self.broadcast(newstr, False)
          whose_turn = (whose_turn + 1) % 4
          cards_played+=1
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
        newstr += '%d:%d' % (boundaries[6], boundaries[7])
        self.broadcast(newstr, False)
        whose_turn = (whose_turn + 1) % 4
        cards_played+=1
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
        newstr += '%d:%d' % (boundaries[6], boundaries[7])
        self.broadcast(newstr, False)
        whose_turn = (whose_turn + 1) % 4
        cards_played+=1
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
        self.broadcast(newstr, False)
        whose_turn = -1
        cards_played = 0
        player_penalty = [0] * 4
        player_score = [0] * 4
        boundaries = [-1] * 8
        whose_card = [-1] * num_of_total_card
        seats_state = [0] * 4
        ready_num = 0
        super_seven = 0

      l = '<%s> %s\n' % (self.nickname, l)
      print l
      self.broadcast(l)
    return done
    
  def nick_command(self,nickname):
    "Attempts to change a user's nickname."
    if not nickname:
      raise ClientError('No nickname provided.')
    if not self.NICKNAME.match(nickname):
      raise ClientError('Invalid nickname: %s' % nickname)
    if nickname == self.nickname:
      raise ClientError('You\'re already known as %s.' % nickname)
    if self.server.users.get(nickname,None):
      raise ClientError('There\'s already a user named "%s" here.' %nickname)
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
  
  def broadcast(self, message, includeThisUser=True):
    """Send a message to every connected user, possibly exempting the
    user who's the cause of the message."""
    message = self._ensure_newline(message)
    for user, output in self.server.users.items():
      if includeThisUser or user != self.nickname:
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