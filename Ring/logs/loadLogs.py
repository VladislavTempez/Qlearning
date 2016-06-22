import pickle
from curves import *
def load(filename):
    logFile = open(filename,'rb')

    infos = pickle.load(logFile)

    timeOfReward = pickle.load(logFile)

    infos = infos.split('\n')
    runDuration = int(infos[0].split(':')[1])
    popSize = int(infos[1].split(':')[1])
    ringSize = int(infos[2].split(':')[1])
    decreasePoint = float(infos[3].split(':')[1])
    decreaseValue = float(infos[4].split(':')[1])
    learnersNumber = int(infos[5].split(':')[1])
    adultsNumber = int(infos[6].split(':')[1])
    reward = int(infos[7].split(':')[1])
    penalty = int(infos[8].split(':')[1])
    minSizeOfGroup = int(infos[9].split(':')[1])
    minimumDistanceToBeInGroup = int(infos[10].split(':')[1])
    pointToStopExploration = int(float(infos[11].split(':')[1]))
    cycleLength = int(infos[12].split(':')[1])
    infosValues = [
            runDuration,
            popSize,
            ringSize,
            decreasePoint,
            decreaseValue,
            learnersNumber,
            adultsNumber,
            reward,
            penalty,
            minSizeOfGroup,
            minimumDistanceToBeInGroup,
            pointToStopExploration,
            cycleLength
            ]
    print('Run Duration :',runDuration)
    print('Population Size :',popSize)
    print('Learners :',learnersNumber)
    print('Adults :',adultsNumber)
    print('Ring Size :',ringSize)
    print('Cycle length is',cycleLength)
    print('At ',decreasePoint,' of the run, learning rate is ',decreaseValue)
    print('After', pointToStopExploration/runDuration,  'of the learning phase, the fishes are no longer exploring at all')
    print('Reward for being in the group is', reward, ', penalty for being alone is',penalty)
    print('The group is at least of size', minSizeOfGroup, 'and its members are at most', minimumDistanceToBeInGroup, 'far from each other')
    joinGroupDateLearnersHist = [] 
    timeInGroupLearnersHist = []
    joinGroupDateAdultsHist = []
    timeInGroupAdultsHist = [] 
    if learnersNumber > 0 :
        joinGroupDateLearnersHist = pickle.load(logFile)
        timeInGroupLearnersHist = pickle.load(logFile)
    if adultsNumber > 0:
        joinGroupDateAdultsHist = pickle.load(logFile)
        timeInGroupAdultsHist = pickle.load(logFile)
    posHistoryA = []
    posHistoryL = []
    for f in range(adultsNumber):
        posHistoryA.append(pickle.load(logFile))
    for f in range(learnersNumber):
        posHistoryL.append(pickle.load(logFile))
    logFile.close()
    return (infosValues,timeOfReward,joinGroupDateLearnersHist,timeInGroupLearnersHist,joinGroupDateAdultsHist,timeInGroupAdultsHist,posHistoryA,posHistoryL)

