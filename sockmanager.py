import json
import time
#this class will handle message formatting, making the JSON transparent for the sending method.
class MsgGen:
	#Message must be sent with a TYPE, ID and MESSAGE for simplicity
	def __init__(self):
		self.data = {}
	def addType(self, mtype):
		#Type is either NEWTERM, NEWWEB, NORMAL, ACKNEW, REQ
		self.data['type'] = mtype
	def setID(self, UID):
		self.id = UID
	def addMessage(self, message):
		#must have set an ID to call message function
		self.data['message'] = message
		self.data['time'] = int(time.time())
		self.data['uid'] = self.id
	def pack(self):
		return json.dumps(self.data) + '\n'
	def wipe(self):
		self.data = {}
	def newTerm(self):
		self.setID("NULL")
		self.addType("NEWTERM")
		self.addMessage("NULL")
	def newTermReply(self, uid):
		self.setID(uid)
		self.addType("ACKNEW")
		self.addMessage("NULL")

#this will do JSON parsing and packing for messages.
#Mainly this will safely throw an error if a message is unsanitary.
#Add proper error handling later so that clients can be kicked for sending bad messages.
class Message:
    def __init__(self, rawMessage):
        #set each element of the message to a dictionary using the parsed JSON\
        self.raw = rawMessage[:(len(rawMessage)-1)]
        try:
            self.messageDict = json.loads(self.raw)
        except:
            print "bad formatting."
    def getType(self):
        return self.messageDict["type"]
    def getLine(self):
        return self.messageDict["message"]
    def getID(self):
        return self.messageDict["uid"]
    def getRaw(self):
    	return self.raw

#Receive whole messages instead 
#This should be a CLASS, and each connection should get their OWN.
#Functions so that each class can rememeber the conn and buffer without needing to include as an ARG
#Relies on a protocol that sends '\n' at the end of each message.
class SocketHandler:

    def __init__(self, conn):
        self.conn = conn
        self.buff = ""

    def rcvNext(self):
        #While the buffer does not contain a newline string, keep asking for new data.
        while (self.buff.find('\n') == -1):
            #this will be where each thread should hang and wait for data
            data = self.conn.recv(1024)
            print data 
            if not data:
                #called if connection closes.
                return "\0"
            self.buff += data
        end = self.buff.find('\n')
        message = self.buff[:end+1] #include the breaking character so that message handles it.
        self.buff = self.buff[end+1:]
        return Message(message)

    def close(self):
        self.conn.close()

    def getConn(self):
        return self.conn