import math
import random

fishId=0
def newID():
    global fishId
    newId=fishId
    fishId = fishId + 1
    return newId
random.seed()
class Fish:
    def __init__(self,idFish,ringSize,vision,rewards,previousKnowledge  ,pos = 0,learningRate = 0.2,exploreRate = 0.1):
        self.idFish = idFish
        self.ringSize = ringSize
        self.Q = previousKnowledge
        self.pos = pos
        self.posHistory=[]
        self.stateHistory=[]
        self.vision=vision
        self.learningRate = learningRate
        self.exploreRate = exploreRate
        self.eligibilityTrace = []
        self.age = 0
        self.speed = 1
        self.lastAction = None
        self.nextAction = None
        self.states = []
        self.memoryDecrease = 0.9
        self.rewards = rewards
        self.lastReward = 0
        def goLeft(self):
            self.pos = (self.pos - 1)% self.ringSize
        def goRight(self):
            self.pos = (self.pos + 1)% self.ringSize
        def dontMove(self):
            return
        self.actions={'left' : goLeft,'right' : goRight, 'dontMove' :dontMove}
    def distance(self,fish):
        return min((self.pos - fish. pos) % self.ringSize ,(fish.pos - self. pos) % self.ringSize)
    def getState(self):
        near = 0
        left = 0
        right = 0
        for fish in self.vision:
            if self.distance(fish) <= 2:
                near = near + 1
            elif fish.pos - self.pos > self.ringSize / 2 :
                left = left + 1
            else :
                right = right + 1
        return (near,left,right)
    def decide(self):
        s=self.getState()
        r=random.random()
        if r < self.exploreRate :
            self.nextAction = random.choice(['left','right','dontMove'])
        else :
            if s in self.Q.keys():
                self.nextAction = max((value,key) for key,value in self.Q[s].items())[1]
            else :
                self.nextAction = random.choice(['left','right','dontMove'])

    def updateQ(self):
        state = self.getState()
        reward=self.rewards(state)
        if reward == 0:
            return
        self.lastReward=reward
        for (a,v) in self.eligibilityTrace:
            if state in self.Q.keys():
                if a in self.Q[state].keys():
                    self.Q[state][a] = self.Q[state][a]*self.memoryDecrease + reward*v*self.learningRate
                else :
                    self.Q[state][a] = reward * v * self.learningRate
            else :
                self.Q[state]={a : reward * v * self.learningRate}
    def act(self):
        self.actions[self.nextAction](self)
        self.lastAction=self.nextAction
        self.posHistory.append(self.pos)
        self.stateHistory.append(self.getState())
        newEligibilityTrace=[]
        for (a,v) in self.eligibilityTrace:
            newEligibilityTrace.append((a,v * self.memoryDecrease))
        self.eligibilityTrace.clear()
        self.eligibilityTrace = newEligibilityTrace
        self.eligibilityTrace.append((self.nextAction,1))
        self.updateQ()
    def __str__(self):
        return str(self.idFish)
    def __repr__(self):
        return str(self.idFish)
    def __eq__(self,fish):
        return self.idFish==fish.idFish
    def __ne__(self,fish):
        return self.idFish!=fish.idFish
    def __lt__(self,fish):
        return self.idFish<fish.idFish
