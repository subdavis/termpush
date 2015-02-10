from pymongo import MongoClient

class Database:

	def __init__(self):
		#Lazy shit until I write proper location determination
		self.col = "0000"
		PORT = 27017
		HOST = 'localhost'
		self.client = MongoClient(HOST, PORT)
		self.db = self.client.termdev
		#This will rememeber where I left off creating new line documents
		self.meta = self.db.meta
		#this will remember the collection I stored a particular ID in
		self.ids = self.db.ids
		#id will determine the collection it's messages will be in
		self.col = self.db[self.col]
		print "Connected to DB successfully on port " + str(PORT)
	def addID(self, uid):
		newID = {"uid" : uid , "location" : self.col }
		retrn = self.db.ids.insert(newID)
		print "Created new ID " + uid
	def insertLine(self, line):
		retrn = self.db[self.col].insert(line)