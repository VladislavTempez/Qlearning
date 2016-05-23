import matplotlib.pyplot as plt
import pickle
from sys import argv

def smoothCurve(curve,windowsSize):
    res=[]
    for j in range(len(curve)-windowsSize):
        res.append(0)
        for i in range(windowsSize):
            res[j] = res[j] + curve[i+j]
        res[j] =res[j] / windowsSize
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
posHistory=[]
maxPlot=min(runDuration,500)
for f in range(popSize):
    posHistory.append(pickle.load(logFile))
logFile.close()
plt.plot(smoothCurve(timeOfReward,100))
plt.title('average number of rewards')
plt.show()
plt.plot(stackHistory)
plt.title('average date of joinging the group')
plt.show()
plt.plot([averageDistanceSinceGoal[runDuration - maxPlot + i] for i in range(0,maxPlot)])
plt.title('average distance since goal')
plt.show()
subHist=[]
for f in range(popSize-learnersNumber):
    subHist.append([posHistory[f][runDuration - maxPlot + i] for i in range(0,maxPlot)])
    plt.plot(subHist[f])
for f in range(learnersNumber):
    subHist.append([posHistory[popSize - f - 1][runDuration - maxPlot + i] for i in range(0,maxPlot)])
    plt.plot(subHist[f],'ro')
plt.title('position of fishes')
plt.show()
