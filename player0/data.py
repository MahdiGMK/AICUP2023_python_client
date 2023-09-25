import json
import math

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
        def __init__(self , nonDropSoldier = 0 , doneFort = False , hadSuccessInAttack = False) :
            self.nonDropSoldier = nonDropSoldier
            self.doneFort = doneFort
            self.hadSuccessInAttack = hadSuccessInAttack
    def __init__(self , map : Map, numPlayers : int, actions : list) : 
        self.players = [self.Player() for i in range(numPlayers)]
        self.verts = [self.Vert(-1 , 0 , 0) for i in range(map.n)]
        self.actions = actions
        
class Genome :
    def __init__(self , path) :
        fl = open(path)
        self.data = json.load(fl)

class StaticData : 
    def __init__(self) :
        fl = open("../States.json" , "r")
        self.states = json.load(fl)
        fl.close()
staticData = StaticData()

def pow2(num) : 
    return num * num
class HuristicFunction :
    def dfs(self , v : int) :
        self.seen[v] = True
        self.vertices.append(v)
        self.soldiers += self.proxyMap.verts[v].numNorm + self.proxyMap.verts[v].numDef
        self.currentPoint += 1000
        if self.map.verts[v].strategicPts > 0 :
            self.nextTurnSoldier += self.map.verts[v].strategicPts
            self.currentPoint += 3000 / self.map.verts[v].strategicPts
            self.numStrat += 1
        sz = 1
        for u in self.map.adj[v] :
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
                simulatedAttack = staticData.states[n][m] # problem?
                self.powELossRemain1[v] += pow2(simulatedAttack[6][0] + m - simulatedAttack[6][1])
            else :
                self.cntMarzi[v]+=1
                if (self.cntMarzi[v]==1) : 
                    self.numberOfBorders+=1
                n = self.proxyMap.verts[u].numNorm
                m = self.proxyMap.verts[v].numDef + self.proxyMap.verts[u].numNorm
                simulatedAttack = staticData.states[n][m] # problem?
                self.powELossRemain2[v] += pow2(simulatedAttack[6][0] + m - simulatedAttack[6][1])
            if not self.seen[u] :
                if self.proxyMap.verts[u].team == self.playerId :
                    sz += self.dfs(u)
                    
        return sz
    
    def __init__(self , map : Map , proxyMap : ProxyMap , genome : Genome , playerId : int) :
        self.map = map
        self.proxyMap = proxyMap
        self.genome = genome
        self.playerId = playerId
        #num strat
        self.vertices = []
        self.numStrat = 0
        self.soldiers = 0
        self.currentPoint = 0
        self.nextTurnSoldier = 0
        self.cntMarzi = [0 for i in range(map.n)]

        #safety (sigma (Pi/Di^1/2))  /|marzi|
        # danger[v] = sigma^2 E^2(loss[v] + remaining[u]) + b * sigma^2 E^2(loss[v] + remaining[u])
        # safety[v] =  sigma y^1/2 + b * sigma y + c b * sigma y^2 + m*X 
        self.totalSafety = 0
        self.safety = [0 for i in range(map.n)]
        self.danger = [0 for i in range(map.n)]
        self.sqy = [0 for i in range(map.n)]
        self.normy = [0 for i in range(map.n)]
        self.powy = [0 for i in range(map.n)]
        self.powELossRemain1 = [0 for i in range(map.n)]
        self.powELossRemain2 = [0 for i in range(map.n)]
        self.numberOfBorders = 0

        #sigma (Ci/n)^2
        self.ci2 = 0
        self.seen = [False for i in range(map.n)]
        for v in range(map.n) :
            if not self.seen[v] :
                if proxyMap.verts[v].team == playerId :
                    x = self.dfs(v)
                    self.ci2 += x * x

        #safety again
        
        self.safetyB = genome.data['saftyB']
        self.safetyBeta = genome.data['saftyBata']
        self.safetyLanda = genome.data['saftyLanda']
        self.safetyMu = genome.data['saftyMu']
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
        self.dsuPar = [i for i in range(self.map.n)]
        self.dsuSize = [1 for i in range(self.map.n)]
        self.dsuHomie = [self.proxyMap.verts[i].team == self.playerId for i in range(self.map.n)]
        self.dsuHist = []
        self.ci2 = len(self.vertices)
        for v in self.vertices :
            for u in self.map.adj[v] :
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
        self.nonDropSoldier += data.nonDropSoldier
        
        self.proxyMap.players[self.playerId] = data
    
    def updateVertex(self , v : int , data : ProxyMap.Vert) :
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
            if v in self.map.strategicVerts:
                self.numStrat += 1
                self.currentPoint += 3 / self.map.verts[v].strategicPts
                self.nextTurnSoldier += self.map.verts[v].strategicPts
            self.dsuHist.append(-1)
            for u in self.map.adj[v]:
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
            if self.map.verts[v].strategicPts > 0 :
                self.numStrat -= 1
                self.currentPoint -= 3 / self.map.verts[v].strategicPts
                self.nextTurnSoldier -= self.map.verts[v].strategicPts
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
                simulatedAttack = staticData.states[n][m] # problem?
                self.powELossRemain1[v] -= pow2(simulatedAttack[6][0] + m - simulatedAttack[6][1])
            else :
                self.cntMarzi[v]-=1
                if (self.cntMarzi[v]==0) : 
                    self.numberOfBorders-=1
                n = self.proxyMap.verts[u].numNorm
                m = self.proxyMap.verts[v].numDef + self.proxyMap.verts[u].numNorm
                simulatedAttack = staticData.states[n][m] # problem?
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
                simulatedAttack = staticData.states[n][m] # problem?
                self.powELossRemain1[v] += pow2(simulatedAttack[6][0] + m - simulatedAttack[6][1])
            else :
                self.cntMarzi[v]+=1
                if (self.cntMarzi[v]==1) : 
                    self.numberOfBorders+=1
                n = self.proxyMap.verts[u].numNorm
                m = self.proxyMap.verts[v].numDef + self.proxyMap.verts[u].numNorm
                simulatedAttack = staticData.states[n][m] # problem?
                self.powELossRemain2[v] += pow2(simulatedAttack[6][0] + m - simulatedAttack[6][1])
        
        self.map.adj[v].append(v)
        for i in self.map.adj[v] : 
            if (self.proxyMap.verts[i].team==self.playerId and self.cntMarzi[i] > 0) : 
                self.totalSafety-= math.sqrt(self.safety[i]/math.sqrt(self.danger[i]))
        self.map.adj[v].pop()
        
        for u in self.map.adj[v] :
            removeSafety(v , u)
            removeSafety(u , v)
            
        lastData.team = data.team
        lastData.numNorm = data.numNorm
        lastData.numDef = data.numDef
        
        for u in self.map.adj[v] :
            addSafety(v , u)
            addSafety(u , v)
        
        self.map.adj[v].append(v)
        for i in self.map.adj[v] : 
            if (self.proxyMap.verts[i].team==self.playerId and self.cntMarzi[i] > 0) : 
                self.danger[i] = self.powELossRemain1[i] * self.powELossRemain1[i] + self.safetyB*self.powELossRemain2[i]*self.powELossRemain2[i]
                self.safety[i] = self.sqy[i] + self.safetyBeta * self.normy[i] + self.safetyLanda * self.powy[i] 
                self.safety[i] += self.safetyMu * (self.proxyMap.verts[i].numDef + self.proxyMap.verts[i].numNorm)
                self.totalSafety+= math.sqrt(self.safety[i]/math.sqrt(self.danger[i]))
        self.totalSafety /= self.numberOfBorders + 1
        self.map.adj[v].pop()
        
    
    def calculateValue(self) :
        value = 0
        value += pow(3 , self.numStrat) * self.genome.data['numStrat']
        value += self.genome.data['connectivity'] * self.ci2 / len(self.vertices) / len(self.vertices)
        value += self.totalSafety * self.genome.data['totalSafety']
        value += self.nonDropSoldier * self.genome.data['nonDropSoldier']
        value += self.currentPoint * self.genome.data["currentPoint"]
        value += self.nextTurnSoldier * self.genome.data["nextTurnSoldier"]
        value += self.soldiers * self.genome.data["soldiers"]
        return value
    
# testing