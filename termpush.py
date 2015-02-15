#!/usr/bin/python
import socket
import getopt
import sys #for args parsing.
import subprocess
from thread import *
from sockmanager import *

#this will be called as a thread.  We will ignore this for now.
def listen(csocket, async):
	while 1:
		sockin = csocket.recv(SIZE)
		async.register(sockin)
def usage():
	print "Usage Examples:"
	print "termpush file.in   #To upload file.in"
	print "termpush           #To manually input text"
	print "termpush [-args] some-command [-args for somecommand]"     #To stream output of some-command""

def stripEscape(line):
	if not line.find("\"") == -1:
		line.replace("\"", "")
	return line


#this class is not yet used, but will be able to transfer socket input data into the stream
class Async:

	def __init__(self):
		self.queue = []
	def register(self, sockin):
		queue.append(sockin)
		#nobody cares that this isnt being used.

if __name__=='__main__':
	#Handle arguments FIRST
	argLen = len(sys.argv)
	args = sys.argv
	try:
		opts, args = getopt.getopt(args[1:], 'c:vhpi:f:')
	except getopt.GetoptError as err:
		print str(err)
		usage()
		sys.exit(2)
	#verbose: show output
	#command: the thing will be for executing, not importing
	#help: show help
	#private: don't publish on the recent page
	#in: the file to take in
	inFilePath = None
	streamMode = "DEFAULT"
	verbose = False
	private = False
	cmdarr = []
	for o, a in opts:
		if o=="-v":
			verbose = True
		elif o in ("-h"):
			usage()
			sys.exit()
		elif o in ("-f", "-i"):
			inFilePath = a
			streamMode = "FILE"
		elif o in ("-p"):
			private = True
		elif o in ("-c"):
			print str(sys.argv)
			indx = sys.argv.index("-c")
			cmdarr = sys.argv[indx+1:]
			streamMode = "CMD"
		else:
			assert False, "Unhandles args"
	if len(cmdarr) == 0:
		#there was no command passed, check for file paths.
		if len(sys.argv) > 1:
			print len(sys.argv)
			inFilePath = sys.argv[len(sys.argv)-1]
			try:
				filein = open(inFilePath)
				streamMode = "FILE"
			except:
				print "Couldn't find file " + inFilePath

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
	if streamMode == "DEFAULT":
		#Start reading STDIN to send
		print "Use ^C to terminate."
		while True:
			try:
				stdin = raw_input()
			except:
				print ">> Input terminated by user.  Done."
				sys.exit()
			msg.setID(uid)
			msg.addMessage(stdin)
			msg.addType("NORMAL")
			csock.send(msg.pack())
			msg.wipe()
			#consider letting async handle all message send / receive
			#Strongly consider queueing data for send so that the buffers aren't overloaded.
			#have a look for that progress bar thingy.
	
	elif streamMode == "FILE":
		#if we are just feeding a file
		f = filein.read().splitlines()
	 	for line in f:
	 		if (verbose):
	 			print line
	 		#line = stripEscape(line)
	 		msg.setID(uid)
	 		msg.addMessage(line)
	 		msg.addType("NORMAL")
	 		csock.send(msg.pack())
	 		msg.wipe()
	 	filein.close()

	elif streamMode == "CMD":
		#do the thing with a command instead.
		commandString = ""
		for x in cmdarr:
			commandString += x + " "
		p = subprocess.Popen(commandString, shell=True, stdout=subprocess.PIPE)
		while True:
			try:
				out = p.stdout.readline()
			except:
				print ">> Input terminated by user.  Done."
				sys.exit()
			if out == '' and p.poll() != None:
				break
			if not (out == ""):
				#this is where we do the thing.
				if (verbose):
					print "######## Beginning Execution ########"
					print out
				msg.setID(uid)
	 			msg.addMessage(out)
	 			msg.addType("NORMAL")
	 			csock.send(msg.pack())
	 			msg.wipe()
	
	#Do the thing after we
	csock.close()