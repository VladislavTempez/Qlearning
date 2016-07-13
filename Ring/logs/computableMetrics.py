
import matplotlib.pyplot as plt
from curves import *
def plotMetrics(infos,posHistoryA,posHistoryL):
 
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
    groupness = []
    maxNumberOfNeighbourHist = []
    minNumberOfNeighbourHist = []
    firstTimeInGroupHist = []
    firstTimeInGroup = cycleLength;
    for i in range(runDuration):
        fishPositionOnRing = []
        for f in range(learnersNumber):
            fishPositionOnRing.append(posHistoryL[f][i])
        for f in range(adultsNumber): 
            fishPositionOnRing.append(posHistoryA[f][i])
        fishRepartitionOnRing = [0 for k in range(ringSize)]
        for j in fishPositionOnRing:
            fishRepartitionOnRing[j] = fishRepartitionOnRing[j] + 1
#sum of squared distances
        stepGroupness = sum([sum([fishRepartitionOnRing[k] * fishRepartitionOnRing[j] * min((k-j)%ringSize,(j-k)%ringSize) for k in range(ringSize) if fishRepartitionOnRing[k] > 0]) for j in range(ringSize) if fishRepartitionOnRing[j] > 0]) /2

        groupness.append(stepGroupness)

#Size of groups
        numberOfNeighbour = [fishRepartitionOnRing[j - 2] + fishRepartitionOnRing[j - 1] + fishRepartitionOnRing[j] if fishRepartitionOnRing[j] > 0  else 0 for j in range(ringSize)]
        maxNumberOfNeighbour = max(numberOfNeighbour)
        minNumberOfNeighbour = min([j for j in numberOfNeighbour if j > 0])
        maxNumberOfNeighbourHist.append(maxNumberOfNeighbour)
        minNumberOfNeighbourHist.append(minNumberOfNeighbour)

#Time before the first group
        
        if (maxNumberOfNeighbour > minSizeOfGroup) and (i % cycleLength < firstTimeInGroup):
            firstTimeInGroup = i % cycleLength
        if i % cycleLength == 0:
            if i > 0:
                firstTimeInGroupHist.append(firstTimeInGroup)
            firstTimeInGroup = cycleLength;

    plt.plot(smoothCurve(groupness))
    plt.xlabel('Time in fraction of learning phase')
    plt.ylabel('Sum of squared distance between agents')
    plt.show()
    plt.plot(smoothCurve(maxNumberOfNeighbourHist))
    plt.plot(smoothCurve(minNumberOfNeighbourHist))
    plt.xlabel('Time in fraction of learning phase')
    plt.ylabel('Size of larger number of neighbour and smaller number of neighbour')
    plt.show()
    plt.plot(smoothCurve(firstTimeInGroupHist))
    plt.xlabel('Time in fraction of learning phase')
    plt.ylabel('Time to form group')
    plt.show()
    return


        
