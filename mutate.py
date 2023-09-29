import os , json , random
import random

def numberInRange(min , max):
    if(min == max) : return min
    return random.uniform(min , max)

def randHash() -> str:
    return "%016x" % random.getrandbits(64)

def filter(bestCut , randChance) :
    with open('scores.json' , 'r') as fl :
        scores = json.load(fl)
    sorted_ids = sorted(scores , key=lambda x:scores[x] , reverse=True)
    removed_ids = []
    
    idx = 0
    for id in sorted_ids :
        idx += 1
        exist = idx <= bestCut * len(sorted_ids) or random.random() <= randChance
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
    
    for i in range(count) : 
        i0 = random.choice(genomes)
        i1 = random.choice(genomes)
        
        result = {}
        for p in parameters :
            rnd = random.random()
            if rnd <= .5 :
                result[p] = i0[p]
            else :
                result[p] = i1[p]
            
            if random.random() < mutation :
                result[p] += random.uniform(-result[p] / 10 , result[p] / 10)
                
        mutatedGenomes.append(result)
    folder_path = 'genomes'
    # for filename in os.listdir(folder_path):
    #     file_path = os.path.join(folder_path, filename)
    #     if filename.endswith('.json') and os.path.isfile(file_path):
    #         os.remove(file_path)
    for m in mutatedGenomes : 
        file_name = str(randHash()) + ".json"
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'w') as fl:
            json.dump(m, fl, indent=4)


filter(7/30 , 3/30)
mutate(.1 , 15)