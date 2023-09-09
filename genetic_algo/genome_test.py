import json
import os
import random


def randHash() -> str:
    return "%016x" % random.getrandbits(64)

def generateNewGenome() :
    id = randHash()
    
    # update scores.json
    fl = open('scores.json' , 'r')
    scores = json.load(fl)
    fl.close()
    
    scores[id] = 0
    
    fl = open('scores.json' , 'w')
    json.dump(scores , fl)
    fl.close()
    
    # read parameters.json
    
    fl = open('parameters.json' , 'r');
    parameters = json.load(fl)
    fl.close()
    
    # create genome{id}.json
    
    data = {}
    for x in parameters :
        mn = parameters[x]['min']
        mx = parameters[x]['max']
        data[x] = random.uniform(mn , mx)
    
    fl = open("genomes/{}.json".format( id) , "w")
    json.dump(data , fl)
    fl.close()

generateNewGenome()