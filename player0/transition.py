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

def attackBeamSearch(HR0: HuristicFunction, beta: int, depth: int, playerId: int, turn: int):
    risk_rate = 3
    simulate_rate = 4
    Q = [[(0 , -1 , Movement(MoveKind.Nothing , []) , HR0)]]
    for i in range(depth) : Q.append([])
    
    HR0.buildDsu()
    current_depth = 0
    while current_depth < depth:
        qp = []
        for idx in range(len(Q[current_depth])):
            q = Q[current_depth][idx]
            hr = q[3]

            qp.append([hr.calculateValue(), Movement(MoveKind.Nothing, []), idx])
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
                    
                    qp.append([hr.calculateValue(), movement, i])
                    
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

    return Q[depth]


def dropSoldierBeamSearch(Hr0 : HuristicFunction , beta : int , depth : int , playerId : int , turn : int) :
    x = 0 # todo