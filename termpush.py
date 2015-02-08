import socket
import json
import time
from thread import *

#===============================================================
#				Setup variables and start the connection
#===============================================================

HOST = 'localhost'
PORT = 8888
SIZE = 1024 # the size in bytes to accept from the server.
#connect to the sock server.
csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
csock.connect(HOST, PORT)
#in the event we want to listen to socket input asynchranously.  
async = Async()
#this will be recycled for each line of input.  Dont waste memory!
msg = MsgGen()

#===============================================================
#				Begin actually doing things
#===============================================================

#let's write a message to introduce ourselves.
firstMessage = MsgGen()
firstMessage.addType("NEW") 
csock.send(firstMessage.pack())
#expected that server waits for connection to be NEW and then replies with a UID
greeting = csock.recv(SIZE)
#parse the greeting and tell MsgGen what the ID we should use is.
#idea: have the server also generate a passkey to keep spammers from spamming randomly generated IDS.
#---------left off here

msg.wipe()

#Start reading STDIN to send
while 1:
	stdin = raw_input()
	msg.addMessage(stdin)
	csock.send(msg.pack())

#this will be called as a thread.  We will ignore this for now.
def listen(csocket, async):
	while 1:
		sockin = csocket.recv(SIZE)
		async.register(sockin)

#this class will create new messages.
class MsgGen:
	def __init__(self):
		self.data = {}
	def addType(self, mtype):
		#Type is either NEW, NORMAL, or REQ
		self.data['type'] = mtype
	def setID(self, UID):
		self.id = UID
	def addMessage(self, message):
		self.data['message'] = message
		self.data['time'] = int(time.time())
		self.data['uid'] = self.id
		self.setID("NORMAL")
	def pack(self):
		return json.dumps(self.data)
	def wipe(self):
		self.data = {}

#this class is not yet used, but will be able to transfer socket input data into the stream
class Async:

	def __init__(self):
		self.queue = []
	def register(self, datain):
		queue.append(datain)
		#nobody cares that this isnt being used.
