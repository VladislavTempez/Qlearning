from loadLogs import *
from joinGroupDatePlotFunction import *
from positionPlotFunction import *
from timeInGroupPlotFunction import *
from averageDistanceSinceGoalPlotFunction import *
from averageNumberOfRewardPlotFunction import *
from sys import argv
if len(argv) > 1:
    script, filename = argv
else:
    filename='logsLoc'

logsLocFile=open(filename)
logsFileName=logsLocFile.read().splitlines()[0]
logsLocFile.close()
infos,averageDistanceSinceGoal,timeOfReward,joinGroupDateLearnersHist,timeInGroupLearnersHist,joinGroupDateAdultsHist,timeInGroupAdultsHist,joinGroupDateLearntHist,timeInGroupLearntHist,posHistoryA,posHistoryL,posHistoryLearnt = load(logsFileName)

plotJoinGroup(infos,joinGroupDateAdultsHist,joinGroupDateLearnersHist,joinGroupDateLearntHist)

plotPos(infos,posHistoryA,posHistoryL,posHistoryLearnt)

plotTimeInGroup(infos,timeInGroupLearnersHist,timeInGroupLearntHist,timeInGroupAdultsHist)
learnersNumber = infos[2]
if learnersNumber > 0:
    plotAverageDistance(infos,averageDistanceSinceGoal)

    plotAverageReward(infos,timeOfReward)
