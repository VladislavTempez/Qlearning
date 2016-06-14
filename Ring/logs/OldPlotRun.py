import matplotlib.pyplot as plt
import math
import pickle
from sys import argv

def smoothCurve(curve,windowsSize = -1):
    if windowsSize == -1:
        windowsSize = math.ceil(len(curve) /100)
    if curve == []:
        return []
    res=[]
    for j in range(math.ceil(len(curve)/windowsSize)):
        res.append(0)
        for i in range(windowsSize):
            if i+j*windowsSize < len(curve): 
                res[j] = res[j] + curve[i+j * windowsSize]
            else :
                break
        res[j] =res[j] / windowsSize
    return res
def smoothSparseCurve(curve,windowsSize=-1):
    if windowsSize == -1:
        windowsSize = math.ceil(len(curve) /100)
    if curve == []:
        return []
    res=[]
    for j in range(math.floor(len(curve)/windowsSize)):
        res.append(0)
        numberOfPoint =0
        for i in range(windowsSize):
            if i+j*windowsSize < len(curve): 
                p=curve[i+j * windowsSize]
                if p != 0:
                    res[j] = res[j] + p
                    numberOfPoint = numberOfPoint + 1
            else:
                break
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

infos = infos.split('\n')
runDuration = int(infos[0].split(':')[1])
print('Run Duration :',runDuration)
popSize = int(infos[1].split(':')[1])
print('Population Size :',popSize)
learnersNumber = int(infos[5].split(':')[1])
print('Learners :',learnersNumber)
try:
    learntNumber = int(infos[6].split(':')[1])
except IndexError:
    learntNumber = 0
print('Learnt :',learntNumber)
adultsNumber = popSize-learnersNumber-learntNumber
print('Adults :',adultsNumber)
ringSize = float(infos[2].split(':')[1])
print('Ring Size :',ringSize)
decreasePoint = float(infos[3].split(':')[1])
decreaseValue = float(infos[4].split(':')[1])
print('At ',decreasePoint,' of the run, learning rate is ',decreaseValue)

if learnersNumber > 0 :
    joinGroupDateLearnersHist = pickle.load(logFile)
    timeInGroupLearnersHist = pickle.load(logFile)
if adultsNumber > 0:
    joinGroupDateAdultsHist = pickle.load(logFile)
    timeInGroupAdultsHist = pickle.load(logFile)
if learntNumber > 0:
    joinGroupDateLearntHist = pickle.load(logFile)
    timeInGroupLearntHist = pickle.load(logFile)

posHistoryA=[]
posHistoryL=[]
posHistoryLearnt=[]
maxPlot=min(runDuration, int(ringSize) * 10 )
for f in range(adultsNumber):
    posHistoryA.append(pickle.load(logFile))
for f in range(learnersNumber):
    posHistoryL.append(pickle.load(logFile))
for f in range(learntNumber):
    posHistoryLearnt.append(pickle.load(logFile))
logFile.close()

plt.plot(smoothCurve(timeOfReward))
plt.title('average number of rewards')
plt.show()
for i in range(learnersNumber):
    plt.plot(smoothCurve([t[i] for t in joinGroupDateLearnersHist]),color = 'r')

for i in range(learntNumber):
    plt.plot(smoothCurve([t[i] for t in joinGroupDateLearntHist]),color = 'g')
try:
    plt.plot(smoothCurve([max(t[i] for i in range(adultsNumber)) for t in joinGroupDateAdultsHist]),color = 'b')
except ValueError:
    print('No Adults')
plt.title('date of joinging the group, in red for learners, in green for old fishes and in blue for last of non learners')
plt.show()
for i in range(learnersNumber):
    plt.plot(smoothCurve([t[i] for t in timeInGroupLearnersHist]),color = 'r')
for i in range(learntNumber):
    plt.plot(smoothCurve([t[i] for t in timeInGroupLearntHist]),color = 'g')
try:
    plt.plot(smoothCurve([min(t[i] for i in range(adultsNumber)) for t in timeInGroupAdultsHist]),color = 'b')
except ValueError:
    print('No Adults')
plt.title('time in the group, in red for learners, in green for old fishes and in blue for min in non learners')
plt.show()
plt.plot(smoothSparseCurve(averageDistanceSinceGoal))
plt.title('average distance since goal')
plt.show()
subHist=[]
for f in range(adultsNumber):
    plt.plot(posHistoryA[f][ 0 : maxPlot - 1])
for f in range(learnersNumber):
    plt.plot(posHistoryL[f][0 : maxPlot : - 1],'ro',color='r')
for f in range(learntNumber):
    plt.plot(posHistoryLearnt[f][0 : maxPlot - 1],'ro',color='g')

plt.xlabel('Time in iterations')
plt.ylabel('Position of the fishes on the ring')
#plt.title('position of fishes (learners in red, old fishes in green) for the '+str(maxPlot)+' last steps')
plt.show()
