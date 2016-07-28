import matplotlib.pyplot as plt
from pylab import setp
import numpy as np
import statistics as stat

def boxPlot(infos,time,minNeighbour,maxNeighbour):
 
    [
            runDuration,
            popSize,
            ringSize,
            decreasePoint,
            decreaseValue,
            learnersNumber,
            adultsNumber,
            reward,
            penalty,
            minSizeOfGroup,
            minimumDistanceToBeInGroup,
            pointToStopExploration,
            cycleLength 
        ] = infos
    colors = ['white','white']
    data = [time]
    plot1 = plt.boxplot(data,               
                        widths = 0.3,       # width of the box
                        showmeans = True,
                        meanline=True,
                        positions = [1],
                        patch_artist = True)  # enable further customizatons

    for patch, color in zip(plot1['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_edgecolor('black')

    plt.setp(plot1['whiskers'],     # customise whisker appearence
             color='Black',   # whisker colour
             linewidth=1.0)         # whisker thickness

    plt.setp(plot1['caps'],         # customize lines at the end of whiskers 
             color='Black',   # cap colour
             linewidth=1.0)         # cap thickness

    plt.setp(plot1['fliers'],       # customize marks for extreme values
             color='Black',        # set mark colour
             marker='o',            # maker shape
             markersize=0)         # marker size

    plt.setp(plot1['medians'],      # customize median lines
             color='Black',        # line colour
             linestyle='-.',
             linewidth=1.5)         # line thickness

    plt.setp(plot1['means'],      # customize median lines
             color='Black',        # line colour
             linestyle='--',
             linewidth=1.5)         # line thickness

    for patch, color in zip(plot1['boxes'], colors):
        patch.set_facecolor(color)
    curr_axes = plt.gca()
    curr_axes.axes.get_xaxis().set_visible(False)
    print('mean:',stat.mean(time),'median:',stat.median(time),'std',stat.pstdev(time))

    plt.show()

    data = [[10*j for j in maxNeighbour],[10*i for i in minNeighbour]]
    plot2 = plt.boxplot(data,               
                        widths = 0.3,       # width of the box
                        showmeans = True,
                        meanline=True,
                        positions = [1,1.5],
                        patch_artist = True)  # enable further customizatons

    for patch, color in zip(plot2['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_edgecolor('black')

    plt.setp(plot2['whiskers'],     # customise whisker appearence
             color='Black',   # whisker colour
             linewidth=1.0)         # whisker thickness

    plt.setp(plot2['caps'],         # customize lines at the end of whiskers 
             color='Black',   # cap colour
             linewidth=1.0)         # cap thickness

    plt.setp(plot2['fliers'],       # customize marks for extreme values
             color='Black',        # set mark colour
             marker='o',            # maker shape
             markersize=0)         # marker size

    plt.setp(plot2['medians'],      # customize median lines
             color='Black',        # line colour
             linestyle='-.',
             linewidth=1.5)         # line thickness

    plt.setp(plot2['means'],      # customize median lines
             color='Black',        # line colour
             linestyle='--',
             linewidth=1.5)         # line thickness

    curr_axes = plt.gca()
    curr_axes.axes.get_xaxis().set_visible(False)
    print('Max: mean:',stat.mean(maxNeighbour),'median:',stat.median(maxNeighbour),'std',stat.pstdev(maxNeighbour))
    print('Min: mean:',stat.mean(minNeighbour),'median:',stat.median(minNeighbour),'std',stat.pstdev(minNeighbour))
    plt.show()
    return
