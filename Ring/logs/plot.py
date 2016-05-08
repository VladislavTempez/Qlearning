import matplotlib.pyplot as plt
from sys import argv
script, filename = argv
logFile = open(filename,'r')
lines = logFile.readlines()
logFile.close()
runDLine = lines[0].split()
runDuration = int(runDLine[1])
print(runDuration)
popSizeLine = lines[1].split()
popSize = int(popSizeLine[1])
print(popSize)
ringSizeLine = lines[2].split()
ringSize = int(ringSizeLine[1])
print(ringSize)
decreasePointLine = lines[3].split()
decreasePoint = float(decreasePointLine[1])
print(decreasePoint)
decreaseValueLine = lines[4].split()
decreaseValue = float(decreaseValueLine[1])
print(decreaseValue)
averageDistanceSinceGoal = [float(d) for d in lines[6].replace('[','').replace(']','').split(',')]
averageDistanceWhenReachingGoal = [float(d) for d in lines[8].replace('[','').replace(']','').split(',')]

plt.plot(averageDistanceWhenReachingGoal)
plt.show()
plt.plot(averageDistanceSinceGoal)
plt.show()
