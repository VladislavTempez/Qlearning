################################################
#                 Dependencies                 #
################################################

from fish import *
import math
import time
import pickle
#import matplotlib.pyplot as plt

################################################
#                 Parameters                   #
################################################

popSize = 10 
learnersNumber = 1
adultsNumber = popSize - learnersNumber
runDuration = 1*10**(4) 
ringSize = 13 
reward = 100
punition = -2 
previousKnowledge = {}

#Setting the explore rate evolution. alpha / (alpha + n). 

decreasePoint = 2 /3 # Fraction of the run at which exploreRate is decreaseValue
decreaseValue = 3 / 1000


################################################
#                 Useful values                #
################################################

alpha = decreaseValue * runDuration / (1 - decreaseValue)

def reset(pop,date,cycleLength,stack):
    meanStack = None
    for f in learners:
        if f.lastReward == reward :
            if stack[learners.index(f)] == 0:
                stack[learners.index(f)] = (date % cycleLength)
    if date % cycleLength == 0:
        sumStack = sum([i for i in stack if i != 0 ])
        countNonZeroStack = sum([1 for i in stack if i!= 0])
        if countNonZeroStack == 0:
            meanStack = cycleLength
        else:
            meanStack = sumStack / countNonZeroStack
        random.shuffle(pop)
        stack = [0 for i in range(learnersNumber)]
        for f in pop:
            f.moveStock = 0
            f.eligibility = {}
            f.timeSinceReward = 0
            f.pos = math.ceil( pop.index(f) * f.ringSize / len(pop) ) % f.ringSize
    return(stack,meanStack)
   
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

for i in range(adultsNumber):
    adults.append(Fish(idFish = newID(),
                       ringSize = ringSize,
                       rewards = rewards(punition,reward,minSizeOfGroup = math.floor(adultsNumber * 0.9)),
                       alpha = alpha,
                       criticalSize = 1,
                       learning = False))

for i in range(learnersNumber):
    learners.append(Fish(idFish = newID(),
                        ringSize = ringSize,
                        rewards = rewards(punition,reward, minSizeOfGroup = math.floor(adultsNumber * 0.9)),
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
stack = [0 for i in range(learnersNumber)]
stackHistory = []
################################################
#            Main Loop                         #
################################################

for t in range(runDuration) :
    averageDistanceSinceGoal.append(0)
    for f in pop :
        f.decide(f)
    for f in pop :
        f.act()
    for f in pop :
        f.update(f)

    stack,meanStack = reset(pop,t,ringSize*5,stack)
    if meanStack != None:
        stackHistory.append(meanStack)
    for f in learners:
        averageDistanceSinceGoal[t] = averageDistanceSinceGoal[t] + f.moveStock
    averageDistanceSinceGoal[t] = averageDistanceSinceGoal[t] / learnersNumber 

################################################
#                 After Run process            #
################################################
for f in learners:
    f.genLogs()
timeOfReward = []
for f in learners:
    timeOfReward = f.dateOfReward + timeOfReward
timeOfReward = [timeOfReward.count(i) for i in range(runDuration)]
date = time.time()
idFile = math.ceil((date - math.ceil(date))*1000000) % 1000
timeNow = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())

logRun=open('logs/logRunD:'+str(math.log10(runDuration))+'P:'+str(popSize)+'S:'+str(ringSize)+'-'+timeNow+'-'+str(idFile),'wb')
infos='runDuration:' + str(runDuration) + '\n'
infos = infos +'popSize:' + str(popSize) + '\n' 
infos = infos + 'ringSize:' + str(ringSize) + '\n' 
infos= infos + 'decreasePoint:' + str(decreasePoint) + '\n'
infos = infos +'decreaseValue:' + str(decreaseValue) + '\n'
infos = infos + 'learnersNumber:' + str(learnersNumber) + '\n'
pickle.dump(infos,logRun,2)
pickle.dump(averageDistanceSinceGoal,logRun,2)
pickle.dump(timeOfReward,logRun,2)
pickle.dump(stackHistory,logRun,2)
for f in adults:
    pickle.dump(f.posHistory,logRun,2)
for f in learners:
    pickle.dump(f.posHistory,logRun,2)
logRun.close()
#plt.plot(smoothCurve(stackHistory,50))
#plt.show()
#for f in adults:
#    plt.plot(f.posHistory)
#for f in learners:
#    plt.plot(f.posHistory,'ro')
#plt.show()
