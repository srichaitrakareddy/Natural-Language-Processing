# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

unigramsWordcount = {}
NoSmoothingUnigramsProb = {}
totalDistinctWords = 0
numOfWordTokens = 0

def writeToFile(filename, Ngram):
    file = open(filename, 'w')
    file.write('{:<40s}{:<25s}{:<25s}'.format('Unigrams','count','Probability') + '\n')
    for k,v in Ngram.items():
        file.write('{:<40s}{:<25s}{:<25s}'.format(str(k),str(v[0]),str(v[1])) + '\n')
    file.close()
    
with open('../Downloads/NLP6320_POSTaggedTrainingSet.txt') as file: 
    for word in file.read().split():
        wordBase = word.split('_')
        word_lowerCase = wordBase[0].lower()
        if word_lowerCase not in unigramsWordcount:
            unigramsWordcount[word_lowerCase] = 1
        else:
            unigramsWordcount[word_lowerCase] += 1
        numOfWordTokens += 1;
    totalDistinctWords = len(unigramsWordcount)
    print(len(unigramsWordcount))
    print(numOfWordTokens)

    for k, v in unigramsWordcount.items():
        prob = v/numOfWordTokens
        NoSmoothingUnigramsProb[k] = v, prob
writeToFile("NoSmoothing_Unigrams.txt", NoSmoothingUnigramsProb)
file.close()


bigramWords = {}
NoSmoothingbigramProb = {}
bigramTotalWords = 0
with open('../Downloads/NLP6320_POSTaggedTrainingSet.txt') as file:    
    line = file.readline()
    while line:
        words = line.split()
        i = 0
        while i<len(words) - 1:          
            wordn = (words[i].split('_'))[0].lower()
            wordnminusone = (words[i+1].split('_'))[0].lower()
            if (wordn, wordnminusone) in bigramWords:
                bigramWords[(wordn, wordnminusone)] += 1
            else: 
                bigramWords[(wordn, wordnminusone)] = 1           
            i = i+1
            bigramTotalWords = bigramTotalWords + 1
        line = file.readline()
    for k, v in bigramWords.items():
        prob = v/ unigramsWordcount[k[0]]
        NoSmoothingbigramProb[k] = v, prob
    #print(NoSmoothingbigramProb)
writeToFile("NoSmoothing_bigrams.txt", NoSmoothingbigramProb)
file.close()

print("---")
print(bigramTotalWords)
print(len(bigramWords))



'''-----------------------------------------
***********Add one Smoothing*****************
-----------------------------------------'''

uingramsAddOneCountandProb = {}

for k, v in unigramsWordcount.items():
    smoothedCount = (v + 1)*(numOfWordTokens/(numOfWordTokens + totalDistinctWords))
    prob = (v + 1)/(numOfWordTokens + totalDistinctWords)
    uingramsAddOneCountandProb[k] = smoothedCount, prob
#print(uingramsAddOneCountandProb)
writeToFile("AddOneSmoothing_Unigrams.txt", uingramsAddOneCountandProb)
    
bigramsAddOneCountandProb = {}
for k, v in bigramWords.items():
    smoothedCount = (v + 1)*(bigramTotalWords/(bigramTotalWords + len(bigramWords)))
    prob = (v + 1)/ (unigramsWordcount[k[0]] + totalDistinctWords)
    bigramsAddOneCountandProb[k] = smoothedCount, prob
writeToFile("AddOneSmoothing_bigrams.txt", bigramsAddOneCountandProb)
# print(bigramsAddOneCountandProb)
   
'''--------------------------------------------------------------------
***********Good-Turing Discounting based Smoothing*****************
-----------------------------------------------------------------------'''

unigramsGTCount = {}

for k, v in unigramsWordcount.items():
    if v not in unigramsGTCount:
        unigramsGTCount[v] = (k,)
    else:
        unigramsGTCount[v] = unigramsGTCount[v] + (k,)
unigramsGTCount = sorted(unigramsGTCount.items())
#print(unigramsGTCount)       

unigramsGTCountandProb = {}
i = unigramsGTCount[0][0]
lastitemCt = unigramsGTCount[len(unigramsGTCount) -1][0]
while i<len(unigramsGTCount)-1:
    newCount = ((i+1) * len(unigramsGTCount[i+1][1])) / len(unigramsGTCount[i][1])
    prob = 0
    if newCount == 0:
        prob = len(unigramsGTCount[i+1][1]) / totalDistinctWords 
    else:
        prob = newCount / totalDistinctWords
    unigramsGTCountandProb[unigramsGTCount[i+1][1]] = newCount, prob
    i = i+1
#print(unigramsGTCountandProb)   

bigramsGTCount = {}
for k, v in bigramWords.items():
    if v not in bigramsGTCount:
        bigramsGTCount[v] = (k,)
    else:
        bigramsGTCount[v] = bigramsGTCount[v] + (k,)
bigramsGTCount = sorted(bigramsGTCount.items())
#print(bigramsGTCount)

bigramsGTCountandProb = {}
i = bigramsGTCount[0][0]
lastitemCt = bigramsGTCount[len(bigramsGTCount) -1][0]
print(i)
print(lastitemCt)
print(len(bigramsGTCount)-1)
while i<len(bigramsGTCount)-1:
    newCount = ((i+1) * len(bigramsGTCount[i+1][1])) / len(bigramsGTCount[i][1])
    prob = 0
    if newCount == 0:
        prob = len(bigramsGTCount[i+1][1]) / len(bigramWords)
    else:
        prob = newCount / len(bigramWords)
    bigramsGTCountandProb[bigramsGTCount[i+1][1]] = newCount, prob
    i = i+1
#print(bigramsGTCountandProb)


    