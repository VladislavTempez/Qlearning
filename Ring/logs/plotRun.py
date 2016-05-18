import matplotlib.pyplot as plt
import pickle
from sys import argv
script, filename = argv
logFile = open(filename,'rb')
infos = pickle.load(logFile)
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
averageDistanceSinceGoal=pickle.load(logFile)
timeOfReward=pickle.load(logFile)
posHistory=[]
for f in range(popSize):
    posHistory.append(pickle.load(logFile))
logFile.close()
plt.plot(averageDistanceSinceGoal)
plt.plot(timeOfReward)
plt.show()
for f in range(popSize):
    plt.plot(posHistory[f])
plt.show()
