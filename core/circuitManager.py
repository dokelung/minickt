from circuit import *

class CircuitManager(object):

	def __init__(self):
		self.ckts = []
		self.token = 0

	def getToken(self):
		return self.token

	def transToCkt(self,index):
		self.token = index

	def getCurrentCkt(self):
		return self.ckts[self.token]

	def addCkt(self,ckt):
		self.ckts.append(ckt)

	def rmCktByIndex(self,index):
		self.ckts.pop(index)
		if self.token < index:
			pass
		else:
			self.token -= 1

	def getCkts(self):
		return self.ckts

	def getCkt(self,index):
		return self.ckts[index]

	def changeCktName(self,name):
		self.ckts[self.token].setName(name)