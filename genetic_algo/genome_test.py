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

def readGenome(version , round_idx , id) -> dict :
    fl = open('genomes/{}/{}/{}.json'.format(version , round_idx , id) , 'r')
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
    round_idx = parameters['round']['min']
    
    # create genome{id}.json
    
    data = {}
    for x in parameters :
        mn = parameters[x]['min']
        mx = parameters[x]['max']
        data[x] = numberInRange(mn , mx)
    
    os.makedirs('genomes/{}/{}/'.format(version , round_idx) ,exist_ok=True)
    fl = open('genomes/{}/{}/{}.json'.format(version , round_idx , id) , "w")
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
    last_round_idx = scores['round']
    
    # update version and round_idx
    version = scores['version'] = parameters['version']['min']
    round_idx = scores['round'] = parameters['round']['min']
    fl = open('scores.json' , 'w')
    json.dump(scores , fl)
    fl.close()
    
    os.makedirs('genomes/{}/{}/'.format(version , round_idx) , exist_ok=True)
    for id in scores :
        if(id == 'version' or id == 'round') :
            continue
        genome = readGenome(last_version , last_round_idx , id)
        for p in parameters :
            mn = parameters[p]['min']
            mx = parameters[p]['max']
            
            if(genome.__contains__(p)) :
                if(genome[p] < mn) : genome[p] = mn
                if(genome[p] > mx) : genome[p] = mx
            else :
                genome[p] = numberInRange(mn , mx)
        
        fl = open('genomes/{}/{}/{}.json'.format(version , round_idx , id) , 'w')
        json.dump(genome , fl)
        fl.close()

def filterGenomes(bestCut , randChance) :
    scores = readScores()
    sorted_ids = sorted(scores , key=lambda x:scores[x] , reverse=True)
    removed_ids = []
    version = scores['version']
    round_idx = scores['round']
    
    idx = 0
    for id in sorted_ids :
        if id == 'version' or id == 'round' : continue
        idx += 1
        exist = idx <= bestCut * (len(sorted_ids) - 2) or random.random() <= randChance
        if not exist :
            scores.pop(id)
            os.remove('genomes/{}/{}/{}.json'.format(version , round_idx , id))

    fl = open('scores.json' , 'w')
    json.dump(scores , fl)
    fl.close()

def createOffsprings(numChild) :
    parameters = readParameters()
    scores = readScores()
    version = parameters['version']['min']
    round_idx = parameters['round']['min']
    
    current_ids = []
    for id in scores :
        if(id == 'version' or id == 'round') : continue
        current_ids.append(id)
    
    for i in range(numChild) :
        id = randHash()
        id1 = random.choice(current_ids)
        id2 = random.choice(current_ids)
        
        fl = open('genomes/{}/{}/{}.json'.format(version , round_idx , id1) , 'r')
        par1 = json.load(fl)
        fl.close()
        fl = open('genomes/{}/{}/{}.json'.format(version , round_idx , id2) , 'r')
        par2 = json.load(fl)
        fl.close()
        genome = {}
        
        for param in parameters :
            rnd = random.random()
            PAR1CUT = .45
            PAR2CUT = .9
            
            if rnd <= PAR1CUT :
                genome[param] = par1[param]
            elif rnd <= PAR2CUT :
                genome[param] = par2[param]
            else :
                mn = parameters[param]['min']
                mx = parameters[param]['max']
                genome[param] = numberInRange(mn , mx)
            
        scores[id] = 0
        fl = open('genomes/{}/{}/{}.json'.format(version , round_idx , id) , 'w')
        json.dump(genome , fl)
        fl.close()
    
    
    for id in current_ids :
        scores.pop(id)
        os.remove('genomes/{}/{}/{}.json'.format(version , round_idx , id))
    fl = open('scores.json' , 'w')
    json.dump(scores , fl)
    fl.close()

def getScore(id) -> float:
    scores = readScores()
    return scores[id]
    
def updateScore(id , newScore):
    scores = readScores()
    scores[id] = newScore
    fl = open('scores.json' , 'r')
    json.dump(scores , fl)
    fl.close()


# for i in range(4) :
#     generateNewGenome()

# filterGenomes(-1 , -1)
resetGenomes()