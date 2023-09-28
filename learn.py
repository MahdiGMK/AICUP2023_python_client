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
    # scoreBoard[genome1] += res[0]
    # scoreBoard[genome2] += res[1]
    # scoreBoard[genome3] += res[2]

def runMatch(map , genome1 , genome2 , genome3) :
    runGame(map , genome1 , genome2 , genome3)
    runGame(map , genome3 , genome1 , genome2)
    runGame(map , genome2 , genome3 , genome1)

def runRound() :
    x = 0
    
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
    
    with open('parameters.json' , 'w') as fl :
        json.dump(data , fl)

# def makeNeededGenomes() :
#     num = os.listdir('genomes')

# makeNewGenome()


# timer = time.time()
# # runGame(f"map1.json" , "player0/genome.json" , "player0/genome.json" , "player0/genome.json")
for i in range(1 , 105) :
    runGame(f"map{i}.json" , "player0/genome.json" , "player0/genome.json" , "player0/genome.json")
# print('total time' , time.time() - timer)

# print(res)
# run.run("map1.json" , "player0/genome.json" , "player0/genome.json" , "player0/genome.json")
# run.run("map1.json" , "player0/genome.json" , "player0/genome.json" , "player0/genome.json")
# run.run("map1.json" , "player0/genome.json" , "player0/genome.json" , "player0/genome.json")

