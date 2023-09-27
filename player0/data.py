import json , math , time , copy

class Map :
    class Vert :
        def __init__(self) :
            self.strategicPts = 0
    def __init__(self , n) :
        self.n = n
        self.adj = [[] for i in range(n)]
        self.verts = [self.Vert() for i in range(n)]
        self.strategicVerts = []
    
    def setAdj(self , v , adj) :
        self.adj[v] = adj
        
    def setStrategic(self , v , strategicPts) :
        self.strategicVerts.append(v)
        self.verts[v].strategicPts = strategicPts
    


class ProxyMap :
    class Vert : 
        def __init__(self , team , numNorm , numDef) :
            self.team = team
            self.numNorm = numNorm
            self.numDef = numDef
    class Player :
        def __init__(self , nonDropSoldier, doneFort, hadSuccessInAttack) :
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
        x = 0
    @classmethod
    def makeCopy(cls , prx) :
        val = cls()
        val.players = [ProxyMap.Player(p.nonDropSoldier , p.doneFort , p.hadSuccessInAttack) for p in prx.players]
        val.verts = [ProxyMap.Vert(v.team , v.numNorm , v.numDef) for v in prx.verts]
        val.actions = copy.deepcopy(prx.actions)
        return val
        
class Genome :
    def __init__(self , path) :
        fl = open(path)
        self.data = json.load(fl)

class StaticData : 
    def __init__(self) :
        fl = open("../States.json" , "r")
        self.states = json.load(fl)
        fl.close()
    def getState(self , n , m) -> list :
        mx = max(n , m)
        if mx > 300 :

            mlt = 300 / mx
            n *= mlt
            m *= mlt
            n = int(n)
            m = int(m)
            x = []
            for st in self.states[n][m] :
                nowSt = copy.deepcopy(st)
                nowSt[0]*=1/mlt
                nowSt[1]*=1/mlt
                nowSt[0] = int(nowSt[0])
                nowSt[1] = int(nowSt[1])
                x.append(nowSt)
            return x
        return self.states[n][m]
staticData = StaticData()

def pow2(num) : 
    return num * num

global mapp , genomee
updateTime = 0
initTime = 0
class HuristicFunction :
    def __str__(self) :
        return f"Hval = {self.calculateValue()}"
    def __repr__(self) :
        return f"Hval = {self.calculateValue()}"
    def dfs(self , v : int) :
        self.seen[v] = True
        self.vertices.append(v)
        self.soldiers += self.proxyMap.verts[v].numNorm + self.proxyMap.verts[v].numDef
        self.currentPoint += 1000
        if mapp.verts[v].strategicPts > 0 :
            self.nextTurnSoldier += mapp.verts[v].strategicPts
            self.currentPoint += 3000 / mapp.verts[v].strategicPts
            self.numStrat += 1
        sz = 1
        for u in mapp.adj[v] :
            if self.proxyMap.verts[u].team == -1 : continue
            
            if  self.proxyMap.verts[u].team == self.playerId:
                self.sqy[v]+=math.sqrt(self.proxyMap.verts[u].numNorm)
                self.normy[v] += self.proxyMap.verts[u].numNorm
                self.powy[v] += self.proxyMap.verts[u].numNorm * self.proxyMap.verts[u].numNorm
            elif (self.proxyMap.verts[u].team+1)%3==self.playerId:
                self.cntMarzi[v]+=1
                if (self.cntMarzi[v]==1) : 
                    self.numberOfBorders+=1
                n = self.proxyMap.verts[u].numNorm
                m = self.proxyMap.verts[v].numDef + self.proxyMap.verts[u].numNorm
                simulatedAttack = staticData.getState(n , m)
                self.powELossRemain1[v] += pow2(simulatedAttack[6][0] + m - simulatedAttack[6][1])
            else :
                self.cntMarzi[v]+=1
                if (self.cntMarzi[v]==1) : 
                    self.numberOfBorders+=1
                n = self.proxyMap.verts[u].numNorm
                m = self.proxyMap.verts[v].numDef + self.proxyMap.verts[u].numNorm
                simulatedAttack = staticData.getState(n , m)
                self.powELossRemain2[v] += pow2(simulatedAttack[6][0] + m - simulatedAttack[6][1])
            if not self.seen[u] :
                if self.proxyMap.verts[u].team == self.playerId :
                    sz += self.dfs(u)
                    
        return sz
    # def __init__(self , hr : HuristicFunction) :
    #     x = 0
    #     # self.vertices
    #     self.ci2 
    #     self.cntMarzi
    #     self.currentPoint
    #     self.danger
    #     self.dsuHist
    #     self.dsuHomie
    #     self.dsuPar
    #     self.dsuSize
    #     genomee
    #     self.hadSuccesfulAttack
    #     mapp
    #     self.nextTurnSoldier
    #     self.nonDropSoldier
    #     self.normy
    #     self.numberOfBorders
    #     self.numStrat
    #     self.playerId
    #     self.powELossRemain1
    #     self.powELossRemain2
    #     self.powy
    #     self.proxyMap
    #     self.safety
    #     self.safetyB
    #     self.safetyBeta
    #     self.safetyLanda
    #     self.safetyMu
    #     self.seen
    #     self.soldiers
    #     self.sqy
    #     self.totalSafety
    #     self.vertices
        
    def __init__(self ,  proxyMap : ProxyMap , playerId : int) : 
        global initTime
        initTime -= time.time()
        self.proxyMap = proxyMap
        self.playerId = playerId
        #num strat
        self.vertices = []
        self.numStrat = 0
        self.soldiers = 0
        self.currentPoint = 0
        self.nextTurnSoldier = 0
        self.cntMarzi = [0 for i in range(mapp.n)]

        #safety (sigma (Pi/Di^1/2))  /|marzi|
        # danger[v] = sigma^2 E^2(loss[v] + remaining[u]) + b * sigma^2 E^2(loss[v] + remaining[u])
        # safety[v] =  sigma y^1/2 + b * sigma y + c b * sigma y^2 + m*X 
        self.totalSafety = 0
        self.safety = [0 for i in range(mapp.n)]
        self.danger = [0 for i in range(mapp.n)]
        self.sqy = [0 for i in range(mapp.n)]
        self.normy = [0 for i in range(mapp.n)]
        self.powy = [0 for i in range(mapp.n)]
        self.powELossRemain1 = [0 for i in range(mapp.n)]
        self.powELossRemain2 = [0 for i in range(mapp.n)]
        self.numberOfBorders = 0

        #sigma (Ci/n)^2
        self.ci2 = 0
        self.seen = [False for i in range(mapp.n)]
        for v in range(mapp.n) :
            if not self.seen[v] :
                if proxyMap.verts[v].team == playerId :
                    x = self.dfs(v)
                    self.ci2 += x * x

        #safety again
        
        self.safetyB = genomee.data['saftyB']
        self.safetyBeta = genomee.data['saftyBata']
        self.safetyLanda = genomee.data['saftyLanda']
        self.safetyMu = genomee.data['saftyMu']
        for i in self.vertices : 
            if (proxyMap.verts[i].team==playerId and self.cntMarzi[i] > 0) : 
                self.danger[i] = self.powELossRemain1[i]*self.powELossRemain1[i] + self.safetyB*self.powELossRemain2[i]*self.powELossRemain2[i]
                self.safety[i] = self.sqy[i] +self.safetyBeta*self.normy[i] + self.safetyLanda * self.powy[i] 
                self.safety[i] += self.safetyMu * (proxyMap.verts[i].numDef + proxyMap.verts[i].numNorm)
                self.totalSafety+= math.sqrt(self.safety[i]/math.sqrt(self.danger[i]))
        self.totalSafety /= (self.numberOfBorders+1)
        
        #soldiers in hand
        self.nonDropSoldier = proxyMap.players[playerId].nonDropSoldier
        #current point :(sigma 1000ras + sigma 3000/pi + |soldier|)/1000
            # self.numberOfvertices bala tarif shode 
            # self.stratList bala tarif shode 
            # self.soldiers  bala tarif shode
        self.hadSuccesfulAttack = proxyMap.players[playerId].hadSuccessInAttack
        self.currentPoint += self.soldiers
        self.currentPoint/=1000
        #next turn soldier : sigma pi + |ras|/4 + (succesful attack)*3
        self.nextTurnSoldier += len(self.vertices) // 4 + self.hadSuccesfulAttack * 3

        initTime += time.time()
        #|soldier| 
            # self.soldiers  bala tarif shode
        
    def viewDataForDbug(self) : 
        dict = {'numStrat' : pow(3 , self.numStrat) ,'connectivity' : self.ci2 / len(self.vertices) / len(self.vertices) }
        dict['totalSafety'] = self.totalSafety
        # dict['safetyParams'] = {"danger" : self.danger , "safety" : self.safety}
        dict['nonDropSoldier'] = self.nonDropSoldier
        dict['currentPoint'] = self.currentPoint
        dict['nextTurnSoldier'] = self.nextTurnSoldier
        dict['soldiers'] = self.soldiers
        return dict
        
    def buildDsu(self) :
        self.dsuPar = [i for i in range(mapp.n)]
        self.dsuSize = [1 for i in range(mapp.n)]
        self.dsuHomie = [self.proxyMap.verts[i].team == self.playerId for i in range(mapp.n)]
        self.dsuHist = []
        self.ci2 = len(self.vertices)
        for v in self.vertices :
            for u in mapp.adj[v] :
                if self.proxyMap.verts[u].team == self.playerId : self.mergeDsu(v , u)
    
    def parDsu(self , u) : 
        if self.dsuPar[u] == u : return u
        return self.parDsu(self.dsuPar[u])
    
    def mergeDsu(self , v , u) : # us - someone
        v = self.parDsu(v)
        u = self.parDsu(u)
        if u == v : return
        if self.dsuSize[u] > self.dsuSize[v] :
            u , v = v , u
        # if self.dsuHomie[v] :   always this is true
        self.ci2 -= self.dsuSize[v] * self.dsuSize[v]
        if self.dsuHomie[u] : self.ci2 -= self.dsuSize[u] * self.dsuSize[u]
        
        self.dsuPar[u] = v
        self.dsuSize[v] += self.dsuSize[u]
        
        self.ci2 += self.dsuSize[v] * self.dsuSize[v]
        self.dsuHist.append(u)
        
    def undoDsu(self , u) : 
        v = self.dsuPar[u]
        
        self.ci2 -= self.dsuSize[v] * self.dsuSize[v]
        
        self.dsuSize[v] -= self.dsuSize[u]
        self.dsuPar[u] = u
        
        self.ci2 += self.dsuSize[v] * self.dsuSize[v]
        if self.dsuHomie[u] : self.ci2 += self.dsuSize[u] * self.dsuSize[u]
        
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
    
    def updatePlayer(self , data : ProxyMap.Player) :
        
        self.nextTurnSoldier += 3 * (data.hadSuccessInAttack - self.hadSuccesfulAttack)
        self.hadSuccesfulAttack = data.hadSuccessInAttack
        self.nonDropSoldier = data.nonDropSoldier
        
        self.proxyMap.players[self.playerId] = data
    
    def updateVertex(self , v : int , data : ProxyMap.Vert) :
        global updateTime
        updateTime -= time.time()
        self.totalSafety *= self.numberOfBorders + 1
        lastData = self.proxyMap.verts[v]
        flag = 0
        if lastData.team != data.team :
            if self.playerId == lastData.team :
                flag = -1
            elif self.playerId == data.team : 
                flag = 1
        
        if flag > 0:
            # print("here flag 1")
            self.dsuHomie[v] = True
            self.ci2 += 1
            self.nextTurnSoldier -= len(self.vertices) // 4 + self.hadSuccesfulAttack * 3
            self.vertices.append(v)
            self.currentPoint += 1
            self.nextTurnSoldier += len(self.vertices) // 4 + self.hadSuccesfulAttack * 3
            if v in mapp.strategicVerts:
                self.numStrat += 1
                self.currentPoint += 3 / mapp.verts[v].strategicPts
                self.nextTurnSoldier += mapp.verts[v].strategicPts
            self.dsuHist.append(-1)
            for u in mapp.adj[v]:
                if self.proxyMap.verts[u].team == self.playerId:
                    self.mergeDsu(u, v)
            self.soldiers += data.numNorm + data.numDef
            self.currentPoint += data.numNorm / 1000 + data.numDef/1000
            
        elif flag == 0 : 
            # print("here falg 0")
            self.currentPoint -= self.soldiers/1000
            self.soldiers -= lastData.numNorm + lastData.numDef
            self.soldiers += data.numNorm + data.numDef
            self.currentPoint += self.soldiers/1000
            
        else :
            self.nextTurnSoldier-=len(self.vertices) // 4 + self.hadSuccesfulAttack * 3
            self.currentPoint-= (lastData.numNorm + lastData.numDef)/1000 + 1
            if mapp.verts[v].strategicPts > 0 :
                self.numStrat -= 1
                self.currentPoint -= 3 / mapp.verts[v].strategicPts
                self.nextTurnSoldier -= mapp.verts[v].strategicPts
            self.soldiers-= lastData.numNorm + lastData.numDef
            # print("here flag -1")
            hst = self.dsuHist.pop()
            while hst >= 0 :
                self.undoDsu(hst)
                hst = self.dsuHist.pop()
            self.dsuHomie[v] = False
            self.ci2 -= 1
            self.vertices.pop() # guaranty v is at the end of vertices
            self.nextTurnSoldier+=len(self.vertices) // 4 + self.hadSuccesfulAttack * 3
            

        #safety : 
        # self.totalSafety
        # self.safety[]    alpha * 
        # self.danger[]    a * pow2(powELossRemain1) + b * pow2(powELossRemain2)
        # self.sqy[]       sigma(y) sqrt(y)
        # self.normy[]     sigma(y) y
        # self.powy[]      sigma(y) pow2(y)
        # self.powELossRemain1[]    sigma(u) pow2(E(loss[v] + remaining[u]))
        # self.powELossRemain2[]    sigma(u) pow2(E(loss[v] + remaining[u]))
        
        def removeSafety(v : int , u : int) :
            if self.proxyMap.verts[v].team != self.playerId or self.proxyMap.verts[u].team == -1 : return
            if self.proxyMap.verts[u].team == self.playerId :
                self.sqy[v]-=math.sqrt(self.proxyMap.verts[u].numNorm)
                self.normy[v] -= self.proxyMap.verts[u].numNorm
                self.powy[v] -= self.proxyMap.verts[u].numNorm * self.proxyMap.verts[u].numNorm
            elif (self.proxyMap.verts[u].team + 1) % 3 == self.playerId :
                self.cntMarzi[v]-=1
                if (self.cntMarzi[v]==0) : 
                    self.numberOfBorders-=1
                n = self.proxyMap.verts[u].numNorm
                m = self.proxyMap.verts[v].numDef + self.proxyMap.verts[u].numNorm
                simulatedAttack = staticData.getState(n , m)
                self.powELossRemain1[v] -= pow2(simulatedAttack[6][0] + m - simulatedAttack[6][1])
            else :
                self.cntMarzi[v]-=1
                if (self.cntMarzi[v]==0) : 
                    self.numberOfBorders-=1
                n = self.proxyMap.verts[u].numNorm
                m = self.proxyMap.verts[v].numDef + self.proxyMap.verts[u].numNorm
                simulatedAttack = staticData.getState(n , m)
                self.powELossRemain2[v] -= pow2(simulatedAttack[6][0] + m - simulatedAttack[6][1])
        
        def addSafety(v : int , u : int) :
            if self.proxyMap.verts[v].team != self.playerId or self.proxyMap.verts[u].team == -1 : return
            if self.proxyMap.verts[u].team == self.playerId :
                self.sqy[v]+=math.sqrt(self.proxyMap.verts[u].numNorm)
                self.normy[v] += self.proxyMap.verts[u].numNorm
                self.powy[v] += self.proxyMap.verts[u].numNorm * self.proxyMap.verts[u].numNorm
            elif (self.proxyMap.verts[u].team + 1) % 3 == self.playerId :
                self.cntMarzi[v]+=1
                if (self.cntMarzi[v]==1) : 
                    self.numberOfBorders+=1
                n = self.proxyMap.verts[u].numNorm
                m = self.proxyMap.verts[v].numDef + self.proxyMap.verts[u].numNorm
                simulatedAttack = staticData.getState(n , m) # problem?
                self.powELossRemain1[v] += pow2(simulatedAttack[6][0] + m - simulatedAttack[6][1])
            else :
                self.cntMarzi[v]+=1
                if (self.cntMarzi[v]==1) : 
                    self.numberOfBorders+=1
                n = self.proxyMap.verts[u].numNorm
                m = self.proxyMap.verts[v].numDef + self.proxyMap.verts[u].numNorm
                simulatedAttack = staticData.getState(n , m)
                self.powELossRemain2[v] += pow2(simulatedAttack[6][0] + m - simulatedAttack[6][1])
        
        mapp.adj[v].append(v)
        for i in mapp.adj[v] : 
            if (self.proxyMap.verts[i].team==self.playerId and self.cntMarzi[i] > 0) : 
                self.totalSafety-= math.sqrt(self.safety[i]/math.sqrt(self.danger[i]))
        mapp.adj[v].pop()
        
        for u in mapp.adj[v] :
            removeSafety(v , u)
            removeSafety(u , v)
            
        lastData.team = data.team
        lastData.numNorm = data.numNorm
        lastData.numDef = data.numDef
        
        for u in mapp.adj[v] :
            addSafety(v , u)
            addSafety(u , v)
        
        mapp.adj[v].append(v)
        for i in mapp.adj[v] : 
            if (self.proxyMap.verts[i].team==self.playerId and self.cntMarzi[i] > 0) : 
                self.danger[i] = self.powELossRemain1[i] * self.powELossRemain1[i] + self.safetyB*self.powELossRemain2[i]*self.powELossRemain2[i]
                self.safety[i] = self.sqy[i] + self.safetyBeta * self.normy[i] + self.safetyLanda * self.powy[i] 
                self.safety[i] += self.safetyMu * (self.proxyMap.verts[i].numDef + self.proxyMap.verts[i].numNorm)
                self.totalSafety+= math.sqrt(self.safety[i]/math.sqrt(self.danger[i]))
        self.totalSafety /= self.numberOfBorders + 1
        mapp.adj[v].pop()
        updateTime += time.time()
        
    
    def calculateValue(self) :
        value = 0
        value += pow(3 , self.numStrat) * genomee.data['numStrat']
        value += genomee.data['connectivity'] * self.ci2 / len(self.vertices) / len(self.vertices)
        value += self.totalSafety * genomee.data['totalSafety']
        value += self.nonDropSoldier * genomee.data['nonDropSoldier']
        value += self.currentPoint * genomee.data["currentPoint"]
        value += self.nextTurnSoldier * genomee.data["nextTurnSoldier"]
        value += self.soldiers * genomee.data["soldiers"]
        return value
    
# testing