from envND import *
import matplotlib.pyplot
from misc import *
import numpy

baseKnowledge={'toNearestFish': 0.5 ,'fromNearestFish': 0.5}
actions = ['toNearestFish','fromNearestFish']
fishes = []
popSize = 2
sparsity = 30
runDuration = 60
dim = 1
populationKnowledge=baseKnowledge.copy()
success=[]
oldOnes=[]
for j in range (50):
	success.append(0)
	for i in range(popSize):
		fishes.append(Fish(newID(),populationKnowledge.copy(),dim))
	Env1 = Environment(runDuration,fishes,actions)
	placeFishes(dim,sparsity,Env1.fishList)
	for i in range(100):
		placeFishes(dim,sparsity,Env1.fishList)
		survivors, newPopulationKnowledge = Env1.run()
		for s in survivors:
			s.age = s.age + 1
#			s.learningRate=s.learningRate+(1-s.learningRate)*(s.age-1)/s.age
#			s.speed=s.speed+1
			if s.age > 5:
				if s in oldOnes:
					oldOnes.remove(s)
				oldOnes.append(s)
		sLen = len(survivors)
		if sLen > 0:
			success[j]=success[j] + 1
			populationKnowledge=newPopulationKnowledge.copy()
#			print(populationKnowledge)			
		for i in range(popSize-sLen):
			survivors.append(Fish(newID(),populationKnowledge.copy(),dim))
		Env1.date = 0
		Env1.fishList = survivors
#		print(Env1.fishList)
left=[i for i in range(len(success))]
matplotlib.pyplot.bar(left,height=success)
matplotlib.pyplot.ylabel('number of success')
title='Population : ' + str(popSize)
title=title + '; dimension : ' + str(dim)
title=title + '; sparsity : ' + str(sparsity)
title=title + '; run duration : ' + str(runDuration)
title=title + '; criticalDistance : ' + str(Env1.criticalDistance)
#title=title+' with active learning'
matplotlib.pyplot.title(title)
matplotlib.pyplot.savefig('./'+title)
matplotlib.pyplot.show()
#testFish=Fish(newID(),populationKnowledge.copy(),2,[0,0])
#testFish2=Fish(newID(),populationKnowledge.copy(),2,[sparsity * 1,sparsity * 1])
#testFish.vision=[testFish2]
#testFish2.vision=[testFish]
#print(testFish.pos,testFish2.pos)
#print(testFish.valueMap)
#for i in range(10):
#	testFish.act(actions)
#	print(testFish.pos,testFish2.pos)
#	testFish2.act(actions)
#	print(testFish.pos,testFish2.pos)
#testFish2.pos=[-5,-5]
#print(testFish.pos,testFish2.pos)
#for i in range(10):
#	testFish.act(actions)
#	print(testFish.pos,testFish2.pos)
#	testFish2.act(actions)
#	print(testFish.pos,testFish2.pos)
#for s in oldOnes:
#	print('id :', s.idFish,'age :', s.age)
#	print(sorted( ((v,k) for k,v in s.valueMap.items()), reverse=True))
#	print(s.valueMap)
#	
