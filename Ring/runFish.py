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
ringSize = 53 
reward = 100
punition = -2 
previousKnowledge = {}

#Setting the explore rate evolution. alpha / (alpha + n). 

decreasePoint = 1 /3 # Fraction of the run at which exploreRate is decreaseValue
decreaseValue = 5 / 10


################################################
#                 Useful values                #
################################################
alpha = decreaseValue * runDuration * decreasePoint / (1 - decreaseValue)
cycleLength = 5*ringSize
def popUpdate(pop,date,cycleLength):
    for f in pop:
        if f.reachGroup  or f.lastReward == reward:
            f.timeInGroup = f.timeInGroup + 1
            if f.joinGroupDate == cycleLength:
                f.joinGroupDate = date % cycleLength 
    return

def reset(pop,date,cycleLength):
    random.shuffle(pop)
    for f in pop:
        f.moveStock = 0
        f.eligibility = {}
        f.timeSinceReward = 0
        f.joinGroupDate = cycleLength
        f.timeInGroup = 0
        f.reachGroup = False
        f.pos = math.ceil( pop.index(f) * f.ringSize / len(pop) ) % f.ringSize
    return
   
def smoothCurve(curve,windowsSize = -1):
    if windowsSize == -1:
        windowsSize = math.ceil(len(curve) /100)
    res=[]
    for j in range(math.ceil(len(curve)/windowsSize)):
        res.append(0)
        for i in range(windowsSize):
            res[j] = res[j] + curve[i+j * windowsSize]
        res[j] =res[j] / windowsSize
    return res

def smoothSparseCurve(curve,windowsSize=-1):
    if windowsSize == -1:
        windowsSize = math.ceil(len(curve) /100)
    res=[]
    for j in range(math.floor(len(curve)/windowsSize)):
        res.append(0)
        numberOfPoint =0
        for i in range(windowsSize):
            p=curve[i+j * windowsSize]
            if p != 0:
                res[j] = res[j] + p
                numberOfPoint = numberOfPoint + 1
        if numberOfPoint == 0:
            res[j]=res[j-1]
        else :
            res[j] =res[j] / numberOfPoint
    return res

################################################
#            Variables Initialization          #
################################################

pop = []
adults = []
learners = []
averageDistanceSinceGoal = []
joinGroupDateLearnersHist = []
timeInGroupLearnersHist = []
joinGroupDateAdultsHist = []
timeInGroupAdultsHist = []
for i in range(adultsNumber):
    adults.append(Fish(idFish = newID(),
                       ringSize = ringSize,
                       rewards = rewards(punition,reward,minSizeOfGroup = math.floor(adultsNumber * 0.8)),
                       alpha = alpha,
                       criticalSize = 1,
                       learning = False))

for i in range(learnersNumber):
    learners.append(Fish(idFish = newID(),
                        ringSize = ringSize,
                        rewards = rewards(punition,reward, minSizeOfGroup = math.floor(adultsNumber * 0.8)),
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
    popUpdate(pop,t,cycleLength)
    if t % cycleLength == 0:
        joinGroupDateLearnersHist.append([f.joinGroupDate for f in learners])
        timeInGroupLearnersHist.append([f.timeInGroup for f in learners])
        joinGroupDateAdultsHist.append([f.joinGroupDate for f in adults])
        timeInGroupAdultsHist.append([f.timeInGroup for f in adults])
        reset(pop,t,cycleLength)
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
pickle.dump(joinGroupDateLearnersHist,logRun,2)
pickle.dump(timeInGroupLearnersHist,logRun,2)
pickle.dump(joinGroupDateAdultsHist,logRun,2)
pickle.dump(timeInGroupAdultsHist,logRun,2)
for f in adults:
    pickle.dump(f.posHistory,logRun,2)
for f in learners:
    pickle.dump(f.posHistory,logRun,2)
logRun.close()
#plt.plot(smoothCurve(stackHistory,50))
#plt.show()
#for f in adults:
#    plt.plot(f.posHistory,'-')
#for f in learners:
#    plt.plot(f.posHistory,'ro')
#plt.show()
