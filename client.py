import socket
import select
import sys
import os
from threading import Thread

'''
net mode:   connect to server
local mode: play with AI
'''
def login(hostname = 'localhost', port=10086, nickname='wen'):
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
