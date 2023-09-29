import copy
from enum import Enum
import player0.data as pd
from player0.data import *


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


attackBeamSearchTime = 0


def attackBeamSearch(HR0: list[(HuristicFunction, [Movement])], beta: int, depth: int, playerId: int, turn: int):
    global attackBeamSearchTime
    attackBeamSearchTime -= time.time()
    risk_rate = int(pd.genomee.data["riskRate"])
    simulateRate = int(pd.genomee.data["riskSimulate1"])
    if turn%3!=1 : 
        risk_rate = int(pd.genomee.data["riskRate2"])
        simulateRate = int(pd.genomee.data["riskSimulate2"])
    Q = [[]]
    for hr in HR0:
        Q[0].append((0, -1, hr[1], hr[0]))
    for i in range(depth): Q.append([])

    current_depth = 0
    while current_depth < depth:
        qp = []
        for idx in range(len(Q[current_depth])):
            q = Q[current_depth][idx]
            hr : HuristicFunction = q[3]

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

                    if st[min(risk_rate , simulateRate)][1] > 0:
                        continue

                    movement = Movement(MoveKind.Attack, [v, u])

                    hist_v = (hr.proxyMap.verts[v].numNorm, hr.proxyMap.verts[v].numDef)
                    hist_u = (hr.proxyMap.verts[u].numNorm, hr.proxyMap.verts[u].numDef)
                    hist_id_u = hr.proxyMap.verts[u].team

                    if(st[simulateRate][0] - 1 == 0) :
                        print("RIDIDDDIDDI")
                    hr.updateVertex(v, ProxyMap.Vert(playerId, 1, hr.proxyMap.verts[v].numDef))
                    hr.updateVertex(u, ProxyMap.Vert(playerId, st[simulateRate][0] - 1, 0))
                    if current_depth == 0:
                        hr.player.hadSuccessInAttack = True

                    qp.append((hr.calculateValue(), movement, idx))

                    if current_depth == 0:
                        hr.player.hadSuccessInAttack = False
                    hr.updateVertex(v, ProxyMap.Vert(playerId, hist_v[0], hist_v[1]))
                    hr.updateVertex(u, ProxyMap.Vert(hist_id_u, hist_u[0], hist_u[1]))
        qp.sort(key=lambda x: x[0], reverse=True)
        L = []
        L.append(qp[0])
        for i in range(1, len(qp)):
            if abs(qp[i - 1][0] - qp[i][0]) > 0.000001:
                L.append(qp[i])
        qp = L
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

            hr = HuristicFunction.makeCopy(hr)
            hr.player.hadSuccessInAttack = True
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
    attackBeamSearchTime += time.time()
    return res


dropSoldierTime = 0


def dropSoldier(HR: [(HuristicFunction , [Movement])], beta: int, depth: int, playerId: int, turn: int , fraction : float):
    global dropSoldierTime
    dropSoldierTime -= time.time()
    qp = []
    for mp in HR:
        hr = mp[0]
        cnt = int(hr.player.nonDropSoldier * fraction)
        # if(turn == 1) :
        #     print("---nonDrop---" , hr.player.nonDropSoldier)
        #     print("---fraction--" , fraction)
        #     print("-----cnt-----" , cnt)
        qp.append((hr, mp[1] + [Movement(MoveKind.Nothing , [])]))
        if cnt == 0 : continue
        # hr.updatePlayer(ProxyMap.Player(nonDropSoldier=0, doneFort=hr.player.doneFort))
        hr.player.nonDropSoldier -= cnt
        lst = []
        for v in range(pd.mapp.n) :
            if(hr.proxyMap.verts[v].team == playerId or hr.proxyMap.verts[v].team == -1) :
                lst.append(v)
        lst = set(lst)
        for v in lst:
            hst = (hr.proxyMap.verts[v].team, hr.proxyMap.verts[v].numNorm, hr.proxyMap.verts[v].numDef)
            hr.updateVertex(v, ProxyMap.Vert(playerId, hr.proxyMap.verts[v].numNorm + cnt, hr.proxyMap.verts[v].numDef))
            qp.append((hr, mp[1] + [Movement(MoveKind.DropSoldier, [v, cnt])]))
            hr.updateVertex(v, ProxyMap.Vert(hst[0], hst[1], hst[2]))
        # hr.updatePlayer(ProxyMap.Player(nonDropSoldier=cnt, doneFort=hr.player.doneFort))
        hr.player.nonDropSoldier += cnt
    qp.sort(key=lambda x: x[0].calculateValue(), reverse=True)
    Q = []
    for i in range(min(beta, len(qp))):
        move = qp[i][1][len(qp[i][1])-1]
        hr = qp[i][0]
        nhr = HuristicFunction.makeCopy(hr)
        if (move.kind == MoveKind.Nothing) : 
            Q.append([nhr , qp[i][1]])
            continue
        v = move.move[0]
        cnt = move.move[1]
        # nhr.updatePlayer(ProxyMap.Player(doneFort=hr.player.doneFort))
        nhr.player.nonDropSoldier -= cnt
        nhr.updateVertex(v, ProxyMap.Vert(playerId, hr.proxyMap.verts[v].numNorm + cnt, hr.proxyMap.verts[v].numDef))
        Q.append([nhr, qp[i][1]])
    dropSoldierTime += time.time()
    return Q


moveSoldierTime = 0


def moveSoldierSearch(HR: list[HuristicFunction], beta: int, playerId: int):
    global moveSoldierTime
    moveSoldierTime -= time.time()
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
            if cnt < 2: continue
            for u in lst:
                if (u == v or hr.proxyMap.verts[u].numNorm < 2 or hr.parDsu(v) != hr.parDsu(u)):
                    continue
                uNorm = hr.proxyMap.verts[u].numNorm
                uDef = hr.proxyMap.verts[u].numDef
                hr.updateVertex(v, ProxyMap.Vert(playerId, vNorm - cnt, vDef))
                hr.updateVertex(u, ProxyMap.Vert(playerId, uNorm + cnt, uDef))
                qp.append((hr.calculateValue(), Movement(MoveKind.Move, [v, u, cnt]), id))
                hr.updateVertex(v, ProxyMap.Vert(playerId, vNorm, vDef))
                hr.updateVertex(u, ProxyMap.Vert(playerId, uNorm, uDef))
        qp.append((hr.calculateValue() , Movement(MoveKind.Nothing , []) , id))
        id += 1
    qp.sort(key=lambda x: x[0], reverse=True)
    Q = []
    for i in range(min(beta, len(qp))):
        move = qp[i][1]
        nhr = HuristicFunction.makeCopy(HR[qp[i][2]])
        if move.kind==MoveKind.Nothing  :
            Q.append([nhr , move , qp[i][2]])
            continue
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
    moveSoldierTime += time.time()
    return Q


beamSearchTime = 0  # optimize here


def beamSearch(HR: list[HuristicFunction], beta: int, playerId: int, turn: int, attackOrMove: int):
    global beamSearchTime
    beamSearchTime -= time.time()
    Q = []
    if turn > 1 or attackOrMove:
        dropSoldierList = dropSoldier([(hr , []) for hr in HR], playerId=playerId, beta=max(5 , beta), turn=turn, depth=5 , fraction=0.34)
        #print(dropSoldierList)
        dropSoldierList = dropSoldier([(hr[0] , hr[1]) for hr in dropSoldierList], playerId=playerId, beta=max(5 , beta), turn=turn, depth=5 , fraction=0.5)
        #print(dropSoldierList)
        dropSoldierList = dropSoldier([(hr[0] , hr[1]) for hr in dropSoldierList], playerId=playerId, beta=max(5 , beta), turn=turn, depth=5 , fraction=1)
        #print(dropSoldierList)
        for mp in dropSoldierList:
            Q.append((mp[0], mp[1]))
        attackList = attackBeamSearch(Q, max(beta*2 , 5), 7, playerId, turn)
        Q.clear()
        L = []
        for mp in attackList:
            L.append(mp[0])
        moveList = moveSoldierSearch(L, beta, playerId)

        for mp in moveList:
            Q.append((mp[0], attackList[mp[2]][1]))
        beamSearchTime += time.time()
        return Q
    else:
        moveList = moveSoldierSearch(HR, max(5 , beta), playerId)
        for mp in moveList:
            Q.append((mp[0], [mp[1]]))

    beamSearchTime += time.time()
    return Q


calcStateTime = 0


def calcStateValue(HR: HuristicFunction, playerId):
    global calcStateTime
    calcStateTime -= time.time()
    hValues = [0, 0, 0]
    hValues[playerId] = HR.calculateValue()
    hValues[(playerId + 1) % 3] = HuristicFunction.makeNew(ProxyMap.makeCopy(HR.proxyMap), (playerId + 1) % 3).calculateValue()
    hValues[(playerId + 2) % 3] = HuristicFunction.makeNew(ProxyMap.makeCopy(HR.proxyMap), (playerId + 2) % 3).calculateValue()
    total = 0
    for i in hValues:
        total += i * i
    for i in range(3):
        hValues[i] = hValues[i] * hValues[i] / total
    calcStateTime += time.time()
    return hValues


mnmxCNT = 0
miniMaxTime = 0

def miniMax(HR: HuristicFunction, beta: int, playerId: int, alpha: [], attackOrMove: int, turn: int, mxDepth: int) :
    global mnmxCNT
    global miniMaxTime
    miniMaxTime -= time.time()
    mnmxCNT += 1
    global safetyTimer
    if turn == 1 :
        safetyTimer = time.time()
    
    if turn > mxDepth:
        miniMaxTime += time.time()
        return calcStateValue(HR, playerId)
    #if turn > 1 -> update nonDrop Soldier
    # if turn > 1 : 
    #     HR.player.nonDropSoldier += HR.player.hadSuccessInAttack * 3 + HR.nextTurnSoldier
    bestVal = [0, 0, 0]
    Q = beamSearch([HR], beta, playerId, turn, attackOrMove)
    bestMove = 0
    ind = 0
    for nd in Q:
        value = miniMax(HuristicFunction.makeNew(ProxyMap.makeCopy(nd[0].proxyMap), (playerId + 1) % 3), max(beta - 1 , 3) ,
                        (playerId + 1) % 3, alpha[:], 1, turn + 1, mxDepth)
        if bestVal[playerId] < value[playerId]:
            bestVal = value
            bestMove = ind
        alpha[playerId] = max(alpha[playerId], value[playerId])
        if sum(alpha) > 1 + 0.001 :
            break
        ind += 1
    if turn == 1:
        miniMaxTime += time.time()
        return Q[bestMove]
    miniMaxTime += time.time()
    return bestVal


def miniMaxPhase1(HR: HuristicFunction, beta: int, playerId: int, alpha: [], turn: int, mxDepth: int):
    if turn > mxDepth:
        return calcStateValue(HR, playerId)

   
    qp = []
    lst = set()
    # for v in pd.mapp.strategicVerts:
    #     histv = [HR.proxyMap.verts[v].team, HR.proxyMap.verts[v].numNorm]
    #     if histv[0] != -1 and histv[0] != playerId:
    #         continue
    #     lst.add(v)


    # for v in HR.vertices:
    #     if HR.cntMarzi[v] == 0:
    #         continue
    #     lst.add(v)
    #     for u in pd.mapp.adj[v] :
    #         if HR.proxyMap.verts[u].team==-1 :
    #             lst.add(u)
    for v in range(pd.mapp.n) : 
        histv = [HR.proxyMap.verts[v].team, HR.proxyMap.verts[v].numNorm]
        if histv[0] != -1 and histv[0] != playerId:
            continue
        lst.add(v)
        # lst.append(v)

    for v in lst :
        histv = [HR.proxyMap.verts[v].team, HR.proxyMap.verts[v].numNorm]
        HR.updateVertex(v, ProxyMap.Vert(playerId, histv[1] + 1, 0))
        qp.append([HR.calculateValue(), v])
        HR.updateVertex(v, ProxyMap.Vert(histv[0], histv[1], 0))

    qp.sort(key=lambda x: x[0], reverse=True)
    bestVal = [0 , 0 , 0]
    bestMove = 0
    for i in range(min(len(qp) , beta)) :
        nd = qp[i]
        v = nd[1]
        histv = [HR.proxyMap.verts[v].team, HR.proxyMap.verts[v].numNorm]
        HR.updateVertex(v, ProxyMap.Vert(playerId, histv[1] + 1, 0))

        value = miniMaxPhase1(HuristicFunction.makeNew(ProxyMap.makeCopy(HR.proxyMap) , (playerId+1)%3) , max(beta - 1 , 3) , (playerId+1)%3 , alpha[:] , turn+1 , mxDepth)
        if bestVal[playerId] < value[playerId]:
            bestVal = value
            bestMove = v
        alpha[playerId] = max(alpha[playerId], value[playerId])
        HR.updateVertex(v, ProxyMap.Vert(histv[0], histv[1], 0))
        if sum(alpha) > 1 + 0.001 :
            break

    if turn==1 :
        return bestMove
    return bestVal