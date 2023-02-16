import time
import im

server = im.IMServerProxy('http://web.cs.manchester.ac.uk/r13355ty/comp28112_ex1/IMserver.php')
i = 0
numberOfSeconds = 30

def typmessage(userrole):
    myMessage = input("Type your message: ")
    #Quit the program if type exit
    if (myMessage == 'Exit' or myMessage == 'exit'):
        print('Quitting program...')
        # del server[userrole]
        server.clear()
        exit()
    # if server cleared because of not answering 30 second, quitting the program
    elif (len(server.keys()) ==1):
        print("No answer from You")
        print("Quitting the program... ")
        exit()
    else:
        #set message in userrole and sent_message
        server[userrole] = myMessage.encode("utf-8")
        server['sent_message'] = userrole.encode("utf-8")


def waitingforinput(userrole,otheruser):
    while True:
        #other user set as sent_message, type message
        if(server['sent_message'].decode("utf-8").strip() == otheruser):
            print("please enter your message for ",numberOfSeconds,"seconds")
            myMessage = typmessage(userrole)
            break


def waitingforoutput(userrole, otheruser):
    counter =0
    while True:
        #checking time for other user typing for 30 seconds
        if(counter == numberOfSeconds):
            print("No answer from other user")
            print("Quitting the program")
            server.clear()
            exit()
        #Quitting the prgram if sever cleared
        if (len(server.keys()) ==1):
            print("Quitting the program... ")
            exit()
        #showing the message other user sent
        elif(server['sent_message'].decode("utf-8").strip() == otheruser):
            print(server[otheruser])
            break
        else:
            counter +=1
            time.sleep(1)
try:
    #clear server if there's existing keys
    key = server.keys()
    if(len(key)!=1):
        server.clear()

    #get user role
    userrole = input('Type your role: ')
    print("joining session as",userrole)
    userrole =  userrole + str(i)
    #differencing first user and second user
    if (server[userrole].decode("utf-8").strip() == userrole):
        i+=1
        userrole = userrole[:-1] +str(i)
        server[userrole] = userrole.encode("utf-8")
    else:
        server[userrole] = userrole

    #waiting another user to come in
    key = server.keys()
    while (len(key) < 3):
        key = server.keys()

    #set up first user and other user
    for i in key:
        if (i.decode("utf-8").strip() != userrole and i.decode("utf-8").strip() != ""):
            otheruser = i.decode("utf-8").strip()
    #making first user can type
    server['sent_message'] = key[1]
    while True:
        try:
            waitingforinput(userrole,otheruser)
            waitingforoutput(userrole,otheruser)
        except Exception as e:
            print("exiting program")
            print(traceback.format_exc())
            server.clear()
            exit()
except Exception as e:
    print("exiting")
    print(traceback.format_exc())
    server.clear()
    exit()
