import socket
import select
import sys
import os
from threading import Thread

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

        #self.run()
    def send_msg(self, text):
        self.output.write((text + '\r\n').encode('utf-8'))

    def run(self):
        """Start a separate thread to gather the input from the
        keyboard even as we wait for messages to come over the
        network. This makes it possible for the user to simultaneously
        send and receive poker text."""
        
        propagateStandardInput = self.PropagateStandardInput(self.output)
        propagateStandardInput.start()

        #Read from the network and print everything received to standard
        #output. Once data stops coming in from the network, it means
        #we've disconnected.
        inputText = True
        while inputText:
            inputText = self.input.readline().decode('utf-8')
            if inputText:
                print (inputText.strip())
        propagateStandardInput.done = True

    class PropagateStandardInput(Thread):
        """A class that mirrors standard input to the poker server
        until it's told to stop."""

        def __init__(self, output):
            """Make this thread a daemon thread, so that if the Python
            interpreter needs to quit it won't be held up waiting for this
            thread to die."""
            Thread.__init__(self)
            self.setDaemon(True)
            self.output = output
            self.done = False

        def run(self):
            "Echo standard input to the poker server until told to stop."
            while not self.done:
                inputText = sys.stdin.readline().strip() #no need to decode when read from stdin
                if inputText:
                    self.output.write((inputText + '\r\n').encode('utf-8'))


'''
unit test
'''
if __name__ == '__main__':
    import sys
    #See if the user has an OS-provided 'username' we can use as a default 
    #poker nickname. If not, they have to specify a nickname.
    try:
        import pwd
        defaultNickname = pwd.getpwuid(os.getuid())[0]
    except ImportError:
        defaultNickname = None

    if len(sys.argv) < 3 or not defaultNickname and len(sys.argv) < 4:
        print('Usage: %s [hostname] [port number] [username]' % sys.argv[0])
        sys.exit(1)

    hostname = sys.argv[1]
    port = int(sys.argv[2])

    if len(sys.argv) > 3:
        nickname = sys.argv[3]
    else:
        #We must be on a system with usernames, or we would have
        #exited earlier.
        nickname = defaultNickname

    poker_client(hostname, port, nickname)