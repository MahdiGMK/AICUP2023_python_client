import run , threading

def runGame(map , genome1 , genome2 , genome3) :
    res = run.run(map , genome1 , genome2 , genome3)
    x = [(res[i] , i) for i in range(3)]
    x.sort()
    res[x[0][1]] = 0
    res[x[1][1]] = 1
    res[x[2][1]] = 3
    print(res)

runGame("map1.json" , "player0/genome.json" , "player0/genome.json" , "player0/genome.json")
# print(res)
# run.run("map1.json" , "player0/genome.json" , "player0/genome.json" , "player0/genome.json")
# run.run("map1.json" , "player0/genome.json" , "player0/genome.json" , "player0/genome.json")
# run.run("map1.json" , "player0/genome.json" , "player0/genome.json" , "player0/genome.json")

