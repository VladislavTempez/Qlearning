from envND import *

def binomial(j,n):
	if j > n :
		return 0
	else :
		return math.factorial(n)/(math.factorial(j)*math.factorial(n-j))

fishId=0
def newID():
	global fishId
	newId=fishId
	fishId = fishId + 1
	return newId

def placeFishes(dim,sparsity,fishes):
	random.shuffle(fishes)
	k=len(fishes)
	distance=0
	choices=1
	while(k>choices):
		distance=distance+1
		choices=choices+sum(binomial(i,dim)*math.floor(i**(distance-i))*2**i for i in range(1,distance+1))
	for fish in fishes:
		fish.pos=[random.randint(-distance,distance)*sparsity for j in range(dim)]
