import socket
import sys
import json
import string
import random
from thread import *
#These are my custom-written helper classes.
from tputils.database import *
from tputils.sockmanager import *
#thanks to https://github.com/opiate/SimpleWebSocketServer
from websocket.SimpleWebSocketServer import *

#This will be created as a new thread for TERM clients
def termthread(sockhandler, thisID):
    #infinite loop so that function do not terminate and thread do not end.
    while True:
        #Receiving from client
        message = sockhandler.rcvNext()
        if not (message == "\0"):
            print message.getLine()
            #find the right recipients with sockhandler
            if not (global_connection_manager.getWeb(thisID) == None):
                for c in global_connection_manager.getWeb(thisID):
                    c.sendMessage(message.getRaw())
            global_db.insertLine(message.getRaw())
        else: break
     
    #Come out of loop
    sockhandler.close() #tell the handler to close the connection
    del sockhandler # remove the handler
    global_connection_manager.delTerm(thisID)
    print thisID + " closed the connection"

#obvs for unique IDs    
def idGenerator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class ConManager:
    #This class is for keeping association between client sockets and websockets
    #Rememebr what web clients want what data.
    #kept as a global variable for now.  No harm :)

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
        #else why the hell would we be removing it?
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

def startTCP():
    #do sock creation
    HOST = ''   # Symbolic name meaning all available interfaces
    PORT = 8888 # Arbitrary non-privileged port
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
        sockhandler = SocketHandler(conn)
        greeting = sockhandler.rcvNext() #returns message OBJECT. 
        #sockhandlerould throw an error we can catch here leter

        #temporary error checking.
        if type(greeting) == type(" "): 
            #if client isn't formatting messages properly.
            print "Bad Greeting Formatting: Not JSON"
            conn.close()
            continue

        if greeting.getType() == "NEWTERM":
            thisID = idGenerator()
            reply = MsgGen(True)
            reply.newTermReply(thisID)
            reply = reply.pack()
            conn.send(reply)
            global_connection_manager.addTerm(thisID, conn)
            global_db.addID(thisID)
            start_new_thread(termthread ,(sockhandler, thisID))
        else:
            print "Bad Geeting: JSON with incorrect fields"

    s.close()

class WSServer(WebSocket):

    def handleMessage(self):
        if self.data is None:
            self.data = ''

        message = Message(self.data, False)
        self.uid = message.getID()
        self.type = message.getType()
        
        if self.type == "NEWWEB":
            global_connection_manager.addWeb(self.uid , self)
            print "Web connection named " + self.uid + " auth succeded!"
        
            #Now let's send it everything we've ever received for this ID.
            query = global_db.getHistory(self.uid)

            for entry in query:
            	#have to get a JSON object from whatever the fuck mongo delivers.
            	toJSON = json.dumps(entry)
                self.sendMessage(str(toJSON))
        

    def handleConnected(self):
        print "Web Connection from " , self.address

    def handleClose(self):
        global_connection_manager.delWeb(self.uid, self)
        print self.address, 'closed'

#===============================================================
#               Begin the main program
#===============================================================
if __name__=="__main__":

    global global_connection_manager
    global global_db
    
    global_connection_manager = ConManager() #this will store and fetch active connections based on a unique ID
    global_db = Database() #Make mongo transparent.  No Mongo calls in this file.  Dont be sloppy....

    #start the normal sock thread
    start_new_thread(startTCP, ())
    #Start WS server
    ws = SimpleWebSocketServer("", 8000, WSServer)
    try:
        ws.serveforever()
    except:
        print "Terminated!"