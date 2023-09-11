import json
import os
import random

def numberInRange(min , max):
    if(min == max) : return min
    return random.uniform(min , max)

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

def readGenome(version , round , id) -> dict :
    fl = open('genomes/{}/{}/{}.json'.format(version , round , id) , 'r')
    genome = json.load(fl)
    fl.close()
    return genome
    
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
    
    version = parameters['version']['min']
    round = parameters['round']['min']
    
    # create genome{id}.json
    
    data = {}
    for x in parameters :
        mn = parameters[x]['min']
        mx = parameters[x]['max']
        data[x] = numberInRange(mn , mx)
    
    os.makedirs('genomes/{}/{}/'.format(version , round) ,exist_ok=True)
    fl = open('genomes/{}/{}/{}.json'.format(version , round , id) , "w")
    json.dump(data , fl)
    fl.close()
    

def resetGenomes() :
    scores = readScores()
    fl = open('scores{}_{}.json'.format(scores['version'] , scores['round']) , 'w')
    json.dump(scores , fl)
    fl.close()
    
    parameters = readParameters()
    
    scores = {'version':parameters['version']['min'] , 'round':parameters['round']['min']}
    fl = open('scores.json' , 'w')
    json.dump(scores , fl)
    fl.close()

def updateGenomes() :
    scores = readScores()
    parameters = readParameters()
    
    # take backup
    fl = open('scores{}_{}.json'.format(scores['version'] , scores['round']) , 'w')
    json.dump(scores , fl)
    fl.close()
    
    last_version = scores['version']
    last_round = scores['round']
    
    # update version and round
    version = scores['version'] = parameters['version']['min']
    round = scores['round'] = parameters['round']['min']
    fl = open('scores.json' , 'w')
    json.dump(scores , fl)
    fl.close()
    
    os.makedirs('genomes/{}/{}/'.format(version , round) , exist_ok=True)
    for id in scores :
        if(id == 'version' or id == 'round') :
            continue
        genome = readGenome(last_version , last_round , id)
        for p in parameters :
            mn = parameters[p]['min']
            mx = parameters[p]['max']
            
            if(genome.__contains__(p)) :
                if(genome[p] < mn) : genome[p] = mn
                if(genome[p] > mx) : genome[p] = mx
            else :
                genome[p] = numberInRange(mn , mx)
        
        fl = open('genomes/{}/{}/{}.json'.format(version , round , id) , 'w')
        json.dump(genome , fl)
        fl.close()

updateGenomes()