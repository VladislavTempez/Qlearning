import matplotlib.pyplot as plt
from curves import *
def plotJoinGroup(infos,joinGroupDateAdultsHist,joinGroupDateLearnersHist):

    [runDuration,popSize,learnersNumber,adultsNumber,ringSize,decreasePoint,decreaseValue] = infos
    
    for i in range(learnersNumber):
        plt.plot(smoothCurve([t[i] for t in joinGroupDateLearnersHist]),color = 'r')
    try:
        plt.plot(smoothCurve([max(t[i] for i in range(adultsNumber)) for t in joinGroupDateAdultsHist]),color = 'b')
    except IndexError:
        print('No Adults')
#   plt.title('date of joinging the group, in red for learners, in green for old fishes and in blue for last of non learners')
    plt.xlabel('Time in fraction of the learning phase')
    plt.ylabel('Average date for reaching group for learners')
    plt.show()
    return
