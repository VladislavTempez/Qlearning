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
    def __init__(self,idFish,ringSize,vision,rewards,previousKnowledge = {},pos
            = 0,learningRate = 0.3,exploreRate = 0.01):
        self.idFish = idFish
        self.ringSize = ringSize
        self.Q = previousKnowledge.copy()
        self.pos = pos
        self.vision = vision
        self.learningRate = learningRate
        self.exploreRate = exploreRate
        self.memoryDecrease = 0.9
        self.speed = 1
        self.rewards = rewards
        self.age = 0
        self.lastAction = None
        self.nextAction = None
        self.lastState = None
        self.currentState = None
        self.lastReward = 0
        self.states = []
        self.eligibilityTrace = []
        self.posHistory = []
        self.stateHistory = []
        self.timeToGoal = 0
        self.timeToGoalHistory = []
        def goLeft(self):
            self.pos = (self.pos - 1)% self.ringSize
            return
        def goRight(self):
            self.pos = (self.pos + 1)% self.ringSize
            return
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
            if self.distance(fish) <= 1:
                near = near + 1
            elif fish.pos - self.pos > self.ringSize / 2 :
                left = left + 1
            else :
                right = right + 1
        return (near,left,right)
    def decide(self):
        s=self.getState()
        r=random.random()
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
    def updateQ(self):
        reward=self.rewards(self.currentState)
        self.lastReward=reward
        self.timeToGoal=self.timeToGoal + 1
        if reward == 0:
            return
        else:
            for (s,a,v) in self.eligibilityTrace:
                if s in self.Q.keys():
                    if a in self.Q[s].keys():
                        self.Q[s][a] = self.Q[s][a]*(1-self.learningRate) + reward * v * self.learningRate
                    else :
                        self.Q[s][a] = reward * v * self.learningRate
                else :
                    self.Q[s]={a : reward * v * self.learningRate}
        if reward > 0:
            self.eligibilityTrace.clear()
            self.pos = random.randint(0,self.ringSize - 1)
            self.timeToGoalHistory.append(self.timeToGoal)
            self.timeToGoal = 0
        return
    def lookAround(self) :
        self.lastState=self.currentState
        self.currentState=self.getState()
        self.stateHistory.append(self.currentState)
        self.posHistory.append(self.pos)
        self.eligibilityTrace = [(s,a,self.memoryDecrease * v) for (s,a,v) in self.eligibilityTrace]
        if self.lastAction != None: #at the start, there is no action to add in eligibility trace
            self.eligibilityTrace.append((self.lastState,self.lastAction,1))
    def act(self) :
        self.lastAction = self.nextAction
        self.actions[self.nextAction](self)
        self.nextAction = None
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
