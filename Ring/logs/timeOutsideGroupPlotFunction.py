import matplotlib.pyplot as plt
from curves import *
def plotTimeOutGroup(infos,timeInGroupLearnersHist,timeInGroupAdultsHist,joinGroupDateLearnersHist,joinGroupDateAdultsHist):

    [
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
            cycleLength,
            ] = infos
    timeOutsideGroupLearners = [[cycleLength- k[i] for i in range(learnersNumber)] for k in timeInGroupLearnersHist]
    timeOutsideGroupAfterJoiningLearners = [[timeOutsideGroupLearners[k][i] -joinGroupDateLearnersHist[k][i] for i in range(learnersNumber)] for k in range(len(timeOutsideGroupLearners))]
    timeOutsideGroupAdults = [[cycleLength- k[i] for i in range(adultsNumber)]for k in timeInGroupAdultsHist]
    timeOutsideGroupAfterJoiningAdults =  [[timeOutsideGroupAdults[k][i] -joinGroupDateAdultsHist[k][i] for i in range(adultsNumber)] for k in range(len(timeOutsideGroupAdults))]

    for i in range(learnersNumber):
        plt.plot(smoothCurve([t[i] for t in timeOutsideGroupLearners]),color = 'r')
    for i in range(adultsNumber):
        plt.plot(smoothCurve([t[i] for t in timeOutsideGroupAdults]),color = 'b')

    plt.xlabel('Time in fraction of the learning phase')
    plt.ylabel('Average time spent outside the group')
    plt.show()

    for i in range(learnersNumber):
        plt.plot(smoothCurve([t[i] for t in timeOutsideGroupAfterJoiningLearners]),color = 'r')
    for i in range(adultsNumber):
        plt.plot(smoothCurve([t[i] for t in timeOutsideGroupAfterJoiningAdults]),color = 'b')

    plt.xlabel('Time in fraction of the learning phase')
    plt.ylabel('Average time spent outside the group after joining the group')
    plt.show()
    return
