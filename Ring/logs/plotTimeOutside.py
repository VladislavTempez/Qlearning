from loadLogs import *
from timeOutsideGroupPlotFunction import *
from sys import argv
if len(argv) > 1:
    script, filename = argv
else:
    filename='logsLoc'

logsLocFile=open(filename)
logsFileName=logsLocFile.read().splitlines()[0]
logsLocFile.close()
infos,timeOfReward,joinGroupDateLearnersHist,timeInGroupLearnersHist,joinGroupDateAdultsHist,timeInGroupAdultsHist,posHistoryA,posHistoryL = load(logsFileName)

plotTimeOutGroup(infos,timeInGroupLearnersHist,timeInGroupAdultsHist,joinGroupDateLearnersHist,joinGroupDateAdultsHist)

