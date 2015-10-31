def loadDataSet():
    postingList=[
        ['my','dog','has','flea','problems','help','please'],
        ['maybe','not','take','him','to','dog','park','stupid'],
        ['my','dalmation','is','so','cute','I','love','him'],
        ['stop','posting','stupid','worthless','garbage'],
        ['mr','licks','ate','my','steak','now','to','stop','him'],
        ['quit','buying','worthless','dog','food','stupid']
        ]
    classVec=[0,10,1,0,1]
    return postingList,classVec

def createVocabList(dataSet):
    vocabSet=set([])
    for document in dataSet:
        vocabSet=vocabSet|set(document)
    return list(vocabSet)

def setOfWords2Vec(vocabList,inputSet):
    returnVec=[0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)]=1
        else:
            print "The word: %s is not in my vocabulary!"%word
    return returnVec


#*****************************************************#


listOPosts,listClasses=loadDataSet()
print listOPosts[3]
print "*******************************************"
myVocabList=createVocabList(listOPosts)
print myVocabList
print "*******************************************"
resultVec=setOfWords2Vec(myVocabList,listOPosts[0])
print resultVec
