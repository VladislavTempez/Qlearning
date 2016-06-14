import pickle
from curves import *
def load(filename):
    logFile = open(filename,'rb')

    infos = pickle.load(logFile)

    averageDistanceSinceGoal = pickle.load(logFile)
    timeOfReward = pickle.load(logFile)

    infos = infos.split('\n')
    runDuration = int(infos[0].split(':')[1])
    print('Run Duration :',runDuration)
    popSize = int(infos[1].split(':')[1])
    print('Population Size :',popSize)
    learnersNumber = int(infos[5].split(':')[1])
    print('Learners :',learnersNumber)
    try:
        learntNumber = int(infos[6].split(':')[1])
    except IndexError:
        learntNumber = 0
    print('Learnt :',learntNumber)
    adultsNumber = popSize-learnersNumber-learntNumber
    print('Adults :',adultsNumber)
    ringSize = float(infos[2].split(':')[1])
    print('Ring Size :',ringSize)
    decreasePoint = float(infos[3].split(':')[1])
    decreaseValue = float(infos[4].split(':')[1])
    print('At ',decreasePoint,' of the run, learning rate is ',decreaseValue)
    infosValues = [runDuration,popSize,learnersNumber,learntNumber,adultsNumber,ringSize,decreasePoint,decreaseValue]
    joinGroupDateLearnersHist = [] 
    timeInGroupLearnersHist = []
    joinGroupDateAdultsHist = []
    timeInGroupAdultsHist = [] 
    joinGroupDateLearntHist = []
    timeInGroupLearntHist = [] 
    if learnersNumber > 0 :
        joinGroupDateLearnersHist = pickle.load(logFile)
        timeInGroupLearnersHist = pickle.load(logFile)
    if adultsNumber > 0:
        joinGroupDateAdultsHist = pickle.load(logFile)
        timeInGroupAdultsHist = pickle.load(logFile)
    if learntNumber > 0:
        joinGroupDateLearntHist = pickle.load(logFile)
        timeInGroupLearntHist = pickle.load(logFile)
    posHistoryA = []
    posHistoryL = []
    posHistoryLearnt=[]
    for f in range(adultsNumber):
        posHistoryA.append(pickle.load(logFile))
    for f in range(learnersNumber):
        posHistoryL.append(pickle.load(logFile))
    for f in range(learntNumber):
        posHistoryLearnt.append(pickle.load(logFile))
    logFile.close()
    return (infosValues,averageDistanceSinceGoal,timeOfReward,joinGroupDateLearnersHist,timeInGroupLearnersHist,joinGroupDateAdultsHist,timeInGroupAdultsHist,joinGroupDateLearntHist,timeInGroupLearntHist,posHistoryA,posHistoryL,posHistoryLearnt)

