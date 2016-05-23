import matplotlib.pyplot as plt
import math
import pickle
from sys import argv

def smoothCurve(curve,windowsSize = -1):
    if windowsSize == -1:
        windowsSize = math.ceil(len(curve) /100)
    res=[]
    for j in range(math.ceil(len(curve)/windowsSize)):
        res.append(0)
        for i in range(windowsSize):
            res[j] = res[j] + curve[i+j * windowsSize]
        res[j] =res[j] / windowsSize
    return res
def smoothSparseCurve(curve,windowsSize=-1):
    if windowsSize == -1:
        windowsSize = math.ceil(len(curve) /100)
    res=[]
    for j in range(math.floor(len(curve)/windowsSize)):
        res.append(0)
        numberOfPoint =0
        for i in range(windowsSize):
            p=curve[i+j * windowsSize]
            if p != 0:
                res[j] = res[j] + p
                numberOfPoint = numberOfPoint + 1
        if numberOfPoint == 0:
            res[j]=res[j-1]
        else :
            res[j] =res[j] / numberOfPoint
    return res

script, filename = argv
logFile = open(filename,'rb')
infos = pickle.load(logFile)
averageDistanceSinceGoal = pickle.load(logFile)
timeOfReward = pickle.load(logFile)
stackHistory = pickle.load(logFile)
infos = infos.split('\n')
runDuration = int(infos[0].split(':')[1])
print(runDuration)
popSize = int(infos[1].split(':')[1])
print(popSize)
ringSize = float(infos[2].split(':')[1])
print(ringSize)
decreasePoint = float(infos[3].split(':')[1])
print(decreasePoint)
decreaseValue = float(infos[4].split(':')[1])
print(decreaseValue)
learnersNumber = int(infos[5].split(':')[1])
print(learnersNumber)
posHistoryA=[]
posHistoryL=[]
maxPlot=min(runDuration,2000)
for f in range(popSize-learnersNumber):
    posHistoryA.append(pickle.load(logFile))
for f in range(learnersNumber):
    posHistoryL.append(pickle.load(logFile))
logFile.close()
plt.plot(smoothCurve(timeOfReward))
plt.title('average number of rewards')
plt.show()
plt.plot(smoothSparseCurve(stackHistory))
plt.title('average date of joinging the group')
plt.show()
plt.plot(smoothCurve(averageDistanceSinceGoal))
plt.title('average distance since goal')
plt.show()
subHist=[]
for f in range(popSize-learnersNumber):
    plt.plot(posHistoryA[f][ runDuration - maxPlot : runDuration - 1],color='g')
for f in range(learnersNumber):
    plt.plot(posHistoryL[f][runDuration - maxPlot : runDuration - 1],'ro',color='r')
plt.title('position of fishes')
plt.show()
