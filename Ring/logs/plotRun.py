from loadLogs import *
from positionPlotFunction import *
from computableMetrics import *
from firstTimeInGroupPlotFunction import *
from neighbourNumberPlotFunction import *
from sys import argv
if len(argv) > 1:
    script, filename = argv
else:
    filename='logsLoc'

logsLocFile=open(filename)
logsFileName=logsLocFile.read().splitlines()[0]
logsLocFile.close()

infos,sumSquaredDistanceHist,firstTimeInGroupHist,maxNumberOfNeighbour,minNumberOfNeighbour,posHistoryA,posHistoryL = load(logsFileName)

plotFirstTimeInGroup(infos,firstTimeInGroupHist)

plotNumberOfNeighbour(infos,minNumberOfNeighbour,maxNumberOfNeighbour)

#plotMetrics(infos,posHistoryA,posHistoryL)

plotPos(infos,posHistoryA,posHistoryL)
