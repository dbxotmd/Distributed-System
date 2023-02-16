import sys
from ex2utils import Server

class MyServer(Server):

    numberofclient =0
    listofclient = {}
    connecting = {}

    def onStart(self):
        print("Myserver started")

    def onStop(self):
        print("Server stopped")

    def onConnect(self,socket):
        MyServer.numberofclient  += 1
        print("client connected")
        print("client number:",MyServer.numberofclient)
        socket.client = None
        message = "Type your screen name"
        message = message.encode()
        socket.send(message)

    def onDisconnect(self,socket):
        MyServer.numberofclient  -= 1
        print("Disconnected")
        print("client number:",MyServer.numberofclient)
        MyServer.connecting.pop(socket.client)
        message = "Server is stopped Press Enter to quit"
        message = message.encode()
        socket.send(message)


    def onMessage(self,socket,message):
        if socket.client== None:
            if message in MyServer.listofclient:
                message = "Type your screen name Again"
                message = message.encode()
                socket.send(message)
                return True
            else:
                socket.client = message
                MyServer.listofclient[message] = socket
                MyServer.connecting[message] = socket
                message = "Type your message"
                message = message.encode()
                socket.send(message)
                return True
        else:
            (command,sep,paramater) = message.strip().partition(' ')
            if(command == "Quit"):
                message = "Quitting the program"
                message = message.encode()
                socket.send(message)
                return False
            elif(command == "SENT_ALL"):
                paramater = "["+socket.client+"] : "+paramater
                message = paramater.encode()
                for user in MyServer.connecting:
                    MyServer.connecting[user].send(message)
                return True
            elif (command == "WHISPER"):
                seperation = []
                for word in paramater.split():
                    seperation.append(word)
                specific_user = seperation[0]
                if(specific_user in MyServer.listofclient):
                    message = ' '.join(seperation[1:])
                    message = "message from "+socket.client +": "+message
                    message = message.encode()
                    MyServer.listofclient[specific_user].send(message)
                else:
                    message = "Wrong Person Try Again"
                    message = message.encode()
                    socket.send(message)
                return True
            elif(command == "CONNECT_ALL"):
                message = ""
                for user in MyServer.listofclient:
                    message += (user + "\n")
                message = message.encode()
                socket.send(message)
                return True
            elif(command.lower() != "message"):
                message = "Invalid Command"
                message = message.encode()
                socket.send(message)
                return True
            else:
                if (paramater == ""):
                    message = "Invalid paramater"
                    message = message.encode()
                    socket.send(message)
                    return True
                else:
                    print("command:", command)
                    print("paramater:",paramater)
                    print("message from",socket.client,": ",paramater)
                    message = paramater.encode()
                    socket.send(message)
                    return True

ip =sys.argv[1]
port = int(sys.argv[2])

server = MyServer()

server.start(ip,port)
