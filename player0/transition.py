import copy

import data


class Movement:
    def __init__(self, kind: str, move: []):
        self.kind = kind
        self.move = move


def attack_beam_search(HR0: data.HuristicFunction, beta: int, depth: int, id: int, turn: int):
    risk_rate = 3
    Q = [[0, [], HR0]]
    HR0.buildDsu()
    current_depth = 0
    while current_depth < depth:
        qp = []
        for i in range(len(Q)):
            if Q[i][0] < current_depth:
                qp.append([Q[i][2].calculateValue(), Movement("nothing", []), i])
                continue
            hr = Q[i][2]

            qp.append([hr.calculateValue(), Movement("nothing", []), i])
            for v in hr.vertices:
                n = hr.proxyMap.verts[v].numNorm
                if n <= 1:
                    continue
                if hr.cntMarzi[v] > 0:
                    for u in hr.map.adj[v]:
                        if hr.proxyMap.verts[u].team == id or hr.proxyMap.verts[u].team == -1:
                            continue

                        m = hr.proxyMap.verts[u].numNorm + hr.proxyMap.verts[u].numDef
                        st = data.staticData.getState(n, m)

                        if st[risk_rate][1] > 0:
                            continue

                        movement = Movement("attack", [v, u])

                        hist_v = [hr.proxyMap.verts[v].numNorm, hr.proxyMap.verts[v].numDef]
                        hist_u = [hr.proxyMap.verts[u].numNorm, hr.proxyMap.verts[u].numDef]
                        hist_id_u = hr.proxyMap.verts[u].team

                        hr.updateVertex(v, data.ProxyMap.Vert(id, 1, hr.proxyMap.verts[v].numDef))
                        hr.updateVertex(u, data.ProxyMap.Vert(id, st[risk_rate][0] - 1, 0))

                        qp.append([hr.calculateValue(), movement, i])

                        hr.updateVertex(v, data.ProxyMap.Vert(id, hist_v[0], hist_v[1]))
                        hr.updateVertex(u, data.ProxyMap.Vert(hist_id_u, hist_u[0], hist_u[1]))
        qp.sort(key=lambda x: x[0], reverse=True)
        new_q = []
        for i in range(min(beta, len(qp))):
            movement = qp[i][1]
            ind = qp[i][2]
            hr = Q[ind][2]
            if movement.kind == "nothing":
                new_opt = [Q[ind][0], copy.deepcopy(Q[ind][1]), copy.deepcopy(hr)]
                new_q.append(new_opt)
                continue
            v = movement.move[0]
            u = movement.move[1]

            n = hr.proxyMap.verts[v].numNorm
            m = hr.proxyMap.verts[u].numNorm + hr.proxyMap.verts[u].numDef
            st = data.staticData.getState(n, m)

            hist_v = [hr.proxyMap.verts[v].numNorm, hr.proxyMap.verts[v].numDef]
            hist_u = [hr.proxyMap.verts[u].numNorm, hr.proxyMap.verts[u].numDef]
            hist_id_u = hr.proxyMap.verts[u].team

            hr.updateVertex(v, data.ProxyMap.Vert(id, 1, hr.proxyMap.verts[v].numDef))
            hr.updateVertex(u, data.ProxyMap.Vert(id, st[risk_rate][0] - 1, 0))

            new_opt = [Q[ind][0] + 1, Q[ind][1] + [movement], copy.deepcopy(hr)]

            new_q.append(new_opt)
            hr.updateVertex(v, data.ProxyMap.Vert(id, hist_v[0], hist_v[1]))
            hr.updateVertex(u, data.ProxyMap.Vert(hist_id_u, hist_u[0], hist_u[1]))
        Q = new_q
        current_depth += 1

    return Q
