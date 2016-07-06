
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
    groupness1=[]
    groupness2=[]
    groupness3=[]
    maxNumberOfNeighbourHist = []
    minNumberOfNeighbourHist = []
    firstTimeInGroupHist = []
    firstTimeInGroup = cycleLength;
    for i in range(runDuration):
        fishPositionOnRing = []
        for f in range(learnersNumber):
            fishPositionOnRing.append(posHistoryL[f][i])
        for f in range(adultsNumber): 
            fishPositionOnRing.append(posHistoryL[f][i])
        fishRepartitionOnRing = [0 for k in range(ringSize)]
        for j in fishPositionOnRing:
            fishRepartitionOnRing[j] = fishRepartitionOnRing[j] + 1
#Non intuitive metrics        
#sum of squared distances
        stepGroupness1 = sum([sum([fishRepartitionOnRing[k] * fishRepartitionOnRing[j] * min((k-j)%ringSize,(j-k)%ringSize) for k in range(ringSize) if fishRepartitionOnRing[k] > 0]) for j in range(ringSize) if fishRepartitionOnRing[j] > 0]) /2

#distance to next fish
        lastPos = None
        d = 0
        for j in fishRepartitionOnRing:
            if lastPos == None and j>0:
                lastPos = j
            elif j > 0:
                d = d + (j - lastPos)**2
                lastPos = 1
        stepGroupness2 = d

#pseudoConvolution
        a = 0 
        for j in range(len(fishRepartitionOnRing)):
            a = a + fishRepartitionOnRing[j-1]**2 * (fishRepartitionOnRing[j] + fishRepartitionOnRing[j - 2])**1.5
        stepGroupness3 = a


        groupness1.append(stepGroupness1)
        groupness2.append(stepGroupness2)
        groupness3.append(stepGroupness3)

#Size of groups
        numberOfNeighbour = [fishRepartitionOnRing[i - 2] + fishRepartitionOnRing[i - 1] + fishRepartitionOnRing[i] if fishRepartitionOnRing[i] > 0  else 0 for i in range(ringSize)]
        maxNumberOfNeighbour = max(numberOfNeighbour)
        minNumberOfNeighbour = min([i for i in numberOfNeighbour if i > 0])
        maxNumberOfNeighbourHist.append(maxNumberOfNeighbour)
        minNumberOfNeighbourHist.append(minNumberOfNeighbour)

#Time before the first group
        
        if (maxNumberOfNeighbour > minSizeOfGroup) and (i % cycleLength < firstTimeInGroup):
            firstTimeInGroup = i % cycleLength
        if i % cycleLength == 0:
            if i > 0:
                firstTimeInGroupHist.append(firstTimeInGroup)
            firstTimeInGroup = cycleLength;

        print(i % cycleLength,numberOfNeighbour)
    plt.plot(smoothCurve(groupness1))
    plt.xlabel('Time in fraction of elarning phase')
    plt.ylabel('Sum of squared distance between agents')
    plt.show()
    plt.plot(smoothCurve(groupness2))
    plt.xlabel('Time in fraction of elarning phase')
    plt.ylabel('Sum of distances to next fish')
    plt.show()
    plt.plot(smoothCurve(groupness3))
    plt.xlabel('Time in fraction of learning phase')
    plt.ylabel('Area of pseudo convolution')
    plt.show()
    plt.plot(smoothCurve(maxNumberOfNeighbourHist))
    plt.plot(smoothCurve(minNumberOfNeighbourHist))
    plt.xlabel('Time in fraction of learning phase')
    plt.ylabel('Size of larger group and smaller group')
    plt.show()
    plt.plot(smoothCurve(firstTimeInGroupHist,1))
    plt.xlabel('Time in fraction of learning phase')
    plt.ylabel('Time to form group')
    plt.show()
    return


        
