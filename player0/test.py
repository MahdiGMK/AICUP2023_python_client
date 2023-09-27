import copy
import data as pd
import data_experimental as pd_exp
import copy
import random 
import time
import transition as ts

map = pd.Map(42)


def addadj(a, b):
    map.adj[a].append(b)
    map.adj[b].append(a)


x = [[0, 1], [0, 2], [1, 2], [1, 3], [2, 3], [3, 4], [4, 5], [4, 6], [5, 6], [5, 8], [5, 7], [5, 14], [5, 13], [6, 7],
     [6, 21], [7, 21], [7, 15], [7, 14], [8, 13], [8, 11], [8, 10], [9, 8], [9, 10], [10, 12], [10, 11], [10, 36],
     [11, 12], [11, 13], [12, 13], [13, 14], [14, 15], [15, 21], [15, 20], [15, 18], [15, 16], [16, 18], [16, 17],
     [16, 41], [17, 41], [17, 19], [17, 18], [18, 19], [18, 20], [19, 20], [19, 27], [20, 21], [20, 22], [21, 22],
     [21, 23], [22, 23], [22, 27], [23, 24], [23, 25], [23, 26], [23, 27], [24, 25], [25, 26], [26, 27], [27, 28],
     [28, 29], [28, 30], [28, 31], [29, 30], [30, 31], [31, 32], [32, 33], [32, 34], [33, 34], [33, 38], [33, 39],
     [34, 35], [34, 38], [35, 38], [35, 37], [35, 36], [36, 37], [37, 38], [37, 40], [38, 39], [38, 40], [39, 40],
     [40, 41]]
for e in x:
    addadj(e[0], e[1])

for i in [29, 3, 7, 4, 20, 40]:
    map.setStrategic(i, 5)

gen = pd.Genome("genome.json")

t = time.time()

numGames = int(20)
numActions  = int(1e3)
testCorrectness = False

for cntr in range(numGames):

    prx = pd.ProxyMap.makeNew(map , 3 , [])
    # print(map.adj)
    for i in range(41):
        prx.verts[i].team = random.randint(0, 1)
        prx.verts[i].numNorm = random.randint(1, 5)
        prx.verts[i].numDef = random.randint(1, 5)
        if (prx.verts[i].team == 0):
            prx.verts[i].numNorm = random.randint(200, 300)

    pd.genomee = gen
    pd.mapp = map
    hr = pd.HuristicFunction.makeNew(prx, 0)
    hr.proxyMap.players[0].nonDropSoldier += 100

    print(ts.calcStateValue(hr , 0))


    tst = ts.miniMax(hr , 5 , 0 , [0 , 0 , 0] , 1 , 1 , 3)
    print(ts.calcStateValue(tst[0] , 0))


    # tst = ts.beamSearch([hr] , 5  , 0 , 0 , 1)
    # cnt = 0
    # for mp in tst :
    #     print(cnt , " : " , mp)
    #     cnt+=1


    # tst = ts.dropSoldier([hr] , 5 , 5 , 0 , 0)
    # print(tst)

    # tst = ts.attackBeamSearch([(copy.deepcopy(hr), [ts.Movement(ts.MoveKind.DropSoldier, [2, 3])])], 5, 5, 0, 1,
    #                           4)  # Q[depth]
    # print(tst)
    # tst = ts.attackBeamSearch([hr] , 3, 5 , 0 , 1 , 4) # Q[depth]
    # print(len(tst))
    # for at in tst:  # at : Q[depth][]
    #     for m in at:
    #         print(m)

    # attack

    # print(hr.calculateValue() , hr.viewDataForDbug())

    # hist = []

    # hr_exp = pd_exp.HuristicFunction.makeNew(prx_exp , 0)
    # hr_exp.updatePlayer(pd.ProxyMap.Player(100 , False , False))
    
    # for cnt in range(1 , numActions + 1) :
    #     # if False :
    #     rnd = random.random()
    #     if(rnd < .2) :
    #         nonDropSoldier = random.randint(0 , 10)
    #         doneFort = random.randint(0 , 1) > 0
    #         hadSuccessInAttack = random.randint(0 , 1) > 0
    #         hr.updatePlayer(pd.ProxyMap.Player(nonDropSoldier , doneFort , hadSuccessInAttack))
    #         hr_exp.updatePlayer(pd.ProxyMap.Player(nonDropSoldier , doneFort , hadSuccessInAttack))
    #     elif len(hist) > 0 and rnd < 0.6 :
    #         vert = hist.pop()
    #         num = random.randint(1 , 20)
    #         numDef = random.randint(1 , 20)
    #         hr.updateVertex(vert , pd.ProxyMap.Vert(2 , num , numDef))
    #         hr_exp.updateVertex(vert , pd.ProxyMap.Vert(2 , num , numDef))
    #     else :
    #         vert = random.randint(0 , map.n - 1)
    #         if prx.verts[vert].team != 0 :
    #             hist.append(vert)
    #         num = random.randint(1 , 20)
    #         numDef = random.randint(1 , 20)
    #         hr.updateVertex(vert , pd.ProxyMap.Vert(0 , num , numDef))
    #         hr_exp.updateVertex(vert , pd.ProxyMap.Vert(0 , num , numDef))
            
    #     hr_main = pd.HuristicFunction.makeNew(prx , 0) if testCorrectness else hr
    #     hr_main_exp = pd_exp.HuristicFunction.makeNew(prx_exp , 0) if testCorrectness else hr
    #     # hr_main_exp.buildDsu()
    #     # hr2 = pd.HuristicFunction(map , prx , gen , 1)
    #     if abs(hr.calculateValue() - hr_exp.calculateValue()) > 0.01 or abs(hr.calculateValue() - hr_main.calculateValue()) > 0.01 or abs(hr.calculateValue() - hr_main_exp.calculateValue()) > 0.01:
    #         print("Error in " , cnt)
    #         print(hr.calculateValue() , hr.viewDataForDbug())
    #         print(hr_exp.calculateValue() , hr_exp.viewDataForDbug())
    #         print(hr_main.calculateValue() , hr_main.viewDataForDbug())
    #         print(hr_main_exp.calculateValue() , hr_main_exp.viewDataForDbug())
    #         break
    
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


print(time.time() - t)

print('init time : ' , pd.initTime)
print('exp init time : ' , pd_exp.initTime)
print('update time : ' , pd.updateTime)
print('exp update time : ' , pd_exp.updateTime)


# t = -time.time()
# for i in range(int(1e5)) :
#     tst = copy.deepcopy(hr)
# print('copy time : ' , t + time.time())
# t = -time.time()
# for i in range(int(1e5)) :
#     tst = pd_exp.HuristicFunction.makeCopy(hr_exp)
# print('exp copy time : ' , t + time.time())
