import matplotlib.pyplot as plt
from curves import *
def plotPos(infos,posHistoryA,posHistoryL,posHistoryLearnt):
    
    [runDuration,popSize,learnersNumber,learntNumber,adultsNumber,ringSize,decreasePoint,decreaseValue] = infos
    maxPlot = min(runDuration, int(ringSize) * 5 *3 )
    
    plotRangeMin = 0
    plotRangeMax = maxPlot - 1
    for f in range(adultsNumber):
        plt.plot(posHistoryA[f][plotRangeMin : plotRangeMax ])
    for f in range(learnersNumber):
        plt.plot(posHistoryL[f][plotRangeMin : plotRangeMax ])
    for f in range(learntNumber):
        plt.plot(posHistoryLearnt[f][plotRangeMin : plotRangeMax ],'ro',color='g')
    plt.xlabel('Time in iterations')
    plt.ylabel('Position of the fishes on the ring')
    plt.title('position of fishes for the '+str(maxPlot)+' first steps')
#   plt.title('position of fishes (learners in red, old fishes in green) for the '+str(maxPlot)+' first steps')
    plt.show()

    plotRangeMin = math.floor(runDuration/2) 
    plotRangeMax = math.floor(runDuration/2)+ maxPlot - 1
    for f in range(adultsNumber):
        plt.plot(posHistoryA[f][plotRangeMin : plotRangeMax ])
    for f in range(learnersNumber):
        plt.plot(posHistoryL[f][plotRangeMin : plotRangeMax ])
    for f in range(learntNumber):
        plt.plot(posHistoryLearnt[f][plotRangeMin : plotRangeMax ],'ro',color='g')
    plt.xlabel('Time in iterations')
    plt.ylabel('Position of the fishes on the ring')
    plt.title('position of fishes for the '+str(maxPlot)+' intermediate steps')
#   plt.title('position of fishes (learners in red, old fishes in green) for the
#   '+str(maxPlot)+' intermediate steps')
    plt.show()

    plotRangeMin = runDuration - maxPlot 
    plotRangeMax = runDuration - 1
    for f in range(adultsNumber):
        plt.plot(posHistoryA[f][ plotRangeMin : plotRangeMax ])
    for f in range(learnersNumber):
        plt.plot(posHistoryL[f][plotRangeMin : plotRangeMax  ])
    for f in range(learntNumber):
        plt.plot(posHistoryLearnt[f][plotRangeMin : plotRangeMax ],'ro',color='g')
    
    plt.xlabel('Time in iterations')
    plt.ylabel('Position of the fishes on the ring')
    plt.title('Position of fishes for the '+str(maxPlot)+' last steps')
#    plt.title('position of fishes (learners in red, old fishes in green) for the '+str(maxPlot)+' last steps')
    plt.show()

    return
