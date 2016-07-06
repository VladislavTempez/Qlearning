from loadLogs import *
from joinGroupDatePlotFunction import *
from positionPlotFunction import *
from timeInGroupPlotFunction import *
from timeOutsideGroupPlotFunction import *
from averageNumberOfRewardPlotFunction import *
from groupnessPlotFunction import *
from groupExistencePlotFunction import *
from computableMetrics import *
from sys import argv
if len(argv) > 1:
    script, filename = argv
else:
    filename='logsLoc'

logsLocFile=open(filename)
logsFileName=logsLocFile.read().splitlines()[0]
logsLocFile.close()
infos,timeOfReward,joinGroupDateLearnersHist,timeInGroupLearnersHist,joinGroupDateAdultsHist,timeInGroupAdultsHist,posHistoryA,posHistoryL = load(logsFileName)
plotMetrics(infos,posHistoryA,posHistoryL)

#plotJoinGroup(infos,joinGroupDateAdultsHist,joinGroupDateLearnersHist)

plotPos(infos,posHistoryA,posHistoryL)

#plotTimeInGroup(infos,timeInGroupLearnersHist,timeInGroupAdultsHist)

#plotTimeOutGroup(infos,timeInGroupLearnersHist,timeInGroupAdultsHist,joinGroupDateLearnersHist,joinGroupDateAdultsHist)

learnersNumber = infos[2]
#if learnersNumber > 0:
#    plotAverageReward(infos,timeOfReward)
