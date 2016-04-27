from fish import *
popSize = 5
runDuration = 500
ringSize = 19
reward=10
punition=-2
previousKnowledge={}
def rewards(state):
    near,left,right = state
    if near > 2:
        return reward
    elif near < 2:
        return punition
    else :
        return 0
def printHistory(pop):
    globalHistory=[]
    emptyBoard={}
    for i in range(ringSize):
        emptyBoard['Pos'+str(i)]=[]
    for i in range(runDuration):
        globalHistory.append(emptyBoard.copy())
    for fish in pop:
        print(len(fish.posHistory))
        for i in range(len(fish.posHistory)):
            globalHistory[i]['Pos'+str(fish.posHistory[i])].append(fish.idFish)
   

pop = []

for i in range(popSize):
    pop.append(Fish(newID(),ringSize,[],rewards,previousKnowledge.copy()))
for f in pop :
    f.pos = random.randint(0, ringSize -1)
    f.vision = pop
for t in range(runDuration) :
    for f in pop :
        f.decide()
    for f in pop :
        f.act()
for t in range(runDuration) :
    for f in pop:
        if f.lastReward == reward:
            print(f.getState())
            f.eligibilityTrace=[]
            f.pos=random.randint(0,ringSize-1)
            f.timeToGoalHistory.append(f.timeToGoal)
            f.timeToGoal = 0
        else :
            f.timeToGoal=f.timeToGoal + 1
for f in pop :
    print(f.idFish)
    print(f.timeToGoalHistory)
#    print(f.stateHistory)
    for key,value in f.Q.items():
        print(key)
        print(value)
#printHistory(pop)
