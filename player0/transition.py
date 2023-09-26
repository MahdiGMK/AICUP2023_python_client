import copy
from enum import Enum 
from data import *


class MoveKind(Enum) :
    Nothing = 0
    DropSoldier = 1
    Attack = 2
    Fort = 3
class Movement:
    def __init__(self, kind: MoveKind, move: list):
        self.kind = kind
        self.move = move
    def __repr__(self) :
        return f"{self.kind} : {self.move}"
    def __str__(self) :
        return f"Movement ({self.kind} , {self.move})"
    
def attackBeamSearch(HR0: list[HuristicFunction], beta: int, depth: int, playerId: int, turn: int , simulateRate : int):
    risk_rate = HR0[0].genome.data["riskRate"]
    Q = [[]]
    for hr in HR0 :
        Q[0].append((0 , -1 , Movement(MoveKind.Nothing , []) , hr))
    for i in range(depth) : Q.append([])
    
    HR0.buildDsu()
    current_depth = 0
    while current_depth < depth:
        qp = []
        for idx in range(len(Q[current_depth])):
            q = Q[current_depth][idx]
            hr = q[3]

            qp.append((hr.calculateValue(), Movement(MoveKind.Nothing, []), idx))
            if q[0] < current_depth :
                continue
            
            for v in hr.vertices:
                n = hr.proxyMap.verts[v].numNorm
                if n <= 1 or hr.cntMarzi[v] == 0:
                    continue
                for u in hr.map.adj[v]:
                    if hr.proxyMap.verts[u].team == playerId or hr.proxyMap.verts[u].team == -1:
                        continue
                    
                    m = hr.proxyMap.verts[u].numNorm + hr.proxyMap.verts[u].numDef
                    st = staticData.getState(n, m)
                    
                    if st[risk_rate][1] > 0:
                        continue
                    
                    movement = Movement(MoveKind.Attack, [v, u])
                    
                    hist_v = (hr.proxyMap.verts[v].numNorm, hr.proxyMap.verts[v].numDef)
                    hist_u = (hr.proxyMap.verts[u].numNorm, hr.proxyMap.verts[u].numDef)
                    hist_id_u = hr.proxyMap.verts[u].team
                    
                    hr.updateVertex(v, ProxyMap.Vert(playerId, 1, hr.proxyMap.verts[v].numDef))
                    hr.updateVertex(u, ProxyMap.Vert(playerId, st[risk_rate][0] - 1, 0))
                    if current_depth == 0 :
                        hr.updatePlayer(ProxyMap.Player(nonDropSoldier=hr.proxyMap.players[playerId].nonDropSoldier , doneFort=hr.proxyMap.players[playerId] , hadSuccessInAttack=True))
                    
                    qp.append((hr.calculateValue(), movement, idx))
                    
                    if current_depth == 0 :
                        hr.updatePlayer(ProxyMap.Player(nonDropSoldier=hr.proxyMap.players[playerId].nonDropSoldier , doneFort=hr.proxyMap.players[playerId] , hadSuccessInAttack=False))
                    hr.updateVertex(v, ProxyMap.Vert(playerId, hist_v[0], hist_v[1]))
                    hr.updateVertex(u, ProxyMap.Vert(hist_id_u, hist_u[0], hist_u[1]))
        qp.sort(key=lambda x: x[0], reverse=True)
        new_q = Q[current_depth + 1]
        for i in range(min(beta, len(qp))):
            movement = qp[i][1]
            ind = qp[i][2]
            q = Q[current_depth][ind]
            hr = q[3]
            if movement.kind == MoveKind.Nothing:
                new_q.append((q[0] , ind , movement , hr))
                continue
            v = movement.move[0]
            u = movement.move[1]

            n = hr.proxyMap.verts[v].numNorm
            m = hr.proxyMap.verts[u].numNorm + hr.proxyMap.verts[u].numDef
            st = staticData.getState(n, m)

            hist_v = [hr.proxyMap.verts[v].numNorm, hr.proxyMap.verts[v].numDef]
            hist_u = [hr.proxyMap.verts[u].numNorm, hr.proxyMap.verts[u].numDef]
            hist_id_u = hr.proxyMap.verts[u].team

            hr = copy.deepcopy(hr)
            hr.updateVertex(v, ProxyMap.Vert(playerId, 1, hr.proxyMap.verts[v].numDef))
            hr.updateVertex(u, ProxyMap.Vert(playerId, st[risk_rate][0] - 1, 0))

            new_q.append((q[0] + 1 , ind , movement, hr))
        current_depth += 1

    res = []
    
    for i in range(len(Q[depth])) :
        path = []
        res.append(path)
        dep = depth
        ind = i
        while dep > 0 :
            path.append(Q[dep][ind][2])
            ind = Q[dep][ind][1]
            dep -= 1
        path.append(Q[depth][i][3])
        path.reverse()
    
    return res

def dropSoldier(hr : HuristicFunction , beta : int , depth : int , playerId : int , turn : int) : 
    hr.buildDsu()
    cnt = hr.proxyMap.players[playerId].nonDropSoldier
    qp = []
    hr.updatePlayer(ProxyMap.Player(nonDropSoldier=0 , doneFort=hr.proxyMap.players[playerId].doneFort))
    lst = []
    for v in hr.vertices :
        if hr.cntMarzi[v] == 0 : continue
        lst.append(v)
        for u in hr.map.adj[v] :
            if hr.proxyMap.verts[u].team == -1 :
                lst.append(v)
    lst = set(lst)
    for v in lst : 
        hst = (hr.proxyMap.verts[v].team , hr.proxyMap.verts[v].numNorm , hr.proxyMap.verts[v].numDef)
        hr.updateVertex(v , ProxyMap.Vert(playerId , hr.proxyMap.verts[v].numNorm + cnt , hr.proxyMap.verts[v].numDef))
        qp.append((hr.calculateValue() , Movement(MoveKind.DropSoldier , [v , cnt])))
        hr.updateVertex(v , ProxyMap.Vert(hst[0] , hst[1] , hst[2]))
    hr.updatePlayer(ProxyMap.Player(nonDropSoldier=cnt , doneFort=hr.proxyMap.players[playerId].doneFort))
    qp.sort(key=lambda x: x[0], reverse=True)
    Q = []
    for i in range(min(beta, len(qp))):
        move = qp[i][1]
        nhr = copy.deepcopy(hr)
        v = move[0]
        nhr.updatePlayer(ProxyMap.Player(doneFort=hr.proxyMap.players[playerId]))
        nhr.updateVertex(v , ProxyMap.Vert(playerId , hr.proxyMap.verts[v].numNorm + cnt , hr.proxyMap.verts[v].numDef))
        Q.append([nhr , move])
    return Q

def moveSoldierSearch(HR : list[HuristicFunction] , beta : int) : 
    qp = []
    for hr in HR :    
        cnt = hr.proxyMap.players[playerId].nonDropSoldier
        lst = []
        for v in hr.vertices :
            if hr.cntMarzi[v] == 0 : continue
            lst.append(v)
        for v in hr.vertices :
            vNorm = hr.proxyMap.verts[v].numNorm
            vDef  = hr.proxyMap.verts[v].numNorm
            cnt = vNorm // 2
            for u in lst : 
                uNorm = hr.proxyMap.verts[u].numNorm
                uDef  = hr.proxyMap.verts[u].numNorm
                hr.updateVertex(v , ProxyMap.Vert(playerId , vNorm - cnt , vDef))
                hr.updateVertex(u , ProxyMap.Vert(playerId , uNorm + cnt , uDef))
                qp.append((hr.calculateValue() , Movement(MoveKind.Move , [v , u , cnt])))
                hr.updateVertex(v , ProxyMap.Vert(playerId , vNorm , vDef))
                hr.updateVertex(u , ProxyMap.Vert(playerId , uNorm , uDef))
    qp.sort(key=lambda x: x[0], reverse=True)
    Q = []
    for i in range(min(beta, len(qp))):
        move = qp[i][1]
        nhr = copy.deepcopy(hr)
        v = move[0]
        u = move[1]
        cnt = move[2]
        vNorm = hr.proxyMap.verts[v].numNorm
        vDef  = hr.proxyMap.verts[v].numNorm
        uNorm = hr.proxyMap.verts[u].numNorm
        uDef  = hr.proxyMap.verts[u].numNorm
        nhr.updateVertex(v , ProxyMap.Vert(playerId , vNorm - cnt , vDef))
        nhr.updateVertex(u , ProxyMap.Vert(playerId , uNorm + cnt , uDef))
        Q.append([nhr , move])
    return Q