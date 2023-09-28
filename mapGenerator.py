import networkx as nt
import random
import json


comp = 0


def dfs(v, adj, mark):
    mark[v] = 1
    for u in adj[v]:
        if mark[u]:
            continue
        dfs(u, adj, mark)
    return


cnt = 31
while cnt < 35 :
    n = random.randint(35,70)
    L = [0 for i in range(n)]
    for i in range(n):
        x = random.randint(1, 100)
        if x <= 40:
            L[i] = random.randint(1, 3)
        elif (x <= 60):
            L[i] = random.randint(4, 10)
        elif (x <= 100):
            L[i] = random.randint(11, 15)
    try:
        g = nt.random_degree_sequence_graph(L)
    except:
        continue
    print("yo")
    ADJ = [[] for i in range(n)]
    mark = [0 for i in range(n)]
    for ad in g.adj:
        for u in g.adj[ad]:
            ADJ[ad].append(u)
    comp = 0
    for i in range(n):
        if mark[i] == 0:
            comp += 1
            dfs(i, ADJ, mark)
    if comp > 1:
        continue
    print("yohooo", cnt)
    edges = []
    for ad in g.adj:
        for u in g.adj[ad]:
            if [u, ad] in edges:
                continue
            edges.append([ad, u])
    dict = {}
    dict["number_of_nodes"] = n
    dict["number_of_edges"] = len(edges)
    dict["list_of_edges"] = edges
    dict["strategic_nodes"] = [0, 1, 2, 3, 4, 5]
    dict["scores_of_strategic_nodes"] = [random.randint(3, 8) for i in range(6)]

    with open("maps/map" + str(cnt) + ".json", 'w') as f:
        json.dump(dict, f)
    cnt += 1

# {
#     "number_of_nodes": 42,
#     "number_of_edges": 82,
#     "list_of_edges": [[0, 1], [0, 2], [1, 2], [1, 3], [2, 3], [3, 4], [4, 5], [4, 6], [5, 6], [5, 8], [5, 7], [5, 14], [5, 13], [6, 7], [6, 21], [7, 21], [7, 15], [7, 14], [8, 13], [8, 11], [8, 10], [9, 8], [9, 10], [10, 12], [10, 11], [10, 36], [11, 12], [11, 13], [12, 13], [13, 14], [14, 15], [15, 21], [15, 20], [15, 18], [15, 16], [16, 18], [16, 17], [16, 41], [17, 41], [17, 19], [17, 18], [18, 19], [18, 20], [19, 20], [19, 27], [20, 21], [20, 22], [21, 22], [21, 23], [22, 23], [22, 27], [23, 24], [23, 25], [23, 26], [23, 27], [24, 25], [25, 26], [26, 27], [27, 28], [28, 29], [28, 30], [28, 31], [29, 30], [30, 31], [31, 32], [32, 33], [32, 34], [33, 34], [33, 38], [33, 39], [34, 35], [34, 38], [35, 38], [35, 37], [35, 36], [36, 37], [37, 38], [37, 40], [38, 39], [38, 40], [39, 40], [40, 41]],
#     "strategic_nodes": [29, 3, 7, 4, 20, 40],
#     "scores_of_strategic_nodes" : [1, 2, 5, 1, 4, 3]
# }


