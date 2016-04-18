import math
import random
random.seed()

def randomChoose(dictionary,default): #choose randomly a key in a dictionnary whose value are probability to chose the keys	
	x=random.random()
	stack=0
	for key,value in dictionary.items():
		stack = stack + value
		if stack > x:
			return key
	print(default,x,dictionary)
	return default
	
def normalize(dictionary): #linear transformation that makes the dictionary a probability distribution only take distribution with positive values
	sumValues=sum(value for key,value in dictionary.items())
	for key,value in dictionary.items():
		dictionary[key]=value/sumValues	

class Fish:
	def __init__(self,idFish,previousKnowledge,dim=1,pos=[],learningRate=0.6,exploreRate=0.0):
		self.idFish = idFish
		if pos==[]:
			self.pos=[0 for i in range(dim)]
		else :
			self.pos = pos
		self.dim = dim
		self.learningRate = learningRate
		self.vision = []
		self.exploreRate = exploreRate
		self.actionList = []
		self.age = 0
		self.speed = 1
		self.actions = {}
		self.lastAction = None
		self.effrayedOfLoneliness = False
		self.distanceDistribution = {}
		self.valueMap=previousKnowledge
		def randomMove(self):
			moveDir = random.randint(0,self.dim - 1)
			self.pos[moveDir] = self.pos[moveDir] + 2 * random.randint(0,1) - 1
		def increaseDim(self,i):
			self.pos[i] = self.pos[i] + 1

		def decreaseDim(self,i):
			self.pos[i] = self.pos[i] - 1

		def toNearestFish(self):
		#finding nearest fish
			try : 
				n = len(self.pos)
				aim = [0 for i in range(n)]
				for fish in self.vision:
					for i in range(n):
						aim[i] = aim[i] + fish.pos[i]
				k=len(self.vision)
				for i in range(n):
					aim[i] = aim[i] / k
			except ValueError:
				aim = self.pos
		#moving to reduce distance : find the first dimension in which position differs and reduce this difference.
			randDim=[i for i in range(dim)]
			random.shuffle(randDim)
			for i in randDim:
				if self.pos[i] > aim[i]:
					self.pos[i] = self.pos[i] - 1
					break
				elif self.pos[i] < aim[i]:
					self.pos[i] = self.pos[i] + 1
					break
				else:
					continue
	
		def fromNearestFish(self):
		#finding nearest fish
			try : 
				n = len(self.pos)
				aim = [0 for i in range(n)]
				for fish in self.vision:
					for i in range(n):
						aim[i] = aim[i] + fish.pos[i]
				k = len(self.vision)
				for i in range(n):
					aim[i] = aim[i] / k
			except ValueError:
				aim=self.pos
		#moving to increase distance : find the dimension in which position are the closer and increase this difference.
			minDiff,dimMinDiff = min((abs(self.pos[i] - aim[i]),i) for i in range(dim))
			if self.pos[dimMinDiff] > aim[dimMinDiff]:
				self.pos[dimMinDiff]=self.pos[dimMinDiff]+1
			else:
				self.pos[dimMinDiff]=self.pos[dimMinDiff]-1


		self.actions['random']=randomMove
		self.actions['toNearestFish']=toNearestFish
		self.actions['fromNearestFish']=fromNearestFish
		for i in range(dim):
			self.actions['increaseDim'+str(i)] = lambda x: increaseDim(x,i)
			self.actions['decreaseDim'+str(i)] = lambda x: decreaseDim(x,i)
		k=len(self.actions.keys())
#		for key in self.actions.keys():
#			self.valueMap[key]=1/k
	def __str__(self):
		return str(self.idFish)
	__repr__=__str__
	def __eq__(self,fish):
		return self.idFish == fish.idFish
	def __ne__(self,fish):
		return self.idFish != fish.idFish
	def __lt__(self,fish):
		return self.idFish < fish.idFish
	def decide(self,actions):
		unknownActionsList = []
		knownActions={}
		for a in actions:
			if a in self.valueMap.keys():
				knownActions[a] = self.valueMap[a]
			else:
				unknownActionsList.append(a)
		normalize(knownActions)
		
		for key,value in knownActions.items():
			knownActions[key]=value*(1-self.exploreRate)
		#adding the actions that are still unknown to the list of possible actions.
		n = len(unknownActionsList)
		for a in unknownActionsList:
			knownActions[a]=self.exploreRate*1/n
		action=randomChoose(knownActions,'random')
		return action
	def distance(self,fish):
		d=0
		for i in range(len(self.pos)):
			d=d+(self.pos[i]-fish.pos[i])**2
		d=d**(1/2)
		return d
	def act(self,possibleActions):
		action=self.decide(possibleActions)
		self.lastAction=action
		self.actionList.append(action)
		self.actions[action](self)
	def updateQ(self,actionList, reward):
		moves={}
		if(actionList==[]):
			print('noActions')
			return
		for a in actionList:
			if a in moves.keys():
				moves[a] = moves[a] + 1
			else:
				moves[a] = 1
		sumValues = 0
		for key,value in moves.items():
			sumValues=sumValues+value
		for key,value in moves.items():
			gain=self.learningRate*reward*value/sumValues
			if key in self.valueMap.keys():
				self.valueMap[key]=max(self.valueMap[key]+gain,0)
			else:
				self.valueMap[key]=max(gain,0)
		normalize(self.valueMap)
	def updateDistanceDistribution(self,date,fish):
		if fish.idFish in self.distanceDistribution.keys():
			self.distanceDistribution[fish.idFish][date]=self.distance(fish)
		else:
			self.distanceDistribution[fish.idFish]={date : self.distance(fish)}
