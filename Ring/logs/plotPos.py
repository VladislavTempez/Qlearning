from loadLogs import *
from positionPlotFunction import *
from sys import argv
if len(argv) > 1:
    script, filename = argv
else:
    filename='logsLoc'

logsLocFile=open(filename)
logsFileName=logsLocFile.read().splitlines()[0]
logsLocFile.close()
infos,averageDistanceSinceGoal,timeOfReward,joinGroupDateLearnersHist,timeInGroupLearnersHist,joinGroupDateAdultsHist,timeInGroupAdultsHist,joinGroupDateLearntHist,timeInGroupLearntHist,posHistoryA,posHistoryL,posHistoryLearnt = load(logsFileName)

plotPos(infos,posHistoryA,posHistoryL,posHistoryLearnt)

