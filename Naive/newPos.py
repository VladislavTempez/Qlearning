import math

def binomial(j,n):
	if j > n :
		return 0
	else :
		return math.factorial(n)/(math.factorial(j)*math.factorial(n-j))

def newPos(dim,sparsity,k):
	currentPos=[0 for i in range(dim)]
	currentDimUsed=1
	currentDim=0
	posEnumerated=1
	distance=0
	choicesLeft=k
	if k==0:
		return currentPos
	while choicesLeft>posEnumerated: #computing the distance at which is the point
		distance=distance+1
		increment=sum(binomial(i,dim)*math.floor(i**(distance-i))*2**i for i in range(1,distance+1))
		posEnumerated=posEnumerated+increment
		print(posEnumerated,distance)
	choicesLeft=choicesLeft-increment
	vectorUsed=0
	posEnumerated=0
	increment=0
	while choicesLeft>posEnumerated:
		vectorUsed=vectorUsed+1
		increment=2**vectorUsed #each vector used has a non 0 component
		increment=increment*vectorUsed**(distance-vectorUsed) #the rest of the distance is freely shared between vectors
		posEnumerated=posEnumerated+increment
	maxValue=distance-vectorUsed #this is in addition to the value of one corresponding to the use of the vector
	choicesLeft=choicesLeft-posEnumerated-increment
	posEnumerated=0
	values=[1 for i in range(vectorUsed)]
#	for j in range(vectorUsed):
#		posEnumerated=0
#		leftMoves=distance-sum(x in values)
#		for i in range(leftMoves):
#			increment=(dim-j)*2*(leftMoves-i)**(vectorUsed-j)
#			posEnumerated=posEnumerated+increment
#			if posEnumerated>choicesLeft:
#				choicesLeft=choicesLeft-posEnumerated-increment
#				values[j]=leftMoves-i
#				break
#	posEnumerated=0
#	increment=0
	print(distance,vectorUsed)
newPos(3,5,6)
		

