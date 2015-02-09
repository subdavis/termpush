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
		self.data['message'] = message
		self.data['time'] = int(time.time())
	def pack(self):
		return json.dumps(self.data) + "\n"
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

class Message:
    #this will do JSON parsing and packing for messages.
    def __init__(self, rawMessage):
        #set each element of the message to a dictionary using the parsed JSON
        self.messageDict = json.loads(rawMessage)
    def getType(self):
        return self.messageDict["type"]
    def getLine(self):
        return self.messageDict["message"]
    def getID(self):
        return self.messageDict["uid"]