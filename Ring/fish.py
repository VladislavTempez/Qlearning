import math
import random

fishId=0
def newID():
	global fishId
	newId=fishId
	fishId = fishId + 1
	return newId
random.seed()
class Fish:
	def __init__(self,idFish,ringSize,vision,previousKnowledge={},pos = 0,learningRate = 1,exploreRate = 0.0):
		self.idFish = idFish
		self.Q = previousKnowledge
		self.pos = pos
		self.posHistory=[]
		self.stateHistory=[]
		self.vision=vision
		self.learningRate = learningRate
		self.exploreRate = exploreRate
		self.eligibilityTrace = []
		self.age = 0
		self.speed = 1
		self.lastAction= None
		self.states=[]
		def goLeft(self):
			self.pos = (self.pos - 1)% ringSize
			self.lastAction='left'
			self.eligibilityTrace.append('left')
			self.posHistory.append(self.pos)
			self.stateHistory.append(self.getState())
		def goRight(self):
			self.pos = (self.pos + 1)% ringSize
			self.lastAction='right'
			self.eligibilityTrace.append(('right',1))
			for (a,v) in self.eligibilityTrace:
				
			self.posHistory.append(self.pos)
			self.stateHistory.append(self.getState())
		self.actions=['left' : goLeft,'right' : goRight]
	def distance(self,fish):
		return min((self.pos - fish. pos) % n ,(fish.pos - self. pos) % n)
	def getState(self):
		near = 0
		left = 0
		right = 0
		for fish in self.vision:
			if self.distance(fish) <= 2:
				near = near + 1
			elif fish.pos - self.pos > ringSize / 2 :
				left = left + 1
			else :
				right = right + 1
		return (near,left,right)
	def decide(self):
		s=self.getState
		r=random.random()
		if r > exploreRate :
			return random.choice(['left','right'])
		else :
			if s in self.Q.keys():
				return max((value,key) for key,value in self.Q.items())[1]
			else :
				return random.choice(['left','right'])
		
	
	def __str__(self):
		return str(self.idFish)
	def __repr__(self):
		return str(self.idFish)
	def __eq__(self,fish):
		return self.idFish==fish.idFish
	def __ne__(self,fish):
		return self.idFish!=fish.idFish
	def __lt__(self,fish):
		return self.idFish<fish.idFish
