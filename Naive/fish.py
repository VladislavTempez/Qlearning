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
	
class Fish:
	def __init__(self,idFish,x,previousKnowledge,learningRate=1,exploreRate=0.0):
		self.idFish = idFish
		self.x = x
		self.learningRate = learningRate
		self.vision = []
		self.valueMap = previousKnowledge
		self.exploreRate = exploreRate
		self.actionList = []
		self.age=0
		self.speed=1
		self.distanceN=[]
		self.lastAction='random'
	def __str__(self):
		return str(self.idFish)
	__repr__=__str__
	def __eq__(self,fish):
		return self.idFish==fish.idFish
	def __ne__(self,fish):
		return self.idFish!=fish.idFish
	def __lt__(self,fish):
		return self.idFish<fish.idFish
	def decide(self,actions):
		unknownActionsList=[]
		knownActions={}
		for a in actions:
			if a in self.valueMap.keys():
				knownActions[a]=self.valueMap[a]
			else:
				unknownActionsList.append(a)
		#converting to a probability
		sumProb=0
		for key,value in knownActions.items():
			sumProb=sumProb+value
		for key,value in knownActions.items():
			knownActions[key]*value*(1-self.exploreRate)*sumProb
		#adding the actions that are still unknown to the list of possible actions.
		n = len(unknownActionsList)
		for a in unknownActionsList:
			knownActions[a]=exploreRate*1/n
		action=randomChoose(knownActions,'random')
#		self.learningRate=self.learningRate*0.9915
		return action
	def distance(self,fish):
		return math.sqrt((self.x-fish.x)**2)
	def updateQ(self,actionList, reward):
		moves={}
		if(actionList==[]):
			print('noActions')
			return 0
		for a in actionList:
			if a in moves.keys():
				moves[a] = moves[a] + 1
			else:
				moves[a] = 1
#		print(moves,actionList)
		sumValues = 0
		for key,value in moves.items():
			sumValues=sumValues+value
		k=sumValues
		for key,value in self.valueMap.items():
			self.valueMap[key]=value*(1-self.learningRate*reward)
		for key,value in moves.items():
			gain=self.learningRate*reward*value/k
			if key in self.valueMap.keys():
				self.valueMap[key]=self.valueMap[key]+gain
			else:
				self.valueMap[key]=gain
		sumProb=0
		for key,value in self.valueMap.items():
			sumProb=sumProb+value
		for key,value in self.valueMap.items():
			valueMap[key]=value*sumProb
#		probaChecker=0
#		for key,value in self.valueMap.items():
#			probaChecker=probaChecker+value
#		if abs(probaChecker - 1) > 0.0000000001 :
#			print(self.valueMap, ' is no longer a probability') 
