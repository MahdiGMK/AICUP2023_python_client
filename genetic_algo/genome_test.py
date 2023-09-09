import json
import os
import random


def randHash() -> str:
    return "%016x" % random.getrandbits(64)

def readScores() -> dict :
    fl = open('scores.json' , 'r')
    scores = json.load(fl)
    fl.close()
    return scores

def readParameters() -> dict :
    fl = open('parameters.json' , 'r')
    parameters = json.load(fl)
    fl.close()
    return parameters

def generateNewGenome() :
    id = randHash()
    
    # update scores.json
    scores = readScores()
    
    scores[id] = 0
    
    fl = open('scores.json' , 'w')
    json.dump(scores , fl)
    fl.close()
    
    # read parameters.json
    
    parameters = readParameters()
    
    # create genome{id}.json
    
    data = {}
    for x in parameters :
        mn = parameters[x]['min']
        mx = parameters[x]['max']
        data[x] = random.uniform(mn , mx)
    
    fl = open("genomes/{}.json".format( id) , "w")
    json.dump(data , fl)
    fl.close()
    

def resetGenomes() :
    scores = readScores()
    fl = open('scores{}.json'.format(scores['version']) , 'w')
    json.dump(scores , fl)
    fl.close()
    
    parameters = readParameters()
    
    scores = {'version':parameters['version']['min']}
    fl = open('scores.json' , 'w')
    json.dump(scores , fl)
    fl.close()

resetGenomes()