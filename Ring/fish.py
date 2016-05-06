################################################
#                 Dependencies                 #
################################################

import math
import random
import time
import json

################################################
#                 Useful values                #
################################################

fishId=0
def newID():
    global fishId
    newId=fishId
    fishId = fishId + 1
    return newId

def getState(self):
    near = 0
    left = 0
    right = 0
    for fish in self.vision:
        if self.distance(fish) <= self.criticalSize:
            near = near + 2
        elif fish.pos - self.pos > self.ringSize / 2 :
            left = left + 1
        else :
            right = right + 1
    return (near,left,right)

random.seed()

class Fish:
    def __init__(self, idFish, ringSize, rewards, vision=[], getState =
            getState, previousKnowledge = {}, pos = 0, learningRate = 1,
            exploreRate = 1, criticalSize = 2, learningDecreaseRate = 1, alpha =
            10**100):
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
        self.memoryDecrease = 0.95
        self.speed = 1 
        self.rewards = rewards
        self.age = 0
        self.lastAction = None
        self.nextAction = None
        self.lastState = None
        self.currentState = None
        self.lastReward = 0
        self.getState = getState
        self.states = []
        self.eligibilityTrace = []
        self.posHistory = []
        self.stateHistory = []
        self.dateOfResetHistory = []
        self.moveStock = 0
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
        self.actions={'left' : goLeft,'right' : goRight, 'dontMove' :dontMove}

    def distance(self,fish):
        return min((self.pos - fish. pos) % self.ringSize ,(fish.pos - self. pos) % self.ringSize)


    def decide(self):
        s = self.currentState
        r = random.random()
        if r < self.exploreRate : # taking one action at random to explore
            self.nextAction = random.choice(['left','right','dontMove'])
        else : # already a value known for this state and action
            if s in self.Q.keys(): 
                maxVal,maxAction = max((value,key) for key,value in self.Q[s].items())
                minVal,minAction = min((value,key) for key,value in self.Q[s].items())
                possibleActions = [key for key in self.Q[s].keys()]
                if maxVal == minVal: #all known actions are equivalent, choosing randomly
                    self.nextAction = random.choice(possibleActions)
                else :
                    self.nextAction = maxAction
            else : # nothing is known about this state, random decision
                self.nextAction = random.choice(['left','right','dontMove'])

    def update(self):
        self.lastState=self.currentState
        self.currentState=self.getState(self)
        self.stateHistory.append(self.currentState)
        self.posHistory.append(self.pos)
        self.eligibilityTrace = [(s,a,self.memoryDecrease * v) for (s,a,v) in self.eligibilityTrace]
        if self.lastAction != None: #at the start, there is no action to add in eligibility trace
            self.eligibilityTrace.append((self.lastState,self.lastAction,1))
        self.exploreRate = self.alpha / (self.alpha + self.age)
        self.age = self.age + 1
        self.learningRate = self.learningRate * self.learningDecreaseRate
        reward = self.rewards(self.currentState)
        self.lastReward = reward
        if reward == 0:
            return
        else:
            for (s,a,v) in self.eligibilityTrace:
                if s in self.Q.keys():
                    if a in self.Q[s].keys():
                        self.Q[s][a] = self.Q[s][a] * (1 - self.learningRate) + reward * v * self.learningRate
                    else :
                        self.Q[s][a] = reward * v * self.learningRate
                else :
                    self.Q[s]={a : reward * v * self.learningRate}


    def act(self) :
        self.lastAction = self.nextAction
        self.actions[self.nextAction](self)
        self.nextAction = None

    def genLogs(self):
        logs = {}
        logs['age'] = self.age
        logs['posHistory'] = self.posHistory
        logs['stateHistory'] = self.stateHistory
        logs['Q'] = [{str(k):v} for k,v in self.Q.items()] 
        logs['dateOfReset'] = self.dateOfResetHistory
        logsJson = json.dumps(logs)
        title='Fish'+str(self.idFish)
        date = time.time()
        idFile = math.ceil((date - math.ceil(date))*1000000) % 1000
        timeNow = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
        title = title + '-' + timeNow + '-' + str(idFile)
        logFile=open('./logs/'+ title +'.json','w')
        logFile.write(logsJson)
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
