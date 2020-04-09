# -*- coding: utf-8 -*-
"""
@author: Sri Chaitra Kareddy
"""

def viterbiAlg(observationSeq, transitionProb, observationLikelihood, states):
    probabilitiesMat = []
    observationSeq_index = 0
    observationAtIndex = observationSeq[observationSeq_index]
    probForEachSeq = {}
    for state in states:
        probForEachSeq[state] = transitionProb[state]["start"] * observationLikelihood[observationAtIndex][state]
    probabilitiesMat.append(probForEachSeq) 
    final_POSTags = {}
    previousState = ""
    for index in range(1, len(observationSeq)+1):
        probForEachSeq = {}
        if index < len(observationSeq):
            observationAtIndex = observationSeq[index]
            for currState in states:
                maxProb = 0
                for prevState in states:
                    prob = transitionProb[currState][prevState] * observationLikelihood[observationAtIndex][currState] * probabilitiesMat[index-1][prevState]
                    if maxProb < prob:
                        maxProb = prob
                        previousState = prevState
                    probForEachSeq[currState] = maxProb
            probabilitiesMat.append(probForEachSeq)
            final_POSTags[observationSeq[index-1]] = previousState
        else:
            maxProb = 0
            previousState = ""
            for state in states:
                if maxProb < probabilitiesMat[index-1][state]:
                    maxProb = probabilitiesMat[index-1][state]
                    previousState = state
            probForEachSeq["end"] = maxProb
            probabilitiesMat.append(probForEachSeq)
            final_POSTags[observationSeq[index-1]] = previousState
    #print(probabilitiesMat)
    print(final_POSTags)
                

transitionProb = {
        "NNP" :{"start": 0.2767, "NNP": 0.3777, "MD": 0.0008, "VB": 0.0322, "JJ": 0.0366, "NN": 0.0096, "RB": 0.0068, "DT":0.1147},
        "MD" : {"start": 0.0006, "NNP": 0.0110, "MD": 0.0002, "VB": 0.0005, "JJ": 0.0004, "NN": 0.0176, "RB": 0.0102, "DT":0.0021},
        "VB" : {"start": 0.0031, "NNP": 0.0009, "MD": 0.7968, "VB": 0.0050, "JJ": 0.0001, "NN": 0.0014, "RB": 0.1011, "DT":0.0002},
        "JJ" : {"start": 0.0453, "NNP": 0.0084, "MD": 0.0005, "VB": 0.0837, "JJ": 0.0733, "NN": 0.0086, "RB": 0.1012, "DT":0.2157},
        "NN" : {"start": 0.0449, "NNP": 0.0584, "MD": 0.0008, "VB": 0.0615, "JJ": 0.4509, "NN": 0.1216, "RB": 0.0120, "DT":0.4744},
        "RB" : {"start": 0.0510, "NNP": 0.0090, "MD": 0.1698, "VB": 0.0514, "JJ": 0.0036, "NN": 0.0177, "RB": 0.0728, "DT":0.0102},
        "DT" : {"start": 0.2026, "NNP": 0.0025, "MD": 0.0041, "VB": 0.2231, "JJ": 0.0036, "NN": 0.0068, "RB": 0.0479, "DT":0.0017}
}    

observationLikelihood = {
        "Janet": {"NNP": 0.000032, "MD": 0, "VB":0, "JJ": 0, "NN": 0, "RB": 0, "DT":0},
        "will": {"NNP": 0, "MD": 0.308431, "VB":0.000028, "JJ": 0, "NN": 0.000200, "RB": 0, "DT":0},
        "back": {"NNP": 0, "MD": 0, "VB":0.000672, "JJ": 0.000340, "NN": 0.000223, "RB": 0.010446, "DT":0},
        "the": {"NNP": 0.000048, "MD": 0, "VB":0, "JJ": 0, "NN": 0, "RB": 0, "DT":0.506099},
        "bill": {"NNP": 0, "MD": 0, "VB":0.000028, "JJ": 0, "NN": 0.002337, "RB": 0, "DT":0}
}

states =["NNP", "MD", "VB", "JJ", "NN", "RB", "DT"]
#inputStr = "Janet will back the bill"
inputStr = "will Janet back the bill"
#inputStr = "back the bill Janet will"
observationSeq = inputStr.split()
viterbiAlg(observationSeq, transitionProb, observationLikelihood, states)
