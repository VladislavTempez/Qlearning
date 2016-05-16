################################################
#                 Dependencies                 #
################################################

from fish import *
import math
import time
import matplotlib.pyplot as plt

################################################
#                 Parameters                   #
################################################

popSize = 5
learnersNumber = 1
runDuration = 1000000
ringSize = 13 
reward = 10
punition = -2
previousKnowledge = {}

#Setting the explore rate evolution. alpha / (alpha + n). 

decreasePoint = 2 /3 # Fraction of the run at which exploreRate is decreaseValue
decreaseValue = 3 / 1000


################################################
#                 Useful values                #
################################################

alpha = decreaseValue * runDuration / (1 - decreaseValue)

def reset(pop,date):
    totalDistanceAtGoal = 0
    numFish = 0
    for f in pop:
        if f.lastReward == reward :
            if f.learning:
                totalDistanceAtGoal = totalDistanceAtGoal + f.moveStock
                f.moveStock = 0
                numFish = numFish + 1
                f.eligibilityTrace = {}
                f.pos = random.randint(0,f.ringSize) % f.ringSize
                if date > runDuration * 2 / 3:
                    f.pos = math.ceil(pop.index(f) * ringSize / popSize) % f.ringSize
            f.dateOfReward.append(date)
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
adults = []
learners = []
averageDistanceSinceGoal=[]
averageDistanceWhenReachingGoal=[]

for i in range(popSize):
    adults.append(Fish(idFish = newID(),
                       ringSize = ringSize,
                       rewards = rewards(punition,reward,minSizeOfGroup = math.floor(popSize*0.9)),
                       alpha = alpha,
                       criticalSize = 1,
                       learning = False))

for i in range(learnersNumber):
    learners.append(Fish(idFish =newID(),
                        ringSize = ringSize,
                        rewards = rewards(punition,reward, minSizeOfGroup = math.floor(popSize*0.9)),
                        alpha = alpha,
                        criticalSize = 1,
                        learning = True))
pop = adults + learners

for f in pop :
    f.pos = pop.index(f) * math.ceil(ringSize / popSize) % f.ringSize
    f.vision = pop

for f in pop:
    f.currentState = f.getState(f)
    f.posHistory.append(f.pos)
################################################
#            Main Loop                         #
################################################

for t in range(runDuration) :
    averageDistanceSinceGoal.append(0)
    averageDistanceWhenReachingGoal.append(0)
    for f in pop :
        f.decide(f)
    for f in pop :
        f.act()
    for f in pop :
        f.update(f)

    totalDistanceAtGoal,numFish = reset(pop,t)

    if (numFish == 0):
        averageDistanceWhenReachingGoal[t] = -1

    else :
        averageDistanceWhenReachingGoal[t] = totalDistanceAtGoal / numFish
    for f in learners:
        averageDistanceSinceGoal[t] = averageDistanceSinceGoal[t] + f.moveStock
    averageDistanceSinceGoal[t] = averageDistanceSinceGoal[t] / popSize

################################################
#                 After Run process            #
################################################
for f in learners:
    f.genLogs()
timeOfReward = []
for f in adults:
    timeOfReward = f.dateOfReward + timeOfReward
timeOfReward = list(set(timeOfReward))
date = time.time()
idFile = math.ceil((date - math.ceil(date))*1000000) % 1000
timeNow = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())

logRun=open('logs/logRunD:'+str(runDuration)+'P:'+str(popSize)+'S:'+str(ringSize)+'-'+timeNow+'-'+str(idFile),'w')

logRun.write('runDuration: ' + str(runDuration) + '\n')
logRun.write('popSize: ' + str(popSize) + '\n')
logRun.write('ringSize: ' + str(ringSize) + '\n')
logRun.write('decreasePoint: ' + str(decreasePoint) + '\n')
logRun.write('decreaseValue: ' + str(decreaseValue) + '\n')

logRun.write('averageDistanceSinceGoal')
logRun.write('\n')
logRun.write(str(averageDistanceSinceGoal))
logRun.write('\n')

logRun.write('averageWhenReachingGoal')
logRun.write('\n')
logRun.write(str(averageDistanceWhenReachingGoal))
logRun.write('\n')
logRun.write('timeOfReward')
logRun.write(str(timeOfReward))
logRun.write('\n')
logRun.close()
plt.plot(averageDistanceWhenReachingGoal)
plt.show()
print(learners[0].Q)
for f in pop:
    plt.plot(f.posHistory)
plt.show()
