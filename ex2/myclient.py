import sys
from ex2utils import Client

import time

class IRCClient(Client):
    def onMessage(self, socket, message):
        print(message)
        return True

ip =sys.argv[1]
port = int(sys.argv[2])

client = IRCClient()

client.start(ip,port)

while client.isRunning():
    # if(client.socket.connect((ip,port))):
        message = input()
        message = message.encode()
        client.send(message.strip()+b'\n')

client.stop()
