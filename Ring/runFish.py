################################################
#                 Dependencies                 #
################################################
#import fish class
from fish import *
#to copy Qmaps
import copy
import math
#To date the end of the learnin phase
import time
#To write logs
import pickle
#To readQmaps and compare them
from QmapFunctions import *

################################################
#                 Parameters                   #
################################################

learnersNumber = 10
adultsNumber = 0 
popSize = learnersNumber + adultsNumber
ringSize = 13 
#At the begining of a cycle, positions are reset
cycleLength = 5 * ringSize

runDuration = cycleLength *  15000

#reward for being in the group
reward = 100

#penalty for begin alone in the central sector
penalty = -5 

#Minimum number of individuals in the group
minSizeOfGroup = math.floor(10 * 0.8)

minimumDistanceToBeInGroup = 1

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

#update information about population
def popUpdate(pop,date,cycleLength):
    for f in pop:
        if f.lastReward == reward:
            f.timeInGroup = f.timeInGroup + 1
            if f.joinGroupDate == cycleLength:
                f.joinGroupDate = date % cycleLength 
    return

#Reset position of the fishes and the cycle informations
def reset(pop,date,cycleLength):
    random.shuffle(pop)
    for f in pop:
        f.eligibility = {}
        f.timeSinceReward = 0
        f.joinGroupDate = cycleLength
        f.timeInGroup = 0
        f.pos = (pop.index(f) * math.ceil(f.ringSize / len(pop)) + round(2*random.random()-1) ) % f.ringSize
    return

#Load Qmap from a fish file
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

#metrics
joinGroupDateLearnersHist = []
timeInGroupLearnersHist = []
joinGroupDateAdultsHist = []
timeInGroupAdultsHist = []

#Get a Qmap list from a list of fish files
try:
    fishNamesFile = open('logs/Fish/FishToIntegrate','r')
    fishNamesList = fishNamesFile.read().split('\n')
    listQmap = [getKnowledgeFromFish('logs/Fish/'+fishName) for fishName in fishNamesList if fishName != '']
except FileNotFoundError:
    print('No adults found')
    listQmap = [{}]

#Initializing adults
for i in range(adultsNumber):
    adults.append(Fish(idFish = newID(),
                       ringSize = ringSize,
                       rewards = rewards(penalty,reward,minSizeOfGroup = minSizeOfGroup),
                       alpha = alpha,
                       criticalSize = minimumDistanceToBeInGroup,
                       ))

#Initializing learners 
for i in range(learnersNumber):
    learners.append(Fish(idFish = newID(),
                        ringSize = ringSize,
                        rewards = rewards(penalty,reward, minSizeOfGroup = minSizeOfGroup),
                        alpha = alpha,
                        criticalSize = minimumDistanceToBeInGroup,
                        ))

pop = adults + learners

#Giving already filled Qmaps for adults
for f in adults:
    if len(listQmap) >= len(adults):
        f.Q = listQmap[adults.index(f)].copy()
    else:
        f.Q = random.choice(listQmap).copy()
    f.exploreRateMutable = False
    f.exploreRate = 0.
    f.learningRateMutable = False
    f.learningRate = 0.0

#Initializing position a vision (i.e. the other agents that are seen by the agent)
for f in pop :
    f.pos = (pop.index(f) * math.ceil(f.ringSize / len(pop)) + round(2*random.random()-1) ) % f.ringSize
    f.vision = pop

#Initializing the state of the environement
for f in pop:
    f.currentState = f.getState(f)
    f.posHistory.append(f.pos)

################################################
#            Main Loop                         #
################################################

for t in range(runDuration) :
    #Begining of a cycle.
    if t % cycleLength == 0:
        joinGroupDateLearnersHist.append([f.joinGroupDate for f in learners])
        timeInGroupLearnersHist.append([f.timeInGroup for f in learners])
        joinGroupDateAdultsHist.append([f.joinGroupDate for f in adults])
        timeInGroupAdultsHist.append([f.timeInGroup for f in adults])
        reset(pop,t,cycleLength)

    #After a point the fishes are no longer exploring.
    if t > pointToStopExploration:
        f.exploreRateMutable = False
        f.learningRateMutable = False
        f.exploreRate = 0.1
        f.learningRate = 0

    #Deciding next action according to policy.
    for f in pop :
        f.policy(f)

    #Performing next action.
    for f in pop :
        f.act()

    #Updating the state of the agents in the neww environment.
    for f in pop :
        f.update(f,t)

    #Updating the metrics after a step
    popUpdate(pop,t,cycleLength)

################################################
#                 After Run process            #
################################################

#print([len(f.Q) for f in learners])
#print(distanceMatrix([f.Q for f in pop],discreteDistance))

#Computing the average number of rewards
timeOfReward = []
for i in range(runDuration):
    timeOfReward.append(0)
for f in pop:
    for j in f.dateOfReward:
            timeOfReward[j] = timeOfReward[j] + 1

#Generating file name and unique ID
date = time.time()
idFile = math.ceil((date - math.ceil(date))*1000000) % 1000
timeNow = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())

#Generating fishes logs
for f in pop:
    f.genLogs(idFile,timeNow)

#Generating logs for the whole learning phase
logRun = open('logs/logRunD_'+str(math.log10(runDuration))+'P_'+str(popSize)+'S_'+str(ringSize)+'-'+timeNow+'-'+str(idFile)+'.log','wb')

#Learning phase parameters stored
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

#Writing Data
pickle.dump(infos,logRun,2)

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

#Second run to test
################################################
#                 Parameters 2                 #
################################################

learnersNumber2 = 0
adultsNumber2 = 9
popSize2 = learnersNumber2 + adultsNumber2
ringSize2 = 13 
#At the begining of a cycle, positions are reset
cycleLength2 = 5 * ringSize2

runDuration2 = cycleLength2 *  5 * 0

#reward for being in the group
reward2 = 100

#penalty for begin alone in the central sector
penalty2 = -5 

#Minimum number of individuals in the group
minSizeOfGroup2 = math.floor(10 * 0.8)

minimumDistanceToBeInGroup2 = 1

# Setting the parameters for explore rate evolution in alpha / (alpha + n). 
# Fraction of the run at which exploreRate is decreaseValue
decreasePoint2 = 1 / 2
decreaseValue2 = 1 / 2 

# Fraction of the simulation at which there is no longer exploration and behaviour is tested.
pointToStopExploration2 = 9/10 * runDuration2
################################################
#            Variables Initialization 2        #
################################################

pop2 = []
adults2 = []
learners2 = []
joinGroupDateLearnersHist2 = []
timeInGroupLearnersHist2 = []
joinGroupDateAdultsHist2 = []
timeInGroupAdultsHist2 = []




#Get a Qmap list from a list of fish files
try:
#    fishNamesList = ['Fish'+str(idFish)+'-' + timeNow + '-' + str(idFile)+'.log' for idFish in range(10)]
#    fishNamesFile = open('logs/Fish/FishToIntegrate','w')
#    for s in ['Fish'+str(idFish)+'-' + timeNow + '-' + str(idFile)+'.log' for idFish in range(10)]:
#        fishNamesFile.write(s+'\n')
#    fishNamesFile.close()

    fishNamesFile = open('logs/Fish/FishToIntegrate','r')
    fishNamesList = fishNamesFile.read().split('\n')
    listQmap = [getKnowledgeFromFish('logs/Fish/'+fishName) for fishName in fishNamesList if fishName != '']
except FileNotFoundError:
    print('No adults found')
    listQmap = [{}]

for i in range(adultsNumber2):
    adults2.append(Fish(idFish = newID(),
                        ringSize = ringSize2,
                        rewards = rewards(penalty2,reward2, minSizeOfGroup = minSizeOfGroup2),
                        alpha = alpha,
                        criticalSize = minimumDistanceToBeInGroup2,
                        ))
for i in range(learnersNumber2):
    learners2.append(Fish(idFish = newID(),
                        ringSize = ringSize2,
                        rewards = rewards(penalty2,reward2, minSizeOfGroup = minSizeOfGroup2),
                        alpha = alpha,
                        criticalSize = minimumDistanceToBeInGroup2,
                        ))
for f in learners2:
    if len(listQmap) >= len(learners2):
        f.Q=listQmap[learners2.index(f)].copy()
    else:
        f.Q = random.choice(listQmap).copy()
    f.exploreRateMutable = False
    f.exploreRate = 0.0
    f.learningRateMutable = False
    f.learningRate = 0.0

pop2 = adults2 + learners2

for f in pop2 :
    f.pos = (pop2.index(f) * math.ceil(f.ringSize / len(pop2)) + round(2*random.random()-1) ) % f.ringSize
    f.vision = pop2

for f in pop2:
    f.currentState = f.getState(f)
    f.posHistory.append(f.pos)
    f.exploreRateMutable = False
    f.learningRateMutable = False
    f.exploreRate = 0.1
    f.learningRate = 0

################################################
#              Main Loop 2                     #
################################################

for t in range(runDuration2) :
    if t % cycleLength2 == 0:
        joinGroupDateLearnersHist2.append([f.joinGroupDate for f in learners2])
        timeInGroupLearnersHist2.append([f.timeInGroup for f in learners2])
        joinGroupDateAdultsHist2.append([f.joinGroupDate for f in adults2])
        timeInGroupAdultsHist2.append([f.timeInGroup for f in adults2])
        reset(pop2,t,cycleLength)
    for f in pop2 :
        f.policy(f)
    for f in pop2 :
        f.act()
    for f in pop2 :
        f.update(f,t)
    popUpdate(pop2,t,cycleLength2)

################################################
#             After Run process 2              #
################################################

timeOfReward2 = []

for i in range(runDuration2):
    timeOfReward2.append(0)
for f in pop2:
    for j in f.dateOfReward:
            timeOfReward2[j] = timeOfReward2[j] + 1
date2 = time.time()
idFile2 = math.ceil((date2 - math.ceil(date2))*1000000) % 1000
timeNow2 = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())

logRun2=open('logs/logTestD_'+str(math.log10(runDuration2))+'P_'+str(popSize2)+'S_'+str(ringSize2)+'-'+timeNow2+'-'+str(idFile2)+'.log','wb')

infos2 = 'runDuration:' + str(runDuration2) + '\n'
infos2 = infos2 +'popSize:' + str(popSize2) + '\n' 
infos2 = infos2 + 'ringSize:' + str(ringSize2) + '\n' 
infos2 = infos2 + 'decreasePoint:' + str(decreasePoint2) + '\n'
infos2 = infos2 + 'decreaseValue:' + str(decreaseValue2) + '\n'
infos2 = infos2 + 'learnersNumber:' + str(learnersNumber2) + '\n'
infos2 = infos2 + 'adultsNumber:' + str(adultsNumber2) + '\n'
infos2 = infos2 + 'reward:' + str(reward2) + '\n'
infos2 = infos2 + 'penalty:' + str(penalty2) + '\n'
infos2 = infos2 + 'minSizeOfGroup:' + str(minSizeOfGroup2) + '\n'
infos2 = infos2 + 'minimumDistanceToBeInGroup:' + str(minimumDistanceToBeInGroup2) + '\n'
infos2 = infos2 + 'pointToStopExploration:' + str(pointToStopExploration2) + '\n'
infos2 = infos2 + 'cycleLength:' + str(cycleLength2) + '\n'
pickle.dump(infos2,logRun2,2)

pickle.dump(timeOfReward2,logRun2,2)
pickle.dump(joinGroupDateLearnersHist2,logRun2,2)
pickle.dump(timeInGroupLearnersHist2,logRun2,2)
pickle.dump(joinGroupDateAdultsHist2,logRun2,2)
pickle.dump(timeInGroupAdultsHist2,logRun2,2)
for f in adults2:
    pickle.dump(f.posHistory,logRun2,2)
for f in learners2:
    pickle.dump(f.posHistory,logRun2,2)
logRun2.close()
