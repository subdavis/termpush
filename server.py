import socket
import sys
import string
import random
import json
from thread import *
from messagemanager import *

#This will be created as a new thread for TERM clients
def termthread(conn, man, thisID):
    #this is where we do JSON PARSING for the welcome message
     
    #infinite loop so that function do not terminate and thread do not end.
    while True:
         
        #Receiving from client
        data = conn.recv(1024)
        dataString = data + ""
        #Do JSON parsing with the Message class
        
        if not data: #find out how this works.
            break
        #find the right recipients
        if not (m.getWeb(thisID) == None):
            for c in m.getWeb(thisID):
                c.send(dataString)
        
        print "Sent " + dataString + " To " + thisID
     
    #Come out of loo
    conn.close()
    m.delTerm(thisID)
    print thisID + " closed the connection"

#This will be created as a new thread for WEB clients
def webthread(conn, man, thisID):
    SIZE = 1024

    #this is where we do JSON PARSING for the welcome message
     
    #infinite loop so that function do not terminate and thread do not end.
    while True:
         
        #Receiving from client
        data = conn.recv(SIZE)
        #Do JSON parsing with the Message class
        
        if not data: #find out how this works.
            break
        #find the right recipients
        for c in m.getTerm(thisID):
            c.send(sendString)
        print "Sent " + sendString + " To " + thisID
     
    #Come out of loop
    conn.close()
    m.delWeb(thisID)
    print thisID + " closed the connection"

#obvs for unique IDs    
def idGenerator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class ConManager:
    #This class is for keeping together multiple web connections on the same feed
    # Rememebr what web clients want what data.
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
#===============================================================
#               Begin the main program
#===============================================================

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8886 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
m = ConManager() #this will store and fetch active connections based on a unique ID
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
print 'Socket now listening'
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    
    #check to see what kind of connection.
    greeting = conn.recv(1024)
    greeting = Message(greeting)

    if greeting.getType() == "NEWTERM":
        thisID = idGenerator()
        reply = MsgGen()
        reply.newTermReply(thisID)
        reply = reply.pack()
        conn.send(reply)
        m.addTerm(thisID, conn)
        start_new_thread(termthread ,(conn, m, thisID))
    elif greeting.getType() == "NEWWEB":
        thisID = greeting.getID()
        start_new_thread(webthread ,(conn, m, thisID))
    else:
        print "What the fuck is even trying to talk to me??"
 
s.close()