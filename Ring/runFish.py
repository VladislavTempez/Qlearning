from fish import *
import matplotlib.pyplot as plt
popSize = 5
runDuration = 10000
ringSize = 43 
reward=1000
punition=-2
previousKnowledge={}
modifyExploRate=True
exploRateDecrease = 0.995
def rewards(state):
    near,left,right = state
    if near >= 3:
        return reward
    elif near < 2:
        return punition
    else :
        return 0

def printHistory(pop):
    globalHistory=[]
    emptyBoard={}
    for i in range(ringSize):
        emptyBoard['Pos'+str(i)]=[]
    for i in range(runDuration):
        globalHistory.append(emptyBoard.copy())
    for fish in pop:
        print(len(fish.posHistory))
        for i in range(len(fish.posHistory)):
            globalHistory[i]['Pos'+str(fish.posHistory[i])].append(fish.idFish)
   

pop = []

for i in range(popSize):
    pop.append(Fish(newID(),ringSize,[],rewards))
for f in pop :
    f.pos = random.randint(0, ringSize -1)
    f.vision = pop
for f in pop:
    if modifyExploRate :
            f.exploreRate = 1
    f.lookAround()
for t in range(runDuration) :
    for f in pop :
        f.decide()
    for f in pop :
        f.act()
    for f in pop :
        f.lookAround()
    for f in pop :
        f.updateQ()
        if modifyExploRate :
            f.exploreRate = f.exploreRate * exploRateDecrease
for f in pop :
    plt.plot(f.timeToGoalHistory)
    print(f.idFish)
    for key,value in f.Q.items():
        print(key)
        print(value)
plt.ylabel('TimeToReachGoal')
plt.xlabel('NumberOfTrial')
title = 'Population=' + str(popSize)
title = title + ';runDuration=' + str(runDuration)
title = title + ";ringSize=" + str(ringSize)
title = title  + ';ID:' + str(newID())
if modifyExploRate :
        title=title+'exploRateDecreasing'
plt.title(title)
plt.savefig('./'+title)
plt.show()
