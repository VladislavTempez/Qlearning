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

runDuration = cycleLength *  25

#reward for being in the group
reward = 100

#penalty for begin alone in the central sector
penalty = -50 

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

#Reset position of the fishes and the cycle informations
def reset(pop,date,cycleLength):
    random.shuffle(pop)
    for f in pop:
        f.eligibility = {}
        f.timeSinceReward = 0
        f.lastState = None
        f.joinGroupDate = cycleLength
        f.timeInGroup = 0
        f.pos = (pop.index(f) * math.ceil(f.ringSize / len(pop)) + round(2*random.random()-1) ) % f.ringSize
        f.currentState = f.getState(f)
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

################################################
#            Main Loop                         #
################################################

for t in range(runDuration):
    #Begining of a cycle.
    if t % cycleLength == 0 and t > 0:
        joinGroupDateLearnersHist.append([f.joinGroupDate for f in learners])
        timeInGroupLearnersHist.append([f.timeInGroup for f in learners])
        joinGroupDateAdultsHist.append([f.joinGroupDate for f in adults])
        timeInGroupAdultsHist.append([f.timeInGroup for f in adults])
        reset(pop,t,cycleLength)

    #Updating the state of the agents in the neww environment.
    for f in pop :
        f.update(f,t)

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

