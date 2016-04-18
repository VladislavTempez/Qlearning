import math
import random
from fish import *
#from fish2D import*
random.seed()



class Environment:
	def __init__(self,duration,fishes,actions,criticalDistance = 4, criticalSize = 1):
		self.fishList = fishes
		self.duration = duration
		self.date = 0
		self.fishPosition = []
		self.criticalDistance = criticalDistance
		self.criticalSize = criticalSize
		for fish in self.fishList:
			self.fishPosition.append(fish.x)
		self.actions=actions
	def act(self,action,fish):
		try : 
			nearestFish=min((fish.distance(neighbour),neighbour) for neighbour in fish.vision if neighbour != fish)[1]
			assert(nearestFish!=fish)
		except ValueError:
			nearestFish=fish
		if(action=='left'): #going to the left
			fish.x = fish.x - 1*fish.speed
			fish.actionList.append(action)
		elif(action=='right'): #going to the left
			fish.x = fish.x + 1*fish.speed
			fish.actionList.append(action)
		elif(action=='toNearestFish'): #going toward nearest fish in vision
			if(nearestFish == fish): #random behaviour
				print('no neighbour')
				print(fish.vision)
				self.act('random',fish)		
						
			else:
				if nearestFish.x > fish.x :
					fish.x = fish.x + 1*fish.speed
					fish.actionList.append(action)
				else:
					fish.x = fish.x - 1*fish.speed
					fish.actionList.append(action)
		elif(action=='fromNearestFish'): #going away from nearest fish in vision
			if(nearestFish == fish): #random behaviour
				print('no neighbour')
				print(fish.vision)
				self.act('random',fish)				
			else:
				if nearestFish.x > fish.x:
					fish.x = fish.x - 1*fish.speed
					fish.actionList.append(action)
				else:
					fish.x = fish.x + 1*fish.speed
					fish.actionList.append(action)

		else: #random behaviour
#			print('random action !')
			direction=random.randint(0,1)
			if(direction == 0):
				fish.x = fish.x + 1*fish.speed
			else:
				fish.x = fish.x - 1*fish.speed
			
	def update(self,stepNumber):
		for i in range(0,stepNumber):
			for fish in self.fishList:
				fish.vision = self.fishList
			if self.date > self.duration:
				print('experiment ran too long')
				break
			self.fishPosition.clear()
			for fish in self.fishList:
				for fish2 in self.fishList:
					if fish2!=fish:
						fish.distanceN.append(fish.distance(fish2))
			for fish in self.fishList:
				action=fish.decide(self.actions)
				self.lastAction=action
				self.act(action,fish)
				self.fishPosition.append(fish.x)
			for fish in self.fishList:
				for fish2 in self.fishList:
					if fish.distance(fish2) > 2*self.criticalDistance:
						fish.updateQ([fish.lastAction],-1)
				#print(fish.idFish,fish.x)
			self.date = self.date + 1
		#print(self.date)
			
	def run(self):
		self.update(self.duration)
		survivors=[]
		#check if reward
		for fish1 in self.fishList:
			neighbour = 0
			for fish2 in self.fishList:
				if fish1.distance(fish2) < self.criticalDistance:
					neighbour = neighbour + 1
			if neighbour > self.criticalSize:			
				fish1.updateQ(fish1.actionList,1)
				survivors.append(fish1)
		return survivors

def randomChoose(dictionary,default): #choose randomly a key in a dictionnary whose value are probability to chose the keys	
	x=random.random()
	stack=0
	for key,value in dictionary.items():
		stack = stack + value
		if stack > x:
			return key
	print(default,x,dictionary)
	return default

