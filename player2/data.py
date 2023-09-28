import json , math , time , copy


class Map:
    class Vert:
        def __init__(self):
            self.strategicPts = 0

    def __init__(self, n):
        self.n : int = n
        self.adj : list[list[int]] = [[] for i in range(n)]
        self.verts : list[self.Vert] = [self.Vert() for i in range(n)]
        self.strategicVerts : list[int] = []

    def setAdj(self, v, adj):
        self.adj[v] = adj

    def setStrategic(self, v, strategicPts):
        self.strategicVerts.append(v)
        self.verts[v].strategicPts = strategicPts


class ProxyMap:
    class Vert:
        def __init__(self, team, numNorm, numDef):
            self.team = team
            self.numNorm = numNorm
            self.numDef = numDef
    class Player :
        def __init__(self , nonDropSoldier = 0, doneFort = False, hadSuccessInAttack = False) :
            self.nonDropSoldier = nonDropSoldier
            self.doneFort = doneFort
            self.hadSuccessInAttack = hadSuccessInAttack
    @classmethod
    def makeNew(cls , map : Map, numPlayers : int, actions : list) : 
        self = cls()
        self.players = [self.Player(0 , False , False) for i in range(numPlayers)]
        self.verts = [self.Vert(-1 , 0 , 0) for i in range(map.n)]
        self.actions = actions
        return self
    def __init__(self) :
        self.players : list[self.Player]
        self.verts : list[self.Vert]
        self.actions : list
        
    @classmethod
    def makeCopy(cls , prx) :
        self = cls()
        self.players = [ProxyMap.Player(p.nonDropSoldier , p.doneFort , p.hadSuccessInAttack) for p in prx.players]
        self.verts = [ProxyMap.Vert(v.team , v.numNorm , v.numDef) for v in prx.verts]
        self.actions = copy.deepcopy(prx.actions)
        return self
        
class Genome :
    def __init__(self , path) :
        fl = open(path)
        self.data = json.load(fl)


class StaticData:
    def __init__(self):
        fl = open("States.json", "r")
        self.states = json.load(fl)
        fl.close()
    def getState(self, n, m) -> list:
        if n==0 or m==0 : 
            print("ridim" , n , m)
        mx = max(n, m)
        if mx > 300:

            mlt = 300 / mx
            n *= mlt
            m *= mlt
            n = int(n)
            m = int(m)
            x = []
            for st in self.states[n][m]:
                nowSt = copy.deepcopy(st)
                nowSt[0] *= 1 / mlt
                nowSt[1] *= 1 / mlt
                nowSt[0] = int(nowSt[0])
                nowSt[1] = int(nowSt[1])
                x.append(nowSt)
            return x
        return self.states[n][m]


staticData = StaticData()


def pow2(num):
    return num * num

global mapp  , genomee 
mapp : Map
genomee : Genome
updateTime = 0
initTime = 0
copyTime = 0
class HuristicFunction :
    def __str__(self) :
        return f"Hval = {self.calculateValue()}"

    def __repr__(self):
        return f"Hval = {self.calculateValue()}"
    @classmethod
    def makeCopy(cls , hr) :
        global copyTime
        copyTime -= time.time()
        self : HuristicFunction = cls()
        
        self.ci2 = hr.ci2
        self.currentPoint = hr.currentPoint
        self.nextTurnSoldier = hr.nextTurnSoldier
        self.numberOfBorders = hr.numberOfBorders
        self.numStrat = hr.numStrat
        self.playerId = hr.playerId
        self.soldiers = hr.soldiers
        self.totalSafety = hr.totalSafety
        
        self.proxyMap = ProxyMap.makeCopy(hr.proxyMap)
        self.player = self.proxyMap.players[self.playerId]
        self.powELossRemain1 = hr.powELossRemain1[:]
        self.powELossRemain2 = hr.powELossRemain2[:]
        self.safety = hr.safety[:]
        self.cntMarzi = hr.cntMarzi[:]
        self.dsuHist = hr.dsuHist[:]
        self.dsuHomie = hr.dsuHomie[:]
        self.dsuPar = hr.dsuPar[:]
        self.dsuSize = hr.dsuSize[:]
        self.vertices = hr.vertices[:]
        copyTime += time.time()
        return self
        
    def __init__(self) :
        self.ci2 : int
        self.currentPoint : float
        self.nextTurnSoldier : int
        self.numberOfBorders : int
        self.numStrat : int
        self.playerId : int
        self.soldiers : int
        self.totalSafety : int
        
        self.proxyMap : ProxyMap
        self.player : ProxyMap.Player
        self.powELossRemain1 : list[float]
        self.powELossRemain2 : list[float]
        self.safety : list[float]
        self.cntMarzi : list[int]
        self.dsuHist : list[int]
        self.dsuHomie : list[bool]
        self.dsuPar : list[int]
        self.dsuSize : list[int]
        self.vertices : list[int]
        
    @classmethod
    def makeNew(cls , proxyMap : ProxyMap , playerId : int) :
        global initTime
        initTime -= time.time()
        self = cls()
        self.proxyMap = proxyMap
        self.playerId = playerId
        # num strat
        self.vertices = []
        self.numStrat = 0
        self.soldiers = 0
        self.currentPoint = 0
        self.nextTurnSoldier = 0
        self.cntMarzi = [0 for i in range(mapp.n)]
        
        #params
        global safetyB , safetyBeta , safetyLanda , safetyMu , strategicBonus
        safetyB = genomee.data['saftyB']
        safetyBeta = genomee.data['saftyBata']
        safetyLanda = genomee.data['saftyLanda']
        safetyMu = genomee.data['saftyMu']
        strategicBonus = genomee.data['strategicBonus']

        # safety (sigma (Pi/Di^1/2))  /|marzi|
        # danger[v] = sigma^2 E^2(loss[v] + remaining[u]) + b * sigma^2 E^2(loss[v] + remaining[u])
        # safety[v] =  sigma y^1/2 + b * sigma y + c b * sigma y^2 + m*X 
        self.totalSafety = 0
        self.safety = [0 for i in range(mapp.n)]
        self.powELossRemain1 = [0 for i in range(mapp.n)]
        self.powELossRemain2 = [0 for i in range(mapp.n)]
        self.numberOfBorders = 0

        # sigma (Ci/n)^2
        self.ci2 = 0
        # self.buildDsu()
        
        for v in range(mapp.n) :
            if self.proxyMap.verts[v].team == self.playerId:
                self.vertices.append(v)
                self.soldiers += self.proxyMap.verts[v].numNorm + self.proxyMap.verts[v].numDef
                self.currentPoint += 1000
                if mapp.verts[v].strategicPts > 0 :
                    self.nextTurnSoldier += mapp.verts[v].strategicPts
                    self.currentPoint += 3000 / mapp.verts[v].strategicPts
                    self.numStrat += 1
                sz = 1
                
                self.safety[v] = 0
                
                for u in mapp.adj[v] :
                    if self.proxyMap.verts[u].team == -1 : continue
                    
                    if  self.proxyMap.verts[u].team == self.playerId:
                        self.safety[v] += math.sqrt(self.proxyMap.verts[u].numNorm)
                        self.safety[v] += safetyBeta* self.proxyMap.verts[u].numNorm
                        self.safety[v] += safetyLanda* self.proxyMap.verts[u].numNorm * self.proxyMap.verts[u].numNorm
                    elif (self.proxyMap.verts[u].team+1)%3==self.playerId:
                        self.cntMarzi[v]+=1
                        if (self.cntMarzi[v]==1) : 
                            self.numberOfBorders+=1
                        n = self.proxyMap.verts[u].numNorm
                        m = self.proxyMap.verts[v].numDef + self.proxyMap.verts[v].numNorm
                        simulatedAttack = staticData.getState(n , m)
                        self.powELossRemain1[v] += pow2(simulatedAttack[6][0] + m - simulatedAttack[6][1])
                    else :
                        self.cntMarzi[v]+=1
                        if (self.cntMarzi[v]==1) : 
                            self.numberOfBorders+=1
                        n = self.proxyMap.verts[u].numNorm
                        m = self.proxyMap.verts[v].numDef + self.proxyMap.verts[v].numNorm
                        simulatedAttack = staticData.getState(n , m)
                        self.powELossRemain2[v] += pow2(simulatedAttack[6][0] + m - simulatedAttack[6][1])
                
                if(self.cntMarzi[v] > 0) :
                    danger = self.powELossRemain1[v]*self.powELossRemain1[v] + safetyB*self.powELossRemain2[v]*self.powELossRemain2[v]
                    safety = self.safety[v] + safetyMu * (proxyMap.verts[v].numDef + proxyMap.verts[v].numNorm)
                    self.totalSafety += math.sqrt(safety/math.sqrt(danger)) * (1 if mapp.verts[v].strategicPts == 0 else strategicBonus)
           
        self.totalSafety /= (self.numberOfBorders+1)
        self.buildDsu()         
        
        self.player = proxyMap.players[playerId]
        #soldiers in hand
        # self.nonDropSoldier = proxyMap.players[playerId].nonDropSoldier
        #current point :(sigma 1000ras + sigma 3000/pi + |soldier|)/1000
            # self.numberOfvertices bala tarif shode 
            # self.stratList bala tarif shode 
            # self.soldiers  bala tarif shode
        # self.hadSuccesfulAttack = proxyMap.players[playerId].hadSuccessInAttack
        self.currentPoint += self.soldiers
        self.currentPoint/=1000
        #next turn soldier : sigma pi + |ras|/4 + (succesful attack)*3
        self.nextTurnSoldier += len(self.vertices) // 4

        initTime += time.time()
        return self
        #|soldier| 
            # self.soldiers  bala tarif shode
        
    def viewDataForDbug(self) : 
        dict = {'numStrat' : pow(3 , self.numStrat) ,'connectivity' : self.ci2 / (len(self.vertices) + 1) / (len(self.vertices) + 1) }
        dict['totalSafety'] = self.totalSafety
        # dict['safetyParams'] = {"danger" : self.danger , "safety" : self.safety}
        dict['nonDropSoldier'] = self.player.nonDropSoldier
        dict['currentPoint'] = self.currentPoint
        dict['nextTurnSoldier'] = self.nextTurnSoldier + self.player.hadSuccessInAttack * 3
        dict['soldiers'] = self.soldiers
        return dict

    def buildDsu(self):
        self.dsuPar = [i for i in range(mapp.n)]
        self.dsuSize = [1 for i in range(mapp.n)]
        self.dsuHomie = [self.proxyMap.verts[i].team == self.playerId for i in range(mapp.n)]
        self.dsuHist = []
        self.ci2 = len(self.vertices)
        for v in self.vertices:
            for u in mapp.adj[v]:
                if self.proxyMap.verts[u].team == self.playerId: self.mergeDsu(v, u)

    def parDsu(self, u):
        if self.dsuPar[u] == u: return u
        return self.parDsu(self.dsuPar[u])

    def mergeDsu(self, v, u):  # us - someone
        v = self.parDsu(v)
        u = self.parDsu(u)
        if u == v: return
        if self.dsuSize[u] > self.dsuSize[v]:
            u, v = v, u
        # if self.dsuHomie[v] :   always this is true
        self.ci2 -= self.dsuSize[v] * self.dsuSize[v]
        if self.dsuHomie[u]: self.ci2 -= self.dsuSize[u] * self.dsuSize[u]

        self.dsuPar[u] = v
        self.dsuSize[v] += self.dsuSize[u]

        self.ci2 += self.dsuSize[v] * self.dsuSize[v]
        self.dsuHist.append(u)

    def undoDsu(self, u):
        v = self.dsuPar[u]

        self.ci2 -= self.dsuSize[v] * self.dsuSize[v]

        self.dsuSize[v] -= self.dsuSize[u]
        self.dsuPar[u] = u

        self.ci2 += self.dsuSize[v] * self.dsuSize[v]
        if self.dsuHomie[u]: self.ci2 += self.dsuSize[u] * self.dsuSize[u]

    # par[Max] , sz[Max] , stack hist 
    # merge(u , v) :
    #   par[v] = u
    #   sz[v] += sz[u]
    #   hist.push(v)
    # undo() :
    #   v = hist.pop()
    #   u = par[v]
    #   par[v] = v
    #   sz[v] -= sz[u]
    
    # def updatePlayer(self , data : ProxyMap.Player) :
    #     self.player = self.proxyMap.players[self.playerId] = data
    
    def updateVertex(self , v : int , data : ProxyMap.Vert) :
        global updateTime
        updateTime -= time.time()
        self.totalSafety *= self.numberOfBorders + 1
        lastData = self.proxyMap.verts[v]
        flag = 0
        if lastData.team != data.team:
            if self.playerId == lastData.team:
                flag = -1
            elif self.playerId == data.team:
                flag = 1

        if flag > 0:
            # print("here flag 1")
            self.dsuHomie[v] = True
            self.ci2 += 1
            self.nextTurnSoldier -= len(self.vertices) // 4
            self.vertices.append(v)
            self.currentPoint += 1
            self.nextTurnSoldier += len(self.vertices) // 4
            if v in mapp.strategicVerts:
                self.numStrat += 1
                self.currentPoint += 3 / mapp.verts[v].strategicPts
                self.nextTurnSoldier += mapp.verts[v].strategicPts
            self.dsuHist.append(-1)
            for u in mapp.adj[v]:
                if self.proxyMap.verts[u].team == self.playerId:
                    self.mergeDsu(u, v)
            self.soldiers += data.numNorm + data.numDef
            self.currentPoint += data.numNorm / 1000 + data.numDef / 1000

        elif flag == 0:
            # print("here falg 0")
            self.currentPoint -= self.soldiers / 1000
            self.soldiers -= lastData.numNorm + lastData.numDef
            self.soldiers += data.numNorm + data.numDef
            self.currentPoint += self.soldiers/1000
            
        else :
            self.nextTurnSoldier -= len(self.vertices) // 4
            self.currentPoint-= (lastData.numNorm + lastData.numDef)/1000 + 1
            if mapp.verts[v].strategicPts > 0 :
                self.numStrat -= 1
                self.currentPoint -= 3 / mapp.verts[v].strategicPts
                self.nextTurnSoldier -= mapp.verts[v].strategicPts
            self.soldiers -= lastData.numNorm + lastData.numDef
            # print("here flag -1")
            hst = self.dsuHist.pop()
            while hst >= 0:
                self.undoDsu(hst)
                hst = self.dsuHist.pop()
            self.dsuHomie[v] = False
            self.ci2 -= 1
            self.vertices.pop() # guaranty v is at the end of vertices
            self.nextTurnSoldier += len(self.vertices) // 4
            

        
        def removeSafety(v : int , u : int) :
            if self.proxyMap.verts[v].team != self.playerId or self.proxyMap.verts[u].team == -1 : return         
            if  self.proxyMap.verts[u].team == self.playerId:
                self.safety[v] -= math.sqrt(self.proxyMap.verts[u].numNorm)
                self.safety[v] -= safetyBeta* self.proxyMap.verts[u].numNorm
                self.safety[v] -= safetyLanda* self.proxyMap.verts[u].numNorm * self.proxyMap.verts[u].numNorm
            elif (self.proxyMap.verts[u].team+1)%3==self.playerId:
                self.cntMarzi[v]-=1
                if (self.cntMarzi[v]==0) : 
                    self.numberOfBorders-=1
                n = self.proxyMap.verts[u].numNorm
                m = self.proxyMap.verts[v].numDef + self.proxyMap.verts[v].numNorm
                simulatedAttack = staticData.getState(n, m)
                self.powELossRemain1[v] -= pow2(simulatedAttack[6][0] + m - simulatedAttack[6][1])
            else:
                self.cntMarzi[v] -= 1
                if (self.cntMarzi[v] == 0):
                    self.numberOfBorders -= 1
                n = self.proxyMap.verts[u].numNorm
                m = self.proxyMap.verts[v].numDef + self.proxyMap.verts[v].numNorm
                simulatedAttack = staticData.getState(n, m)
                self.powELossRemain2[v] -= pow2(simulatedAttack[6][0] + m - simulatedAttack[6][1])
        
        def addSafety(v : int , u : int) :
            if self.proxyMap.verts[v].team != self.playerId or self.proxyMap.verts[u].team == -1 : return        
            if  self.proxyMap.verts[u].team == self.playerId:
                self.safety[v] += math.sqrt(self.proxyMap.verts[u].numNorm)
                self.safety[v] += safetyBeta* self.proxyMap.verts[u].numNorm
                self.safety[v] += safetyLanda* self.proxyMap.verts[u].numNorm * self.proxyMap.verts[u].numNorm
            elif (self.proxyMap.verts[u].team+1)%3==self.playerId:
                self.cntMarzi[v]+=1
                if (self.cntMarzi[v]==1) : 
                    self.numberOfBorders+=1
                n = self.proxyMap.verts[u].numNorm
                m = self.proxyMap.verts[v].numDef + self.proxyMap.verts[v].numNorm
                simulatedAttack = staticData.getState(n , m)
                self.powELossRemain1[v] += pow2(simulatedAttack[6][0] + m - simulatedAttack[6][1])
            else:
                self.cntMarzi[v] += 1
                if (self.cntMarzi[v] == 1):
                    self.numberOfBorders += 1
                n = self.proxyMap.verts[u].numNorm
                m = self.proxyMap.verts[v].numDef + self.proxyMap.verts[v].numNorm
                simulatedAttack = staticData.getState(n, m)
                self.powELossRemain2[v] += pow2(simulatedAttack[6][0] + m - simulatedAttack[6][1])

        mapp.adj[v].append(v)
        for i in mapp.adj[v] : 
            if (self.proxyMap.verts[i].team==self.playerId and self.cntMarzi[i] > 0) : 
                safety = self.safety[i] + safetyMu * (self.proxyMap.verts[i].numDef + self.proxyMap.verts[i].numNorm)
                danger = self.powELossRemain1[i]*self.powELossRemain1[i] + safetyB*self.powELossRemain2[i]*self.powELossRemain2[i]
                self.totalSafety -= math.sqrt(safety/math.sqrt(danger)) * (1 if mapp.verts[v].strategicPts == 0 else strategicBonus)
        mapp.adj[v].pop()

        for u in mapp.adj[v]:
            removeSafety(v, u)
            removeSafety(u, v)

        lastData.team = data.team
        lastData.numNorm = data.numNorm
        lastData.numDef = data.numDef

        for u in mapp.adj[v]:
            addSafety(v, u)
            addSafety(u, v)

        mapp.adj[v].append(v)
        for i in mapp.adj[v] : 
            if (self.proxyMap.verts[i].team==self.playerId and self.cntMarzi[i] > 0) : 
                safety = self.safety[i] + safetyMu * (self.proxyMap.verts[i].numDef + self.proxyMap.verts[i].numNorm)
                danger = self.powELossRemain1[i]*self.powELossRemain1[i] + safetyB*self.powELossRemain2[i]*self.powELossRemain2[i]
                self.totalSafety += math.sqrt(safety/math.sqrt(danger)) * (1 if mapp.verts[v].strategicPts == 0 else strategicBonus)
        self.totalSafety /= self.numberOfBorders + 1
        mapp.adj[v].pop()
        updateTime += time.time()

    def calculateValue(self):
        value = 0
        if (self.numStrat > 3) : 
            value+=1000000
        value += pow(3, self.numStrat) * genomee.data['numStrat']
        value += genomee.data['connectivity'] * self.ci2 / (len(self.vertices) * len(self.vertices) + 1)
        value += self.totalSafety * genomee.data['totalSafety']
        value += self.player.nonDropSoldier * genomee.data['nonDropSoldier']
        value += self.currentPoint * genomee.data["currentPoint"]
        value += (self.nextTurnSoldier + 3 * self.player.hadSuccessInAttack) * genomee.data["nextTurnSoldier"]
        value += self.soldiers * genomee.data["soldiers"]
        #strategic soldiers 
        for v in mapp.strategicVerts :
            vert = self.proxyMap.verts[v]
            if vert.team == self.playerId :
                value += genomee.data['stratSoldSq'] * math.sqrt(vert.numDef + vert.numNorm) + genomee.data['stratSold'] * (vert.numDef + vert.numNorm)
        return value

# testing
