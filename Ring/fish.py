###############################################
#                Dependencies                 #
###############################################

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
            near = near + 1
        elif fish.pos - self.pos > self.ringSize / 2 :
            left = left + 1
        else :
            right = right + 1
    return (near,left,right)

random.seed()

class Fish:
    def __init__(self, idFish, ringSize, rewards, vision=[], getState = getState, previousKnowledge = {}, pos = 0, learningRate = 1, exploreRate = 1, criticalSize = 2, learningDecreaseRate = 1, alpha = 10**10):
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
        self.discountFactor = 0.8
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
    def checkWhatHappens(self,action):
        if action == 'dontMove':
            return self.currentState
        else:
            if action == 'left' :
                self.actions['left'](self)
                resultingState = self.getState(self)
                self.actions['right'](self)
                self.moveStock = self.moveStock - 2* self.speed
                return resultingState
            else: #action == right
                self.actions['right'](self)
                resultingState = self.getState(self)
                self.actions['left'](self)
                self.moveStock = self.moveStock - 2* self.speed
                return resultingState


    def update(self):
        self.lastState = self.currentState
        self.currentState = self.getState(self)
        self.stateHistory.append(self.currentState)
        self.posHistory.append(self.pos)
        self.exploreRate = self.alpha / (self.alpha + self.age)
        self.age = self.age + 1
        self.learningRate = self.learningRate * self.learningDecreaseRate
        reward = self.rewards(self.currentState)
        self.lastReward = reward
        #Computing the maximum value neighbour   
        maxValue = 0
        for a in self.actions.keys():
            neighbourState = self.checkWhatHappens(a)
            try:
                neighbouringReward =  max(value for key,value in self.Q[neighbourState].items())
            except ValueError:
                neighbouringReward = 0
            except KeyError:
                neighbouringReward = 0
            if neighbouringReward > maxValue :
                maxValue = neighbouringReward
        if (self.currentState in self.Q.keys()):
            if (self.lastAction in self.Q[self.currentState].keys()):
                self.Q[self.currentState][self.lastAction] = self.Q[self.currentState][self.lastAction] * (1-self.learningRate) + self.learningRate * (reward + self.discountFactor * maxValue)
            else:
                self.Q[self.currentState][self.lastAction] = self.learningRate * (reward + self.discountFactor * maxValue)
        else :
            self.Q[self.currentState] = {self.lastAction : self.learningRate * (reward + self.discountFactor * maxValue)}
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
