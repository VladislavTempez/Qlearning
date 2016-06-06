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

learnersNumber = 1 
adultsNumber = 8 
learntNumber = 1
popSize= learnersNumber + adultsNumber + learntNumber
runDuration = 1*10**(5) 
ringSize = 13 
reward = 100
punition = -2 
previousKnowledge = {}
knowledgeList=['Fish9-2016-06-06 13-10-03-930.log']
#Setting the explore rate evolution. alpha / (alpha + n). 

decreasePoint = 1 /3 # Fraction of the run at which exploreRate is decreaseValue
decreaseValue = 1 / 2 


################################################
#                 Useful values                #
################################################
alpha = decreaseValue * runDuration * decreasePoint / (1 - decreaseValue)
cycleLength = 5*ringSize
def popUpdate(pop,date,cycleLength):
    for f in pop:
        if f.reachGroup  or f.lastReward == reward:
            f.timeInGroup = f.timeInGroup + 1
            f.moveStock = 0
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
def getKnowledgeFromFish(FishName):
    fish = open(FishName,'rb')
    infos = pickle.load(fish)
    Q = pickle.load(fish)
    posHistory = pickle.load(fish)
    fish.close()
    return Q

################################################
#            Variables Initialization          #
################################################

pop = []
adults = []
learners = []
learnt = []
averageDistanceSinceGoal = []
joinGroupDateLearnersHist = []
timeInGroupLearnersHist = []
joinGroupDateAdultsHist = []
timeInGroupAdultsHist = []
joinGroupDateLearntHist = []
timeInGroupLearntHist = []
initialKnowledge = []
for s in knowledgeList:
    initialKnowledge.append(getKnowledgeFromFish('logs/Fish/'+s).copy())
for i in range(adultsNumber):
    adults.append(Fish(idFish = newID(),
                       ringSize = ringSize,
                       rewards = rewards(punition,reward,minSizeOfGroup = math.floor(popSize * 0.8)),
                       alpha = alpha,
                       criticalSize = 1,
                       learning = False))

for i in range(learnersNumber):
    learners.append(Fish(idFish = newID(),
                        ringSize = ringSize,
                        rewards = rewards(punition,reward, minSizeOfGroup = math.floor(popSize * 0.8)),
                        alpha = alpha,
                        criticalSize = 1,
                        learning = True))
for i in range(learntNumber):
    learnt.append(Fish(idFish = newID(),
                    ringSize = ringSize,
                    rewards = rewards(punition,reward, minSizeOfGroup = math.floor(popSize * 0.8)),
                    alpha = alpha,
                    criticalSize = 1,
                    learning = True))

pop = adults + learners + learnt
for f in pop :
    f.pos = pop.index(f) * math.ceil(ringSize / popSize) % f.ringSize
    f.vision = pop

for f in pop:
    f.currentState = f.getState(f)
    f.posHistory.append(f.pos)

for f in learnt:
    f.Q = random.choice(initialKnowledge).copy()
    f.age = runDuration ** 2

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
        f.update(f,t)
    popUpdate(pop,t,cycleLength)
    if t % cycleLength == 0:
        joinGroupDateLearnersHist.append([f.joinGroupDate for f in learners])
        timeInGroupLearnersHist.append([f.timeInGroup for f in learners])
        joinGroupDateAdultsHist.append([f.joinGroupDate for f in adults])
        timeInGroupAdultsHist.append([f.timeInGroup for f in adults])
        timeInGroupLearntHist.append([f.timeInGroup for f in learnt])
        joinGroupDateLearntHist.append([f.joinGroupDate for f in learnt])
        reset(pop,t,cycleLength)
    for f in learners:
        averageDistanceSinceGoal[t] = averageDistanceSinceGoal[t] + f.moveStock
    averageDistanceSinceGoal[t] = averageDistanceSinceGoal[t] / learnersNumber 

################################################
#                 After Run process            #
################################################
timeOfReward = []
for i in range(runDuration):
    timeOfReward.append(0)
for f in learners:
    for j in f.dateOfReward:
            timeOfReward[j] = timeOfReward[j] + 1
date = time.time()
idFile = math.ceil((date - math.ceil(date))*1000000) % 1000
timeNow = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())

for f in learners:
    f.genLogs(idFile,timeNow)

logRun=open('logs/logRunD:'+str(math.log10(runDuration))+'P:'+str(popSize)+'S:'+str(ringSize)+'-'+timeNow+'-'+str(idFile),'wb')
infos='runDuration:' + str(runDuration) + '\n'
infos = infos +'popSize:' + str(popSize) + '\n' 
infos = infos + 'ringSize:' + str(ringSize) + '\n' 
infos= infos + 'decreasePoint:' + str(decreasePoint) + '\n'
infos = infos +'decreaseValue:' + str(decreaseValue) + '\n'
infos = infos + 'learnersNumber:' + str(learnersNumber) + '\n'
infos = infos + 'learntNumber:' + str(learntNumber) + '\n'
pickle.dump(infos,logRun,2)
pickle.dump(averageDistanceSinceGoal,logRun,2)
pickle.dump(timeOfReward,logRun,2)
pickle.dump(joinGroupDateLearnersHist,logRun,2)
pickle.dump(timeInGroupLearnersHist,logRun,2)
pickle.dump(joinGroupDateAdultsHist,logRun,2)
pickle.dump(timeInGroupAdultsHist,logRun,2)
pickle.dump(joinGroupDateLearntHist,logRun,2)
pickle.dump(timeInGroupLearntHist,logRun,2)
for f in adults:
    pickle.dump(f.posHistory,logRun,2)
for f in learners:
    pickle.dump(f.posHistory,logRun,2)
for f in learnt:
    pickle.dump(f.posHistory,logRun,2)
logRun.close()
