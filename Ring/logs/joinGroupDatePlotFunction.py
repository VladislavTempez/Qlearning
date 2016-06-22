import matplotlib.pyplot as plt
from curves import *
def plotJoinGroup(infos,joinGroupDateAdultsHist,joinGroupDateLearnersHist):
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
            cycleLength
            ] = infos

    for i in range(learnersNumber):
        plt.plot(smoothCurve([t[i] for t in joinGroupDateLearnersHist]),color = 'r')
    for i in range(adultsNumber):
        plt.plot(smoothCurve(joinGroupDateAdultsHist[i]),color = 'b')
    plt.xlabel('Time in fraction of the learning phase')
    plt.ylabel('Average date for reaching group for learners')
    plt.show()
    return
