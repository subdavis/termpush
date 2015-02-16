from pymongo import MongoClient
import json
class Database:

	def __init__(self):
		#Lazy shit until I write proper location determination
		self.col = "AAAA"
		PORT = 27017
		HOST = 'localhost'
		self.client = MongoClient(HOST, PORT)
		self.db = self.client.termdev
		print "Connected to DB successfully on port " + str(PORT)
	def addID(self, uid):
		newID = {"uid" : uid , "location" : self.col }
		retrn = self.db.ids.insert(newID)
		print "Created new ID " + uid
	def insertLine(self, line):
		retrn = self.db[self.col].insert(json.loads(line))