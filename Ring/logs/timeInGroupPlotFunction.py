import matplotlib.pyplot as plt
from curves import *
def plotTimeInGroup(infos,timeInGroupLearnersHist,timeInGroupAdultsHist):

    [runDuration,popSize,learnersNumber,adultsNumber,ringSize,decreasePoint,decreaseValue] = infos

    for i in range(learnersNumber):
        plt.plot(smoothCurve([t[i] for t in timeInGroupLearnersHist]),color = 'r')
    try:
        plt.plot(smoothCurve([min(t[i] for i in range(adultsNumber)) for t in timeInGroupAdultsHist]),color = 'b')
    except IndexError:
        print('No Adults')
    plt.xlabel('Time in fraction of the learning phase')
    plt.ylabel('Average time spent within the group')
#   plt.title('Time in the group, in red for learners, in green for old fishes and in blue for min in non learners')
    plt.show()
    return
