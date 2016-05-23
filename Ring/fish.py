################################################
#                 Dependencies                 #
################################################

import math
import random
import time
import pickle 

################################################
#                 Useful values                #
################################################

fishId=0
def newID():
    global fishId
    newId=fishId
    fishId = fishId + 1
    return newId

#defining the different relative sectors

def sectorInit(self) :
    #limits of sectors :
    lim1 = self.criticalSize + 1 #strict limit, lim1 in the first index to be outside sector 1
    lim2 = 3 * self.criticalSize + 1 + math.floor(self.ringSize / 5)
    lim3 = 6 * self.criticalSize +1 + math.floor(self.ringSize /2)
    limInf=math.ceil(self.ringSize/2) + 1  
    sectors = ['far' for i in range(self.ringSize)]
#checking that the limits are not larger than the ring
    if lim1 > limInf :
        lim1 = limInf
    if lim2 > limInf :
        lim2 = limInf
    if lim3 > limInf :
        lim3 = limInf
    for i in range(lim3,limInf):
        sectors[i] = 'far'
        sectors[-i] = 'far'
    for i in range(lim2, lim3):
        sectors[i]='rightFar'
        sectors[-i]='leftFar'
    for i in range(lim1 ,lim2):
        sectors[i]='rightNear'
        sectors[-i]='leftNear'
    for i in range(lim1):
        sectors[i] = 'near'
        sectors[-i] = 'near'
    #giving direction to the defined sectors
    directions = {'near' :  'dontMove', 'rightNear' : 'right', 'rightFar' :
            'right', 'leftFar' : 'left', 'leftNear' : 'left' }
    return sectors,directions

def getSector(self,fish):
    relativePos = (fish.pos - self.pos) % self.ringSize
    return self.sectors[relativePos]

def getState(self):
    state=[0 for i in self.sectorList]
    for fish in self.vision:
        fishSector = getSector(self,fish)
        state[self.sectorList.index(fishSector)] = state[self.sectorList.index(fishSector)] + 1
    return tuple(state)

def decideLearning(self):
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
            self.nextAction = random.choice(['left','right','dontMove'])

def decideNoLearning(self):
    s=self.currentState
    maxSize=max(s) #detecting the larger group
    if maxSize == s[self.sectorList.index('near')]: #if it's optimal to not move, don't move
        self.nextAction = random.choice(['dontMove'])
    else :
        sectorToGo=self.sectorList[s.index(maxSize)] #getting the sector in which the larger group is
        if sectorToGo == 'far':
            self.nextAction = random.choice(['left','right','dontMove'])
        else:
            self.nextAction = self.directions[sectorToGo]

random.seed()

def updateLearning(self):
    self.lastState = self.currentState
    self.currentState = self.getState(self)
    self.posHistory.append(self.pos)
    self.timeSinceReward = self.timeSinceReward + 1
    #updating eliginility trace
    if self.lastState in self.eligibilityTrace.keys():
        if self.lastAction in self.eligibilityTrace[self.lastState].keys():
            self.eligibilityTrace[self.lastState][self.lastAction] = self.eligibilityTrace[self.lastState][self.lastAction] + self.discountFactor**(-self.timeSinceReward)
        else :
            self.eligibilityTrace[self.lastState][self.lastAction] = self.discountFactor ** (- self.timeSinceReward)
    else :
        self.eligibilityTrace[self.lastState] = {self.lastAction : self.discountFactor ** (-self.timeSinceReward)}

    self.exploreRate = self.alpha / (self.alpha + self.age)
    self.age = self.age + 1
    self.learningRate = self.alpha  / (self.alpha +self.age)
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
            self.moveStock = 0
            self.dateOfReward.append(self.age)
        self.eligibilityTrace = {}
        self.timeSinceReward = 0

def updateNoLearning(self):
    self.lastState = self.currentState
    self.currentState = self.getState(self)
    self.posHistory.append(self.pos)
    self.age = self.age + 1

def rewards(punition = -2, reward = 10, minSizeOfGroup = 3):
    def res(self):
        state = self.currentState
        near = state[self.sectorList.index('near')]
        if near >= minSizeOfGroup: 
            return reward
        elif near < 2:
            return punition
        else :
            return 0
    return res

class Fish:
    def __init__(self,
                idFish,
                ringSize,
                rewards = rewards,
                vision=[],
                previousKnowledge = {},
                pos = 0,
                learningRate = 1,
                exploreRate = 1,
                criticalSize = 2,
                learningDecreaseRate = 0.9,
                alpha = 10**20,
                learning = True,
                getState = getState,
                decide = decideLearning,
                update = updateLearning,
                ):
        self.idFish = idFish
        self.ringSize = ringSize
        self.criticalSize = criticalSize
        self.Q = previousKnowledge.copy()
        self.pos = pos
        self.vision = vision
        self.learningRate = learningRate
        self.learningDecreaseRate = learningDecreaseRate
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
        self.sectors,self.directions = sectorInit(self)
        self.sectorList = list(set(self.sectors))
        self.decide = decide
        self.update = update
        self.states = []
        self.eligibilityTrace = {}
        self.posHistory = []
        self.dateOfReward=[]
        self.timeSinceReward = 0
        self.moveStock = 0
        self.learning = learning
        if not self.learning:
            self.update = updateNoLearning
            self.decide = decideNoLearning
            self.exploreRate = 0
            self.discountFactor = 0
        def goLeft(self):
            self.pos = (self.pos - self.speed)% self.ringSize
            self.moveStock = self.moveStock + self.speed
            return
        def goRight(self):
            self.pos = (self.pos + self.speed)% self.ringSize
            self.moveStock = self.moveStock + self.speed
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

    def genLogs(self):
        title='Fish'+str(self.idFish)
        date = time.time()
        #unique file number
        idFile = math.ceil((date - math.ceil(date))*1000000) % 1000
        timeNow = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
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
