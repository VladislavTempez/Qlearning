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
runDuration = 1000
ringSize = 37 
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

def reset(pop,date,cycleLength):

    totalDistanceAtGoal = 0
    numFish = 0
    if date % cycleLength == 0:
        random.shuffle(pop)
        for f in pop:
            f.eligibility={}
            f.pos = math.ceil( pop.index(f) * f.ringSize / len(pop) ) % f.ringSize
    for f in pop:
        if f.lastReward == reward :
            if f.learning:
                totalDistanceAtGoal = totalDistanceAtGoal + f.moveStock
                f.moveStock = 0
                numFish = numFish + 1
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

for i in range(adultsNumber):
    adults.append(Fish(idFish = newID(),
                       ringSize = ringSize,
                       rewards = rewards(punition,reward,minSizeOfGroup = math.floor(adultsNumber * 0.9)),
                       alpha = alpha,
                       criticalSize = 1,
                       learning = False))

for i in range(learnersNumber):
    learners.append(Fish(idFish =newID(),
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

    totalDistanceAtGoal,numFish = reset(pop,t,ringSize*5)

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
timeOfReward = list(set(timeOfReward))
date = time.time()
idFile = math.ceil((date - math.ceil(date))*1000000) % 1000
timeNow = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())

logRun=open('logs/logRunD:'+str(math.log10(runDuration))+'P:'+str(popSize)+'S:'+str(ringSize)+'-'+timeNow+'-'+str(idFile),'wb')
infos='runDuration:' + str(runDuration) + '\n'
infos = infos +'popSize:' + str(popSize) + '\n' 
infos = infos + 'ringSize:' + str(ringSize) + '\n' 
infos= infos + 'decreasePoint:' + str(decreasePoint) + '\n'
infos = infos +'decreaseValue:' + str(decreaseValue) + '\n'

pickle.dump(infos,logRun)
pickle.dump(averageDistanceSinceGoal,logRun)
pickle.dump(timeOfReward,logRun)
for f in pop:
    pickle.dump(f.posHistory,logRun)
logRun.close()

#for f in pop:
#    plt.plot(f.posHistory)
#plt.show()
