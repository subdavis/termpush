import socket
import sys
import string
import random
import json
from thread import *
#These are my custom-written helper classes.
from messagemanager import *
from database import Database

#This will be created as a new thread for TERM clients
def termthread(sh, man, thisID, db):
    #infinite loop so that function do not terminate and thread do not end.
    while True:
        #Receiving from client
        message = sh.rcvNext()

        #find the right recipients
        if not (man.getWeb(thisID) == None):
            for c in man.getWeb(thisID):
                c.send(message)

        db.insertLine(message)
     
    #Come out of loop
    sh.close() # tell the handler to close the connection
    del sh # remove the handler
    man.delTerm(thisID)
    print thisID + " closed the connection"

#This will be created as a new thread for WEB clients
def webthread(SockHandler, man, thisID, db):
    #don't even call this yet.  It isn't ready
    print "don't use me"

#obvs for unique IDs    
def idGenerator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class ConManager:
    #This class is for keeping together multiple web connections on the same feed
    #Rememebr what web clients want what data.
    #maybe make this singleton later?  I'll only ever have one, then I wont have to pass the fucker around as an arg.

    def __init__(self):
        self.webCons = {'000000' : None}
        self.termCons = {'000000' : None}
        #Do this once at runtime.
    
    def addWeb(self, uid, conn):
        if uid in self.webCons:
            self.webCons[uid].append(conn)
        else:
            self.webCons[uid] = [conn]
    
    def delWeb(self, uid, conn):
        #assumes at least one connection exists in webCons 
        self.webCons[uid].remove(conn)

    def getWeb(self, uid):
        if uid in self.webCons:
            return self.webCons[uid]
        else: return None

    def addTerm(self, uid, conn):
        self.termCons[uid] = conn

    def delTerm(self, uid):
        del self.termCons[uid]

    def getTerm(self, uid):
        if uid in self.termCons:
            return self.termCons[uid]
        else: return None

#Receive whole messages instead 
#This should be a CLASS, and each connection should get their OWN.
#Functions so that each class can rememeber the conn and buffer without needing to include as an ARG
#Relies on a protocol that sends '\n' at the end of each message.
class SocketHandler:

    def __inti__(self, conn):
        self.conn = conn
        self.buff = ""

    def rcvNext(self):
        #While the buffer does not contain a newline string, keep asking for new data.
        while (self.buff.index('\n') == -1):
            #this will be where each thread should hang and wait for data
            data = self.conn.recv()
            if not data:
                #called if connection closes.
                return ""
            self.buff += data
        end = self.buff.index('\n')
        message = self.buff[:end]
        self.buff = self.buff[end:]
        return message
    def close(self):
        self.conn.close()

#===============================================================
#               Begin the main program
#===============================================================

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
m = ConManager() #this will store and fetch active connections based on a unique ID
db = Database() #Make mongo transparent.  No Mongo calls in this file.  Dont be sloppy....

print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'

#Start listening on socket
s.listen(10)
print 'Socket now listening on ' + str(PORT)

#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    
    #check to see what kind of connection.
    #rewritten to use the new SockHandler Class and protocol
    sh = SockHandler(conn)
    greeting = sh.rcvNext() #will crash if no newline char is ever sent.  Fix that.
    
    #Test that the client is correctly formatting messages.
    try:
        greeting = Message(greeting) #must be a JSON string
        greeting.getType() #must have a type feild.
    except:
        conn.close()
        print "Closed connection: " + addr[0] + " Bad formatting."
        continue

    if greeting.getType() == "NEWTERM":
        thisID = idGenerator()
        reply = MsgGen()
        reply.newTermReply(thisID)
        reply = reply.pack()
        conn.send(reply)
        m.addTerm(thisID, conn)
        db.addID(thisID)
        start_new_thread(termthread ,(sh, m, thisID, db))
    elif greeting.getType() == "NEWWEB":
        thisID = greeting.getID()
        start_new_thread(webthread ,(sh, m, thisID, db))
    else:
        print "Client NOT speaking my protocol."
 
s.close()