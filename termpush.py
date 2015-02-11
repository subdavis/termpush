import socket
import sys #for args parsing.
from thread import *
from sockmanager import *

#this will be called as a thread.  We will ignore this for now.
def listen(csocket, async):
	while 1:
		sockin = csocket.recv(SIZE)
		async.register(sockin)

#this class is not yet used, but will be able to transfer socket input data into the stream
class Async:

	def __init__(self):
		self.queue = []
	def register(self, sockin):
		queue.append(sockin)
		#nobody cares that this isnt being used.

if __name__=='__main__':

	#===============================================================
	#				Setup variables and start the connection
	#===============================================================
	HOST = 'ocean.redspin.net'
	PORT = 8888
	SIZE = 1024 # the size in bytes to accept from the server.
	#connect to the sock server.
	csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	csock.connect((HOST, PORT))
	#in the event we want to listen to socket input asynchranously.  
	#async = Async()
	#this will be recycled for each line of input.  Dont waste memory!
	msg = MsgGen()
	sh = SocketHandler(csock)

	#===============================================================
	#				Begin actually doing things
	#===============================================================

	#let's write a message to introduce ourselves to the server.
	firstMessage = MsgGen()
	firstMessage.newTerm()
	firstMessage = firstMessage.pack()
	csock.send(firstMessage)

	#expected that server waits for connection to be NEW and then replies with a UID
	greeting = sh.rcvNext()

	#Thought: how do we keep poeple from spamming connection requests?
	uid = greeting.getID()
	print "View your output at http://termpush.com/" + uid

	msg.wipe()
	#Start reading STDIN to send
	while True:
		stdin = raw_input()
		msg.setID(uid)
		msg.addMessage(stdin)
		msg.addType("NORMAL")
		csock.send(msg.pack())
		msg.wipe()
		#consider letting async handle all message send / receive
		#Strongly consider queueing data for send so that the buffers aren't overloaded.
		#have a look for that progress bar thingy.
