################################################
#                 Dependencies                 #
################################################

from fish import *
import math
import time
import pickle
from QmapFunctions import *
#import matplotlib.pyplot as plt

################################################
#                 Parameters                   #
################################################

learnersNumber = 10
adultsNumber = 0 
popSize= learnersNumber + adultsNumber
ringSize = 13 
cycleLength = 5 * ringSize
runDuration = cycleLength * 2500
reward = 100
penalty = -5 
minSizeOfGroup = math.floor(10 * 0.8)
minimumDistanceToBeInGroup = 1
previousKnowledge = {}

# Setting the parameters for explore rate evolution in alpha / (alpha + n). 
# Fraction of the run at which exploreRate is decreaseValue
decreasePoint = 1 / 2
decreaseValue = 1 / 2 
# Fraction of the simulation at which there is no longer exploration and behaviour is tested.
pointToStopExploration = 9/10 * runDuration

################################################
#                 Useful values                #
################################################
alpha = decreaseValue * runDuration * decreasePoint / (1 - decreaseValue)



def popUpdate(pop,date,cycleLength):
    for f in pop:
        if f.lastReward == reward:
            f.timeInGroup = f.timeInGroup + 1
            if f.joinGroupDate == cycleLength:
                f.joinGroupDate = date % cycleLength 
    return

def reset(pop,date,cycleLength):
    random.shuffle(pop)
    for f in pop:
        f.eligibility = {}
        f.timeSinceReward = 0
        f.joinGroupDate = cycleLength
        f.timeInGroup = 0
        f.pos = (pop.index(f) * math.ceil(f.ringSize / len(pop)) + round(2*random.random()-1) ) % f.ringSize
    return
   
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
joinGroupDateLearnersHist = []
timeInGroupLearnersHist = []
joinGroupDateAdultsHist = []
timeInGroupAdultsHist = []
initialKnowledge = []
try:
    fishNamesFile = open('logs/Fish/FishToIntegrate','r')
    fishNamesList = fishNamesFile.read().split('\n')
    listQmap = [getKnowledgeFromFish('logs/Fish/'+fishName) for fishName in fishNamesList if fishName != '']
except FileNotFoundError:
    listQmap = [{}]

for i in range(adultsNumber):
    adults.append(Fish(idFish = newID(),
                       ringSize = ringSize,
                       rewards = rewards(penalty,reward,minSizeOfGroup = minSizeOfGroup),
                       alpha = alpha,
                       criticalSize = minimumDistanceToBeInGroup,
                       ))

for i in range(learnersNumber):
    learners.append(Fish(idFish = newID(),
                        ringSize = ringSize,
                        rewards = rewards(penalty,reward, minSizeOfGroup = minSizeOfGroup),
                        alpha = alpha,
                        criticalSize = minimumDistanceToBeInGroup,
                        ))
pop = adults + learners

for f in adults:
    f.Q = random.choice(listQmap).copy()
    f.exploreRateMutable = False
    f.exploreRate = 0
    f.learningRateMutable = False
    f.learningRate = 0
for f in pop :
    f.pos = (pop.index(f) * math.ceil(f.ringSize / len(pop)) + round(2*random.random()-1) ) % f.ringSize
    f.vision = pop

for f in pop:
    f.currentState = f.getState(f)
    f.posHistory.append(f.pos)

################################################
#            Main Loop                         #
################################################

for t in range(runDuration) :
    if t % cycleLength == 0:
        joinGroupDateLearnersHist.append([f.joinGroupDate for f in learners])
        timeInGroupLearnersHist.append([f.timeInGroup for f in learners])
        joinGroupDateAdultsHist.append([f.joinGroupDate for f in adults])
        timeInGroupAdultsHist.append([f.timeInGroup for f in adults])
        reset(pop,t,cycleLength)
    for f in pop :
        f.policy(f)
    for f in pop :
        f.act()
    for f in pop :
        f.update(f,t)
        if t > pointToStopExploration:
            f.exploreRate = 0
            f.learningRate = 0
    popUpdate(pop,t,cycleLength)

################################################
#                 After Run process            #
################################################
print([len(f.Q) for f in pop])
print(distanceMatrix([f.Q for f in pop],discreteDistance))
timeOfReward = []
for i in range(runDuration):
    timeOfReward.append(0)
for f in pop:
    for j in f.dateOfReward:
            timeOfReward[j] = timeOfReward[j] + 1
date = time.time()
idFile = math.ceil((date - math.ceil(date))*1000000) % 1000
timeNow = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())

for f in pop:
    f.genLogs(idFile,timeNow)

logRun=open('logs/logRunD_'+str(math.log10(runDuration))+'P_'+str(popSize)+'S_'+str(ringSize)+'-'+timeNow+'-'+str(idFile)+'.log','wb')

infos='runDuration:' + str(runDuration) + '\n'
infos = infos +'popSize:' + str(popSize) + '\n' 
infos = infos + 'ringSize:' + str(ringSize) + '\n' 
infos = infos + 'decreasePoint:' + str(decreasePoint) + '\n'
infos = infos + 'decreaseValue:' + str(decreaseValue) + '\n'
infos = infos + 'learnersNumber:' + str(learnersNumber) + '\n'
infos = infos + 'adultsNumber:' + str(adultsNumber) + '\n'
infos = infos + 'reward:' + str(reward) + '\n'
infos = infos + 'penalty:' + str(penalty) + '\n'
infos = infos + 'minSizeOfGroup:' + str(minSizeOfGroup) + '\n'
infos = infos + 'minimumDistanceToBeInGroup:' + str(minimumDistanceToBeInGroup) + '\n'
infos = infos + 'pointToStopExploration:' + str(pointToStopExploration) + '\n'
infos = infos + 'cycleLength:' + str(cycleLength) + '\n'
pickle.dump(infos,logRun,2)

pickle.dump(timeOfReward,logRun,2)
if learnersNumber > 0:
    pickle.dump(joinGroupDateLearnersHist,logRun,2)
    pickle.dump(timeInGroupLearnersHist,logRun,2)
if adultsNumber > 0:
    pickle.dump(joinGroupDateAdultsHist,logRun,2)
    pickle.dump(timeInGroupAdultsHist,logRun,2)
for f in adults:
    pickle.dump(f.posHistory,logRun,2)
for f in learners:
    pickle.dump(f.posHistory,logRun,2)
logRun.close()
