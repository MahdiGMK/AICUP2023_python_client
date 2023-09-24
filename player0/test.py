import data as pd
import random 
import time 
map = pd.Map(42)

def addadj(a , b) : 
    map.adj[a].append(b)
    map.adj[b].append(a)


x = [[0, 1], [0, 2], [1, 2], [1, 3], [2, 3], [3, 4], [4, 5], [4, 6], [5, 6], [5, 8], [5, 7], [5, 14], [5, 13], [6, 7], [6, 21], [7, 21], [7, 15], [7, 14], [8, 13], [8, 11], [8, 10], [9, 8], [9, 10], [10, 12], [10, 11], [10, 36], [11, 12], [11, 13], [12, 13], [13, 14], [14, 15], [15, 21], [15, 20], [15, 18], [15, 16], [16, 18], [16, 17], [16, 41], [17, 41], [17, 19], [17, 18], [18, 19], [18, 20], [19, 20], [19, 27], [20, 21], [20, 22], [21, 22], [21, 23], [22, 23], [22, 27], [23, 24], [23, 25], [23, 26], [23, 27], [24, 25], [25, 26], [26, 27], [27, 28], [28, 29], [28, 30], [28, 31], [29, 30], [30, 31], [31, 32], [32, 33], [32, 34], [33, 34], [33, 38], [33, 39], [34, 35], [34, 38], [35, 38], [35, 37], [35, 36], [36, 37], [37, 38], [37, 40], [38, 39], [38, 40], [39, 40], [40, 41]]
for e in x : 
    addadj(e[0] , e[1])

for i in [29, 3, 7, 4, 20, 40] : 
    map.setStrategic(i , 5)

gen = pd.Genome("genome.json")

t = time.time()

numGames = 1
numActions  = 1000000

for cntr in range(numGames) :

    prx = pd.ProxyMap(map , 3 , [])
    # print(map.adj)
    for i in range(41) : 
        prx.verts[i].team = random.randint(0 , 3)-1
        prx.verts[i].numNorm = random.randint(1 , 50)
        prx.verts[i].numDef = random.randint(1 , 50)


    hr = pd.HuristicFunction(map , prx , gen , 1)
    #attack 

    # print(hr.calculateValue() , hr.viewDataForDbug())
    hr.buildDsu()

    hist = []

        
    for cnt in range(1 , numActions + 1) :
        # if False :
        if len(hist) > 0 and random.random() < 0.4 :
            vert = hist.pop()
            num = random.randint(1 , 20)
            numDef = random.randint(1 , 20)
            hr.updateVertex(vert , pd.ProxyMap.Vert(2 , num , numDef))
        else :
            vert = random.randint(0 , map.n - 1)
            if prx.verts[vert].team != 1 :
                hist.append(vert)
            num = random.randint(1 , 20)
            numDef = random.randint(1 , 20)
            hr.updateVertex(vert , pd.ProxyMap.Vert(1 , num , numDef))
        # hr2 = pd.HuristicFunction(map , prx , gen , 1)
        # if abs(hr.calculateValue() - hr2.calculateValue()) > 0.01 :
        #     print("Error in " , cnt)
        #     print(hr.calculateValue() , hr.viewDataForDbug())
        #     print(hr2.calculateValue() , hr2.viewDataForDbug())
        #     break
    
# print(hr.calculateValue() , hr.viewDataForDbug())
# print(hr2.calculateValue() , hr2.viewDataForDbug())
        
    
print("DONE")




# cnt = 0 
# while(cnt < 1000000) : 
#     hr1 = pd.HuristicFunction(map , prx , gen , 1)
#     hr2 = pd.HuristicFunction(map , prx , gen , 2)
#     hr3 = pd.HuristicFunction(map , prx , gen , 0)
#     cnt = cnt + 1

# print(hr1.viewDataForDbug())
# print(hr2.viewDataForDbug())
# print(hr3.viewDataForDbug())
# print(hr1.ci2)
# hr1.buildDsu()
# print(hr1.ci2)

# print(hr2.ci2)
# hr2.buildDsu()
# print(hr2.ci2)

# print(hr3.ci2)
# hr3.buildDsu()
# print(hr3.ci2)


print(time.time()-t)

