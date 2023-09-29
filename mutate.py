import os , json , random
import learn
import random

def filter(bestCut , randChance) :
    with open('scores.json' , 'r') as fl :
        scores = json.load(fl)
    sorted_ids = sorted(scores , key=lambda x:scores[x] , reverse=True)
    removed_ids = []
    
    idx = 0
    for id in sorted_ids :
        idx += 1
        exist = idx <= bestCut * (len(sorted_ids) - 2) or random.random() <= randChance
        if not exist :
            scores.pop(id)
            os.remove(id)

    with open('scores.json' , 'w') as fl :
        json.dump(scores , fl)

def mutate(mutation , count) :
    with open('scores.json' , 'r') as fl :
        scores = json.load(fl)
    with open('parameters.json' , 'r') as fl :
        parameters = json.load(fl)
    genomes = []
    mutatedGenomes = []
    for key in scores :
        with open(key, 'r') as fl :
            genomes.append(json.load(fl))
    
    G1CUT = 1 - mutation
    G0CUT = G1CUT / 2
    for i in range(count) : 
        i0 = random.choice(genomes)
        i1 = random.choice(genomes)
        
        result = {}
        for p in parameters :
            rnd = random.random()
            if rnd < G0CUT :
                result[p] = i0[p]
            elif rnd < G1CUT :
                result[p] = i1[p]
            else :
                result[p] = learn.numberInRange(parameters[p]['min'] , parameters[p]['max'])
        mutatedGenomes.append(result)