import math

def smoothCurve(curve,windowsSize = -1):
    if windowsSize == -1:
        windowsSize = math.ceil(len(curve) /100)
    if curve == []:
        return []
    res=[]
    for j in range(math.ceil(len(curve)/windowsSize)):
        res.append(0)
        k = 0
        for i in range(windowsSize):
            if i+j*windowsSize < len(curve): 
                k = k + 1
                res[j] = res[j] + curve[i+j * windowsSize]
            else :
                break
        if k==0:
            res[j] = 0
        else:
            res[j] =res[j] / k
    return res

def smoothSparseCurve(curve,windowsSize=-1):
    if windowsSize == -1:
        windowsSize = math.ceil(len(curve) /100)
    if curve == []:
        return []
    res=[]
    for j in range(math.floor(len(curve)/windowsSize)):
        res.append(0)
        numberOfPoint =0
        for i in range(windowsSize):
            if i+j*windowsSize < len(curve): 
                p=curve[i+j * windowsSize]
                if p != 0:
                    res[j] = res[j] + p
                    numberOfPoint = numberOfPoint + 1
            else:
                break
        if numberOfPoint == 0:
            res[j]=res[j-1]
        else :
            res[j] =res[j] / numberOfPoint
    return res
