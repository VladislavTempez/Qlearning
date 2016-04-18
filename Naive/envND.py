import math
import random
from fishND import *
random.seed()

class Environment:
	def __init__(self,duration,fishes,actions,criticalDistance = 4, criticalSize = 1):
		self.fishList = fishes #list of involved fishes
		self.duration = duration #number of movement steps before evaluation
		self.date = 0 #current step
		self.criticalDistance = criticalDistance #size below (or equal) which fishes are considered safe
		self.criticalSize = criticalSize #size above (or equal) which a group is considered large enough to be safe
		self.actions=actions #list of possible actions for this run
	
	def update(self,stepNumber): #runs 'stepNumber' steps of the run
		for i in range(0,stepNumber):
			if self.date > self.duration:
				print('experiment ran too long')
				break

			for fish in self.fishList:
				fish.act(self.actions)			
			for fish1 in self.fishList:
				for fish2 in self.fishList:
					if fish2!=fish1:
						fish1.updateDistanceDistribution(self.date,fish2)
			
			for fish1 in self.fishList:
				if fish.effrayedOfLoneliness: #check if fish1 is punished from being alone
					nearestNeighbourDistance=min(fish1.distance(fish2) for fish2 in fish1.vision)
					if nearestNeighbourDistance >= 2*self.criticalDistance:
						fish1.updateQ([fish1.lastAction],-1)
			self.date = self.date + 1
			
	def run(self):
		for fish in self.fishList:
			fish.vision = self.fishList.copy()
			fish.vision.remove(fish)
		self.update(self.duration)
		survivors=[]
		#check if reward
		for fish1 in self.fishList:
			neighbour = 0
			for fish2 in self.fishList:
				if fish2 != fish1 :
#					print('distances',fish1.distance(fish2),fish2.distance(fish1),'pos', fish1.pos,fish2.pos)
					if fish1.distance(fish2) <= self.criticalDistance:
						neighbour = neighbour + 1
			if (neighbour >= self.criticalSize):			
				fish1.updateQ(fish1.actionList,1)
				survivors.append(fish1)
		populationKnowledge={} #average knowledge of population
		for fish in survivors:
			for key,value in fish.valueMap.items():
				if key in populationKnowledge.keys():
					populationKnowledge[key] = populationKnowledge[key] + value
				else:
					populationKnowledge[key] = value
		sumValues = sum(values for (key,values) in populationKnowledge.items())
		for key,value in populationKnowledge.items():
			populationKnowledge[key] = value/sumValues
		return survivors,populationKnowledge

