import copy
from enum import Enum
import data as pd
from data import *
import data


class MoveKind(Enum):
    Nothing = 0
    DropSoldier = 1
    Move = 2
    Attack = 3
    Fort = 4


class Movement:
    def __init__(self, kind: MoveKind, move: list):
        self.kind = kind
        self.move = move

    def __repr__(self):
        return f"{self.kind} : {self.move}"

    def __str__(self):
        return f"Movement ({self.kind} , {self.move})"


def attackBeamSearch(HR0: list[(HuristicFunction, [Movement])], beta: int, depth: int, playerId: int, turn: int,
                     simulateRate: int):
    risk_rate = pd.genomee.data["riskRate"]
    Q = [[]]
    for hr in HR0:
        Q[0].append((0, -1, hr[1], hr[0]))
    for i in range(depth): Q.append([])

    current_depth = 0
    while current_depth < depth:
        qp = []
        for idx in range(len(Q[current_depth])):
            q = Q[current_depth][idx]
            hr = q[3]

            qp.append((hr.calculateValue(), Movement(MoveKind.Nothing, []), idx))
            if q[0] < current_depth:
                continue

            for v in hr.vertices:
                n = hr.proxyMap.verts[v].numNorm
                if n <= 1 or hr.cntMarzi[v] == 0:
                    continue
                for u in pd.mapp.adj[v]:
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
                    hr.updateVertex(u, ProxyMap.Vert(playerId, st[simulateRate][0] - 1, 0))
                    if current_depth == 0:
                        hr.updatePlayer(ProxyMap.Player(nonDropSoldier=hr.proxyMap.players[playerId].nonDropSoldier,
                                                        doneFort=hr.proxyMap.players[playerId],
                                                        hadSuccessInAttack=True))

                    qp.append((hr.calculateValue(), movement, idx))

                    if current_depth == 0:
                        hr.updatePlayer(ProxyMap.Player(nonDropSoldier=hr.proxyMap.players[playerId].nonDropSoldier,
                                                        doneFort=hr.proxyMap.players[playerId],
                                                        hadSuccessInAttack=False))
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
                new_q.append((q[0], ind, movement, hr))
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
            hr.updateVertex(u, ProxyMap.Vert(playerId, st[simulateRate][0] - 1, 0))

            new_q.append((q[0] + 1, ind, movement, hr))
        current_depth += 1

    res = []

    for i in range(len(Q[depth])):
        path = [0, []]
        res.append(path)
        if (turn):
            dep = depth
            ind = i
            while dep > 0:
                path[1].append(Q[dep][ind][2])
                ind = Q[dep][ind][1]
                dep -= 1
            path[1] += Q[0][ind][2]
        path[0] = Q[depth][i][3]
        path[1].reverse()

    return res


def dropSoldier(HR: [HuristicFunction], beta: int, depth: int, playerId: int, turn: int):
    qp = []
    for hr in HR:
        hr.buildDsu()
        cnt = hr.proxyMap.players[playerId].nonDropSoldier
        hr.updatePlayer(ProxyMap.Player(nonDropSoldier=0, doneFort=hr.proxyMap.players[playerId].doneFort))
        lst = []
        for v in hr.vertices:
            if hr.cntMarzi[v] == 0:
                continue
            lst.append(v)
            for u in pd.mapp.adj[v]:
                if hr.proxyMap.verts[u].team == -1:
                    lst.append(v)
        lst = set(lst)
        for v in lst:
            hst = (hr.proxyMap.verts[v].team, hr.proxyMap.verts[v].numNorm, hr.proxyMap.verts[v].numDef)
            hr.updateVertex(v, ProxyMap.Vert(playerId, hr.proxyMap.verts[v].numNorm + cnt, hr.proxyMap.verts[v].numDef))
            qp.append((hr.calculateValue(), Movement(MoveKind.DropSoldier, [v, cnt])))
            hr.updateVertex(v, ProxyMap.Vert(hst[0], hst[1], hst[2]))
        hr.updatePlayer(ProxyMap.Player(nonDropSoldier=cnt, doneFort=hr.proxyMap.players[playerId].doneFort))
    qp.sort(key=lambda x: x[0], reverse=True)
    Q = []
    for i in range(min(beta, len(qp))):
        move = qp[i][1]
        nhr = copy.deepcopy(hr)
        v = move.move[0]
        nhr.updatePlayer(ProxyMap.Player(doneFort=hr.proxyMap.players[playerId]))
        nhr.updateVertex(v, ProxyMap.Vert(playerId, hr.proxyMap.verts[v].numNorm + cnt, hr.proxyMap.verts[v].numDef))
        Q.append([nhr, [move]])
    return Q


def moveSoldierSearch(HR: list[HuristicFunction], beta: int, playerId: int):
    qp = []
    id = 0
    for hr in HR:
        lst = []
        for v in hr.vertices:
            if hr.cntMarzi[v] == 0: continue
            lst.append(v)
        for v in hr.vertices:
            vNorm = hr.proxyMap.verts[v].numNorm
            vDef = hr.proxyMap.verts[v].numDef
            cnt = vNorm // 2
            for u in lst:
                if (u == v or hr.proxyMap.verts[u].numNorm < 2):
                    continue
                uNorm = hr.proxyMap.verts[u].numNorm
                uDef = hr.proxyMap.verts[u].numDef
                hr.updateVertex(v, ProxyMap.Vert(playerId, vNorm - cnt, vDef))
                hr.updateVertex(u, ProxyMap.Vert(playerId, uNorm + cnt, uDef))
                qp.append((hr.calculateValue(), Movement(MoveKind.Move, [v, u, cnt]), id))
                hr.updateVertex(v, ProxyMap.Vert(playerId, vNorm, vDef))
                hr.updateVertex(u, ProxyMap.Vert(playerId, uNorm, uDef))
        id += 1
    qp.sort(key=lambda x: x[0], reverse=True)
    Q = []
    for i in range(min(beta, len(qp))):
        move = qp[i][1]
        nhr = copy.deepcopy(HR[qp[i][2]])
        v = move.move[0]
        u = move.move[1]
        cnt = move.move[2]
        vNorm = nhr.proxyMap.verts[v].numNorm
        vDef = nhr.proxyMap.verts[v].numDef
        uNorm = nhr.proxyMap.verts[u].numNorm
        uDef = nhr.proxyMap.verts[u].numDef
        nhr.updateVertex(v, ProxyMap.Vert(playerId, vNorm - cnt, vDef))
        nhr.updateVertex(u, ProxyMap.Vert(playerId, uNorm + cnt, uDef))
        Q.append([nhr, move, qp[i][2]])
    return Q


def beamSearch(HR: list[HuristicFunction], beta: int, playerId: int, turn: int, attackOrMove: int):
    Q = []
    if turn > 1 or attackOrMove:
        dropSoldierList = dropSoldier(HR, playerId=playerId, beta=beta, turn=turn, depth=5)
        for mp in dropSoldierList:
            Q.append((mp[0], mp[1]))
        attackList = attackBeamSearch(Q, beta * 5, 10, playerId, turn, simulateRate=3)
        Q.clear()
        L = []
        for mp in attackList:
            L.append(mp[0])
        moveList = moveSoldierSearch(L, beta, playerId)

        for mp in moveList:
            Q.append((mp[0], attackList[mp[2]][1]))
        return Q
    else:
        moveList = moveSoldierSearch(HR, beta, playerId)
        for mp in moveList:
            Q.append((mp[0], [mp[1]]))

    return Q


def calcStateValue(HR: HuristicFunction, playerId):
    hValues = [0, 0, 0]
    hValues[playerId] = HR.calculateValue()
    hValues[(playerId + 1) % 3] = HuristicFunction(data.mapp, HR.proxyMap, data.genomee,
                                                   (playerId + 1) % 3).calculateValue()
    hValues[(playerId + 2) % 3] = HuristicFunction(data.mapp, HR.proxyMap, data.genomee,
                                                   (playerId + 2) % 3).calculateValue()
    total = 0
    for i in hValues:
        total += i * i
    for i in range(3):
        hValues[i] = hValues[i] * hValues[i] / total
    return hValues


def miniMax(HR: HuristicFunction, beta: int, playerId: int, alpha: [], attackOrMove: int, turn: int, mxDepth: int):
    if turn > mxDepth:
        return calcStateValue(HR, playerId)[playerId]
    bestVal = 0
    Q = beamSearch([copy.deepcopy(HR)], beta, playerId, turn, attackOrMove)
    bestMove = 0
    ind = 0
    for nd in Q:
        value = miniMax(HuristicFunction(data.mapp, nd[0].proxyMap, data.genomee, (playerId + 1) % 3), beta,
                        (playerId + 1) % 3, copy.deepcopy(alpha), 1, turn + 1, mxDepth)
        if bestVal < value:
            bestVal = value
            bestMove = ind
        bestVal = max(bestVal, value)
        alpha[playerId] = max(alpha[playerId], bestVal)
        if sum(alpha) > 1 + 0.001:
            break
        ind += 1
    if turn == 1:
        return Q[bestMove]
    return bestVal
