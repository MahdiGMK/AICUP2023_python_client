import json

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
            self.numNorm = num_norm
            self.numDef = num_def
    class Player :
        def __init__(self) :
            self.nonDropSoldier = 0
            self.doneFort = False
            self.hadSuccessInAttack = False
    def __init__(self , map : Map, numPlayers : int, actions : list) : 
        self.players = [self.Player() for i in range(numPlayers)]
        self.verts = [self.Vert(-1 , 0 , 0) for i in range(map.n)]
        self.actions = actions
        
class Genome :
    def __init__(self , path) :
        fl = open(path)
        self.data = json(fl)

class StaticData : 
    def __init__(self) :
        fl = jsopen("States.json" , "r")
        self.states = json.load(fl)
        fl.close()
def pow2(num) : 
    return num * num
class HuristicFunction :
    @staticmethod
    def dfs(map : Map , proxyMap : ProxyMap , playerId : int , seen : list , v : int) :
        seen[v] = True
        self.vertices.append(v)
        self.soldiers += proxyMap.verts[v].numNorm + proxyMap.verts[v].numDef
        self.currentPoint += 1000
        if map.verts[v].strategicPts > 0 :
            self.nextTurnSoldier += map.verts[v].strategicPts
            self.currentPoint += 3000 / map.verts[v].strategicPts
            self.numStrat += 1
        sz = 1
        for u in map.adj[v] :
            if  proxyMap.verts[u].team == playerId:
                self.sqy[v]+=math.sqrt(proxyMap.verts[u].numNorm)
                self.normy[v] += proxyMap.verts[u].numNorm
                self.powy[v] += proxyMap.verts[u].numNorm * proxyMap.verts[u].numNorm
            elif proxyMap.verts[u].team != -1 and (proxyMap.verts[u].team+1)%3==playerId:
                n = proxyMap.verts[u].numNorm
                m = proxyMap.verts[v].numDef + proxyMap.verts[u].numNorm
                simulatedAttack = StaticData.states[n][m]
                self.PowELossRemain1 += pow2(simulatedAttack[1][0] + m - simulatedAttack[1][1])
            elif proxyMap.verts[u].team != -1 and (proxyMap.verts[u].team+2)%3==playerId:
                n = proxyMap.verts[u].numNorm
                m = proxyMap.verts[v].numDef + proxyMap.verts[u].numNorm
                simulatedAttack = StaticData.states[n][m]
                self.PowELossRemain2 += pow2(simulatedAttack[1][0] + m - simulatedAttack[1][1])
            if not seen[u] :
                if proxyMap.verts[u].team == playerId :
                    sz += HuristicFunction.dfs(map , proxyMap , playerId , seen , u)
                    
        return sz
    
    def __init__(self , map : Map , proxyMap : ProxyMap , genome : Genome , playerId : int) :
        #num strat
        self.vertices = []
        self.numStrat = 0
        self.soldiers = 0
        self.currentPoint = 0
        self.nextTurnSoldier = 0

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
        seen = [False for i in range(map.n)]
        for v in range(map.n) :
            if not seen[v] :
                if proxyMap.verts[u] == playerId :
                    x = HuristicFunction.dfs(map , proxyMap , playerId , seen , v)
                    self.ci2 += x * x

        #safety again
        for i in self.vertices : 
            b = genome.data['saftyB']
            beta = genome.data['saftyBata']
            landa = genome.data['saftyLanda']
            mu = genome.data['saftyMu']
            if (proxyMap.verts[i].team==playerId and self.powELossRemain1[i] + self.powELossRemain2[i] > 0) : 
                self.danger = self.powELossRemain1[i]**2 + b*self.powELossRemain2[i]**2
                self.safety = self.sqy[i] +beta*self.normy[i] + landa * self.powy[i] 
                self.safety += mu * (proxyMap.verts[i].numDef + proxyMap.verts[i].numNorm)
                self.numberOfBorders += 1
                self.totalSafety+= math.sqrt(self.safety/math.sqtr(self.danger))
        self.totalSafety/=self.numberOfBorders
        
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
        self.nextTurnSoldier += self.numberOfvertices // 4 + self.hadSuccesfulAttack * 3

        
        #|soldier| 
            # self.soldiers  bala tarif shode
    
        # value
        self.value += self.numStrat * genome.data['numStrat']
        self.value += genome.data['connectivity'] * self.ci2 / len(self.vertices) / len(self.vertices)
        self.value += self.totalSafety * genome.data['totalSafety']
        self.value += self.nonDropSoldier * genom.data['nonDropSoldier']
        self.value += self.currentPoint * genome.data["currentPoint"]
        self.value += self.nextTurnSoldier * genome.data["nextTurnSoldier"]
        self.value += self.soldiers * genome.data["soldiers"]
    
    def updateVertex(self , map : Map , proxyMap : ProxyMap , genome : Genome , playerId : int , v : int , data : ProxyMap.Vert) :
        x = 0 # todo
    def undoDSU(self , map : Map , proxyMap : ProxyMap , genome : Genome , playerId : int) :
        x = 0 # todo
    
# testing