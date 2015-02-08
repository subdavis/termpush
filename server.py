import socket
import sys
import string
import random
from thread import *

#This will be created as a new thread for each connected client (web AND client)
def clientthread(conn, man, thisID):
    #Sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
     
    #infinite loop so that function do not terminate and thread do not end.
    while True:
         
        #Receiving from client
        data = conn.recv(1024)
        reply = 'OK...' + data
        if not data: 
            break
        #find the right recipients
        for c in m.getRecip(thisID):
            c.send(reply)
            print "Sent " + reply + " To " + thisID
     
    #Come out of loop
    conn.close()

#obvs for unique IDs    
def idGenerator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class ConManager:
    #This class is for keeping together multiple web connections on the same feed
    # Rememebr what web clients want what data.

    def __init__(self):
        self.webCons = {'000000' : None}
        #Do this once at runtime.
    
    def addWeb(self, uid, conn):
        if uid in self.webCons:
            self.webCons[uid].append(conn)
        else:
            self.webCons[uid] = [conn]
    
    def delWeb(self, uid, conn):
        #assumes at least one connection exists in webCons 
        self.webCons[uid].remove(conn)

    def getRecip(self, uid):
        return self.webCons[uid]

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port
 
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
    
    #check to see what kind of connection

    #do this if recipient.  We will pretend all are recipients for now.
    thisID = idGenerator()
    
    m.addWeb(thisID, conn)

    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn, m, thisID))
 
s.close()