################################################
#                 Dependencies                 #
################################################

import math
import random
#To date the end of the learnin phase
import time
#To write logs
import pickle 

################################################
#                 Useful values                #
################################################
#Initialize random seed for random number generator
random.seed()

#number of representants for fishes in sectors
numberOfRepresentant = 10

#Initialize id for fishes
fishId = 0

#From a number vector a_i gives the vector b were b_i is the rank of a_i in a.
def rank(valueList):
    indexList = [(valueList[i],i) for i in range(len(valueList))]
    indexList.sort()
    return [b for (a,b) in indexList]

#Global ID generator
def newID():
    global fishId
    newId=fishId
    fishId = fishId + 1
    return newId

#Defining the different relative sectors and returns a vector where each positionhas a corresponding sector.
def sectorInit(self) :

#limits of sectors :
    lim1 = self.criticalSize + 1 #strict limit, lim1 in the first index to be outside sector 1
    lim2 = 3 * self.criticalSize + 1 + math.ceil((self.ringSize - 13)/5)
    lim3 = 5 * self.criticalSize + 1 + math.ceil((self.ringSize - 13)/3)
    limInf = math.ceil(self.ringSize/2) + 1  

    sectors = ['far' for i in range(self.ringSize)] #by default a position is in 'far' sector

#Checking that the limits are not larger than the ring
    if lim1 > limInf :
        lim1 = limInf
    if lim2 > limInf :
        lim2 = limInf
    if lim3 > limInf :
        lim3 = limInf

#Assigning the correct sector to each position, starting by the farther sectors
    for i in range(lim2, lim3):
        sectors[i]='farLeft'
        sectors[-i]='farRight'
    for i in range(lim1 ,lim2):
        sectors[i]='nearLeft'
        sectors[-i]='nearRight'
    for i in range(lim1):
        sectors[i] = 'central'
        sectors[-i] = 'central'
    
    return sectors

#Returns the sector in which is a fish relatively to the agent.
def getSector(self,fish):
    relativePos = (fish.pos - self.pos) % self.ringSize
    return self.sectors[relativePos]

#Return the state of the environment as the agent sees it.
def getState(self):
    fishDistribution = [0 for i in self.sectorList]
    state = [0 for i in self.sectorList]
    popSize = len(self.vision)
    for fish in self.vision:
        fishSector = getSector(self,fish)
        fishDistribution[self.sectorList.index(fishSector)] = fishDistribution[self.sectorList.index(fishSector)] + 1
    fishDistribution = [j / popSize for j in fishDistribution]
    state = [math.floor(j*numberOfRepresentant) for j in fishDistribution]
    distributionRemaining = [fishDistribution[i] - state[i] for i in range(len(state))]
    rankedDistributionRemaining = rank(distributionRemaining)
    remainingRepresentant = numberOfRepresentant - sum(state)
    for i in range(remainingRepresentant):
        state[rankedDistributionRemaining[i]] = state[rankedDistributionRemaining[i]] + 1

    if sum(state) >  numberOfRepresentant:
        print('Error in selection of representants')
    return tuple(state)

def policy(self): 
    s = self.currentState
    r = random.random()
    if r < self.exploreRate : # taking one action at random to explore
        self.nextAction = random.choice(['left','right','dontMove'])
    else :
        if s in self.Q.keys():  # already a value known for this state and action 
            maxVal,maxAction = max((value,key) for key,value in self.Q[s].items())
            minVal,minAction = min((value,key) for key,value in self.Q[s].items())
            possibleActions = [key for key in self.Q[s].keys()]
            if maxVal == minVal: #all known actions are equivalent, choosing randomly
                self.nextAction = random.choice(possibleActions)
            else :
                self.nextAction = maxAction
        else : # nothing is known about this state, random decision
            self.Q[s] = {'left': 0, 'right': 0,'dontMove':0}
            self.nextAction = random.choice(['left','right','dontMove'])


def updateLearning(self,date):

    self.lastState = self.currentState
    self.currentState = self.getState(self)
    self.posHistory.append(self.pos)
    self.timeSinceReward = self.timeSinceReward + 1

    #updating eligibility trace
    if self.lastState in self.eligibilityTrace.keys():
        if self.lastAction in self.eligibilityTrace[self.lastState].keys():
            self.eligibilityTrace[self.lastState][self.lastAction] = self.eligibilityTrace[self.lastState][self.lastAction] + self.discountFactor**(-self.timeSinceReward)
        else :
            self.eligibilityTrace[self.lastState][self.lastAction] = self.discountFactor ** (- self.timeSinceReward)
    else :
        self.eligibilityTrace[self.lastState] = {self.lastAction : self.discountFactor ** (-self.timeSinceReward)}
    if self.exploreRateMutable:
        self.exploreRate = self.alpha / (self.alpha + self.age)
    if self.learningRateMutable:
        self.learningRate = self.alpha  / (2*self.alpha + 3*self.age)
    self.age = self.age + 1
    reward = self.rewards(self)
    self.lastReward = reward
    
    #updating Q
    if reward == 0:
        return
    else:
        for state,vTemp in self.eligibilityTrace.items():
            for action,value in vTemp.items():
                if state in self.Q.keys():
                    if action in self.Q[state].keys():
                        self.Q[state][action] = self.Q[state][action] * (1 - self.learningRate) + reward * value * self.discountFactor**(self.timeSinceReward) * self.learningRate
                    else :
                        self.Q[state][action] = reward * value * self.discountFactor ** (self.timeSinceReward) * self.learningRate
                else :
                    self.Q[state] = {action : reward * value * self.discountFactor ** (self.timeSinceReward) * self.learningRate}
        if reward > 0:
            self.dateOfReward.append(date)
        self.eligibilityTrace = {}
        self.timeSinceReward = 0

#Define the reward associated to each state
def rewards(penalty = -2, reward = 10, minSizeOfGroup = 3):
    def rewardFunction(self):
        state = self.currentState
        near = state[self.sectorList.index('central')]
        if near >= minSizeOfGroup: 
            return reward
        elif near < 2:
            return penalty
        else :
            return 0
    return rewardFunction

class Fish:
#Initialization
    def __init__(self,
                idFish,
                ringSize,
                rewards = rewards,
                vision=[],
                previousKnowledge = {},
                pos = 0,
                learningRate = 1,
                exploreRate = 1,
                criticalSize = 1,
                alpha = 1,
                getState = getState,
                policy = policy,
                update = updateLearning,
                ):

        self.idFish = idFish
        self.ringSize = ringSize
        self.criticalSize = criticalSize
        self.Q = previousKnowledge.copy()
        self.pos = pos
        self.vision = vision
        self.learningRate = learningRate
        self.exploreRate = exploreRate
        self.alpha = alpha
        self.discountFactor = 0.95
        self.speed = 1 
        self.rewards = rewards
        self.age = 0
        self.lastAction = None
        self.nextAction = None
        self.lastState = None
        self.currentState = None
        self.lastReward = 0
        self.getState = getState
        self.sectors = sectorInit(self)
        self.sectorList = [] 
        
#Defining the format of state representation, here its the sectors in order
        for j in self.sectors:
            if not j in self.sectorList:
                self.sectorList.append(j)

        self.policy = policy
        self.update = update
        self.states = []
        self.eligibilityTrace = {}
        self.posHistory = []
        self.dateOfReward=[]
        self.timeSinceReward = 0
        self.exploreRateMutable = True
        self.learningRateMutable = True
        self.joinGroupDate = 0 
        self.timeInGroup = 0

        def goLeft(self):
            self.pos = (self.pos + self.speed)% self.ringSize
            return

        def goRight(self):
            self.pos = (self.pos - self.speed)% self.ringSize
            return

        def dontMove(self):
            return

        self.actions={'left' : goLeft,'right' : goRight, 'dontMove' : dontMove}

    def distance(self,fish):
        return min((self.pos - fish. pos) % self.ringSize ,(fish.pos - self. pos) % self.ringSize)

    def act(self) :
        self.lastAction = self.nextAction
        self.actions[self.nextAction](self)
        self.nextAction = None

    def genLogs(self,idFile,timeNow):
        title='Fish'+str(self.idFish)
        title = title + '-' + timeNow + '-' + str(idFile)
        logFile=open('./logs/Fish/'+ title +'.log','wb')
        infos = '' 
        infos = infos + 'age:' + str(self.age) + '\n'
        pickle.dump(infos,logFile,2)
        pickle.dump(self.Q,logFile,2)
        pickle.dump(self.posHistory,logFile,2)
        pickle.dump(self.dateOfReward,logFile,2)
        logFile.close()
        return

    def __str__(self):
        return str(self.pos)

    def __repr__(self):
        return str(self.idFish)

    def __eq__(self,fish):
        return self.idFish==fish.idFish

    def __ne__(self,fish):
        return self.idFish!=fish.idFish

    def __lt__(self,fish):
        return self.idFish<fish.idFish
