import matplotlib.pyplot as plt
import pickle
from sys import argv
script, filename = argv
logFile = open(filename,'rb')
infos = pickle.load(logFile)
infos = infos.split('\n')
age = int(infos[0].split(':')[1])
print(age)
Q=pickle.load(logFile)
posHistory=pickle.load(logFile)
dateOfReward=pickle.load(logFile)
logFile.close()
print(Q)
#plt.plot(posHistory)
#plt.show()
#plt.plot(dateOfReward)
#plt.show()