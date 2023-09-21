
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
    def __init__(self) :
        self.numStratMulti = .1
        self.connectivityMulti = .1
        self.nonDropSoldierMulti = .1
        self.currentPointMulti = .1
        self.nextTurnSoldierMulti = .1
        self.soldiersMulti = .1
class HuristicFunction :
    @staticmethod
    def dfs(map : Map , proxyMap : ProxyMap , playerId , seen , v) :
        seen[v] = True
        sz = 1
        for u in map.adj[v] :
            if not seen[u] :
                if proxyMap.verts[u] == playerId :
                    sz += HuristicFunction.dfs(map , proxyMap , playerId , seen , u)
        return sz
    
    def __init__(self , map : Map , proxyMap : ProxyMap , genome : Genome , playerId : int) :
        #num strat
        self.numStrat = 0
        self.numberOfvertices = 0
        self.stratList = []
        self.soldiers = 0
        self.currentPoint = 0
        self.nextTurnSoldier = 0
        for v in range(map.n) :
            if proxyMap.verts[v].team == playerId :
                self.numberOfvertices += 1
                self.soldiers += proxyMap.verts[v].numNorm
                if map.verts[v].strategicPts > 0 :
                    self.nextTurnSoldier += map.verts[v].strategicPts
                    self.currentPoint += 3000 / map.verts[v].strategicPts
                    self.stratList.append(proxyMap.verts[v])
                    self.numStrat += 1
        self.value += self.numStrat * genome.numStratMulti
        
        #sigma (Ci/n)^2
        self.ci2 = 0
        self.numLand = 0
        seen = [False for i in range(map.n)]
        for v in range(map.n) :
            if not seen[v] :
                if proxyMap.verts[u] == playerId :
                    x = HuristicFunction.dfs(map , proxyMap , playerId , seen , v)
                    self.numLand += x
                    self.ci2 += x * x
        self.value += genome.connectivityMulti * self.ci2 / self.numLand / self.numLand
        
        #soldiers in hand
        self.nonDropSoldier = proxyMap.players[playerId].nonDropSoldier
        #current point :(sigma 1000ras + sigma 3000/pi + |soldier|)/1000
            # self.numberOfvertices bala tarif shode 
            # self.stratList bala tarif shode 
            # self.soldiers  bala tarif shode
        self.hadSuccesfulAttack = proxyMap.players[playerId].hadSuccessInAttack
        self.currentPoint += self.numberOfvertices * 1000 + self.soldiers
        #next turn soldier : sigma pi + |ras|/4 + (succesful attack)*3
        self.nextTurnSoldier += self.numberOfvertices // 4 + self.hadSuccesfulAttack * 3
        #safety
        
        #|soldier| 
            # self.soldiers  bala tarif shode
        # value
        self.value = self.numStrat * genome.numStratMulti + self.ci2 / self.numLand / self.numLand * genome.connectivityMulti + self.nonDropSoldier * genome.nonDropSoldierMulti
        self.value += self.currentPoint * genome.self.currentPointMulti + self.nextTurnSoldier * genome.nextTurnSoldierMulti + self.soldiers * genome.soldiers
    
    def captureVertex(self , map : Map , proxyMap : ProxyMap , genome : Genome , playerId : int , v) :
        x = 0
    
# testing