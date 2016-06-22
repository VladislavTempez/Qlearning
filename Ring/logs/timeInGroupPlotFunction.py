import matplotlib.pyplot as plt
from curves import *
def plotTimeInGroup(infos,timeInGroupLearnersHist,timeInGroupAdultsHist):

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
        plt.plot(smoothCurve([t[i] for t in timeInGroupLearnersHist]),color = 'r')
    for i in range(adultsNumber):
        plt.plot(smoothCurve(timeInGroupAdultsHist[i]),color = 'b')

    plt.xlabel('Time in fraction of the learning phase')
    plt.ylabel('Average time spent within the group')
#   plt.title('Time in the group, in red for learners, in green for old fishes and in blue for min in non learners')
    plt.show()
    return
