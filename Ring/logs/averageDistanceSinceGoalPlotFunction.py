import matplotlib.pyplot as plt
from curves import *


def plotAverageDistance(infos,averageDistanceSinceGoal):
    [runDuration,popSize,learnersNumber,learntNumber,adultsNumber,ringSize,decreasePoint,decreaseValue] = infos
    plt.plot(smoothSparseCurve(averageDistanceSinceGoal,ringSize*5))
    plt.xlabel('Time in fraction of the learning phase duration')
    plt.ylabel('Average distance stacked since the cycle started for the learners')
    plt.title('Average distance before goal')
    plt.show()
    return
