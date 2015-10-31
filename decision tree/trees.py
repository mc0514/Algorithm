import operator
from math import log
def calcShannonEnt(dataset):
    numEntries=len(dataset)
    lableCounts={}
    for featVec in dataset:
        currentLable=featVec[-1]
        if currentLable not in lableCounts.keys():
            lableCounts[currentLable]=0
        lableCounts[currentLable]+=1
    shannonEnt=0.0
    for key in lableCounts:
        prob=float(lableCounts[key])/numEntries
        shannonEnt-=prob*log(prob,2)
    return shannonEnt

def creatDataSet():
    dataSet=[
        [1,1,'yes'],
        [1,1,'yes'],
        [1,0,'no'],
        [0,1,'no'],
        [0,1,'no']
        ]
    labels=['no surfacing','flippers']
    return dataSet,labels

def splitDataSet(dataset,axis,value):
    retDataSet=[]
    for featVec in dataset:
        if(featVec[axis]==value):
            reducedFeatVec=featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet


def chooseBestFeatureToSplit(dataset):
    numFeatures=len(dataset[0])-1
    bestEntropy=calcShannonEnt(dataset)
    bestInfoGain=0.0;bestFeature=-1
    
    for i in range(numFeatures):
        featList=[example[i] for example in dataset]
        uniqueVals=set(featList)
        newEntropy=0.0
        for value in uniqueVals:
            subDataSet=splitDataSet(dataset,i,value)
            prob=len(subDataSet)/float(len(dataset))
            newEntropy+=prob*calcShannonEnt(subDataSet)
        infoGain=bestEntropy-newEntropy
        if(infoGain>bestInfoGain):
            bestInfoGain=infoGain
            bestFeature=i
    return bestFeature



def majorityCnt(classList):
    classCount={}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote]=0
        classCount[vote]+=1
    sortedClassCount=sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet,labels):
    classList=[example[-1] for example in dataSet]
    if classList.count(classList[0])==len(classList):
        return classList[0]
    if len(dataSet[0])==1:
        return majorityCnt(classList)
    bestFeat=chooseBestFeatureToSplit(dataSet)
    print bestFeat
    bestFeatLabel=labels[bestFeat]
    myTree={bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues=[example[bestFeat] for example in dataSet]
    uniqueVals=set(featValues)
    for value in uniqueVals:
        subLabels=labels[:]
        myTree[bestFeatLabel][value]=createTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    return myTree
        


#*************************************#
testDataSet,testLables=creatDataSet()
print testDataSet
print testLables
testMyTree=createTree(testDataSet,testLables)
print testMyTree
#testShannonEnt=calcShannonEnt(testDataSet)
#testsplitDataSet=splitDataSet(testDataSet,0,1)
#testBestFeature=chooseBestFeatureToSplit(testDataSet)
#print u'shannon entries value:%f' %testShannonEnt
#print 'split dataset:'
#print testsplitDataSet
#print u'Best Feature is: %d' %testBestFeature
