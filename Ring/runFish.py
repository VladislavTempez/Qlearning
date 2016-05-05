################################################
#                 Dependencies                 #
################################################

from fish import *
import matplotlib.pyplot as plt

################################################
#                 Parameters                   #
################################################

popSize = 5
runDuration = 3000
ringSize = 45 
reward = 10
punition = -2
previousKnowledge = {}

#Setting the explore rate evolution. alpha / (alpha + n). 

decreasePoint = 2 /3 # Fraction of the run at which exploreRate is decreaseValue
decreaseValue = 3 / 1000

def rewards(state):
    near,left,right = state
    if near >= 4:
        return reward
    elif near < 2:
        return punition
    else :
        return 0

################################################
#                 Useful values                #
################################################

alpha = decreaseValue * runDuration / (1 - decreaseValue)

def reset(pop,date):
    totalDistanceAtGoal = 0
    numFish = 0
    for f in pop:
        if f.lastReward>0:
            totalDistanceAtGoal = totalDistanceAtGoal + f.moveStock
            f.moveStock = 0
            numFish = numFish + 1
            f.eligibilityTrace.clear()
            f.pos = pop.index(f) * math.ceil(ringSize / popSize) % f.ringSize
            f.dateOfResetHistory.append(date)
    return(totalDistanceAtGoal,numFish)
   
def smoothCurve(curve,windowsSize):
    res=[]
    for j in range(len(curve)-windowsSize):
        res.append(0)
        for i in range(windowsSize):
            res[j] = res[j] + curve[i+j]
        res[j] =res[j] / windowsSize
    return res
################################################
#            Variables Initialization          #
################################################

pop = []

averageDistanceSinceGoal=[]
averageDistanceWhenReachingGoal=[]
for i in range(popSize):
    pop.append(Fish(idFish = newID(), ringSize = ringSize, rewards = rewards,
        alpha = alpha))

for f in pop :
    f.pos = pop.index(f) * math.ceil(ringSize / popSize) % f.ringSize
    f.vision = pop
    f.currentState = f.getState(f)
    f.posHistory.append(f.pos)
    f.stateHistory.append(f.currentState)


################################################
#            Main Loop                         #
################################################

for t in range(runDuration) :
    averageDistanceSinceGoal.append(0)
    averageDistanceWhenReachingGoal.append(0)
    for f in pop :
        f.decide()
    for f in pop :
        f.act()
    for f in pop :
        f.update()
    totalDistanceAtGoal,numFish = reset(pop,t)
    if (numFish == 0):
        averageDistanceWhenReachingGoal[t] = -1
    else :
        averageDistanceWhenReachingGoal[t] = totalDistanceAtGoal / numFish
    for f in pop:
        averageDistanceSinceGoal[t] = averageDistanceSinceGoal[t] + f.moveStock
    averageDistanceSinceGoal[t] = averageDistanceSinceGoal[t] / popSize

################################################
#                 After Run process            #
################################################
for f in pop:
    f.genLogs()

plt.plot(averageDistanceWhenReachingGoal)
plt.show()
