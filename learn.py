import run , time , random , os , json

scoreBoard = {}


def numberInRange(min , max):
    if(min == max) : return min
    return random.uniform(min , max)

def randHash() -> str:
    return "%016x" % random.getrandbits(64)

def runGame(map , genome1 , genome2 , genome3) :
    res = run.run(map , genome1 , genome2 , genome3)
    x = [(res[i] , i) for i in range(3)]
    x.sort()
    res[x[0][1]] = 0
    res[x[1][1]] = 1
    res[x[2][1]] = 3
    
    # global scoreBoard
    scoreBoard[genome1] += res[0]
    scoreBoard[genome2] += res[1]
    scoreBoard[genome3] += res[2]

def runMatch(genome1 , genome2 , genome3) :
    map = f'map{random.randint(1 , 104)}.json'
    runGame(map , genome1 , genome2 , genome3)
    runGame(map , genome3 , genome1 , genome2)
    runGame(map , genome2 , genome3 , genome1)

def runRound() :
    makeNeededGenomes()
    genomes = os.listdir('genomes')
    genomes = [f'genomes/{x}' for x in genomes]
    random.shuffle(genomes)
    
    for g in genomes : scoreBoard[g] = 0
    
    for i in range(len(genomes) // 3) :
        runMatch(genomes[3 * i] , genomes[3 * i + 1] , genomes[3 * i + 2])
    
    if os.path.exists('scores.json') :
        with open('scores.json' , 'r') as fl :
            prvScores = json.load(fl)
            for x in scoreBoard :
                scoreBoard[x] += prvScores[x]
    
            
    with open('scores.json' , 'w') as fl :
        json.dump(scoreBoard , fl)
        
    
def readParameters() -> dict:
    with open('parameters.json' , 'r') as fl :
        return json.load(fl)

def makeNewGenome() :
    id = randHash()
    parameters = readParameters()
    
    data = {}
    for x in parameters :
        mn = parameters[x]['min']
        mx = parameters[x]['max']
        data[x] = numberInRange(mn , mx)
    
    with open(f'genomes/{id}.json' , 'w') as fl :
        json.dump(data , fl)

def makeNeededGenomes() :
    num = len(os.listdir('genomes'))
    while(num < 30) :
        makeNewGenome()
        num += 1


runRound()
