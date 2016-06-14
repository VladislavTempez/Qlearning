import matplotlib.pyplot as plt
from curves import *


def plotAverageReward(infos,timeOfReward):
    [runDuration,popSize,learnersNumber,learntNumber,adultsNumber,ringSize,decreasePoint,decreaseValue] = infos

    plt.plot(smoothCurve(timeOfReward))
    plt.xlabel('Time in fraction of the learning phase duration')
    plt.ylabel('Average number of reward for the learners')
    plt.title('Average number of rewards')
    plt.show()
    return
