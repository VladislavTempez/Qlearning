from fish import *
popSize = 5
runDuration = 500
ringSize = 19
reward=100
punition=-2
previousKnowledge={}
def rewards(state):
    near,left,right = state
    if near > 2:
        return reward
    elif near < 2:
        return -punition
    else :
        return 0

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
    for f in pop:
        if f.lastReward == reward:
            f.eligibilityTrace=[]
            f.pos=random.randint(0,ringSize-1)
for f in pop :
    print(f.idFish)
    print(f.stateHistory)
    for key,value in f.Q.items():
        print(key)
        print(value)
