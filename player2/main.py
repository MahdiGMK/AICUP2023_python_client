import random , time
from player2.data import Map , ProxyMap , Genome , HuristicFunction
from player2.transition import MoveKind , Movement
import player2.transition as ts , player2.data as pd
from src.components.client_game import ClientGame

initialized = False
turn_number = 0

def initializer(game: ClientGame):
    timer = time.time()
    global initialized , turn_number , playerId
    turn_number+=1
    playerId = game.get_player_id()['player_id']
    
    if not initialized :
        print(f'player {playerId} initializing')
        turn_number = 0
        initialized = True
        adj = game.get_adj()
        n = len(adj)
        pd.mapp = Map(n)
        for v in adj :
            pd.mapp.setAdj(int(v) , adj[v])
        strat = game.get_strategic_nodes()
        stratNodes = strat['strategic_nodes']
        stratScores = strat['score']
        for i in range(len(stratNodes)) :
            v = stratNodes[i]
            s = stratScores[i]
            pd.mapp.setStrategic(v , s)
        
        pd.genomee = Genome(pd.genomee)
        # pd.genomee = Genome("player0/genome.json")
    # print('gooooodd' , playerId)
    
    numNorms = game.get_number_of_troops()
    numDefs = game.get_number_of_fort_troops()
    teams = game.get_owners()
    
    prx = ProxyMap.makeNew(pd.mapp , 3 , [])
    prx.players[playerId].nonDropSoldier = 1
    for i in range(pd.mapp.n) :
        prx.verts[i].team = teams[str(i)]
        prx.verts[i].numNorm = numNorms[str(i)]
        prx.verts[i].numDef = numDefs[str(i)]
        # print(prx.verts[i].team , prx.verts[i].numNorm , prx.verts[i].numDef)
    
    hr = HuristicFunction.makeNew(prx , playerId)
    print(hr.calculateValue() , hr.viewDataForDbug())
    if (turn_number > 15) : 
        res = ts.miniMax(hr , 5 , playerId , [0,0,0] , 1 , 1 , 1) # 4,3
        for mv in res[1] : 
            if mv.kind==MoveKind.DropSoldier: 
                print(game.put_one_troop(mv.move[0]) , "-- putting one troop on", mv.move[0])
                break
        
    else : 
        res = ts.miniMaxPhase1(hr , 5 , playerId , [0 , 0 , 0] , 1 , 3) # 5,5
        print(game.put_one_troop(res), "-- putting one troop on", res)

    print()
    print('timer : ' , time.time() - timer)
    print()
    # print(game.get_player_id())
    # strategic_nodes = game.get_strategic_nodes()['strategic_nodes']
    # score = game.get_strategic_nodes()['score']
    # strategic_nodes = list(zip(strategic_nodes, score))
    # strategic_nodes.sort(key=lambda x: x[1], reverse=True)
    # strategic_nodes, score = list(zip(*strategic_nodes))
    # print(game.get_turn_number())

    # owner = game.get_owners()
    # for i in strategic_nodes:
    #     if owner[str(i)] == -1:
    #         print(game.put_one_troop(i), "-- putting one troop on", i)
    #         return
    # adj = game.get_adj()
    # for i in strategic_nodes:
    #     for j in adj[str(i)]:
    #         if owner[str(j)] == -1:
    #             print(game.put_one_troop(j), "-- putting one troop on neighbor of strategic node", j)
    #             return
    # my_id = game.get_player_id()['player_id']
    # nodes = []
    # nodes.extend([i for i in strategic_nodes if owner[str(i)] == my_id])
    # for i in strategic_nodes:
    #     for j in adj[str(i)]:
    #         if owner[str(j)] == my_id:
    #             nodes.append(j)
    # nodes = list(set(nodes))
    # node = random.choice(nodes)
    # game.put_one_troop(node)
    # print("3-  putting one troop on", node)
    


def turn(game: ClientGame):
    timer = time.time()
    global turn_number
    turn_number+=1
    teams = game.get_owners()
    numNorms = game.get_number_of_troops()
    numDefs = game.get_number_of_fort_troops()
    
    prx = ProxyMap.makeNew(pd.mapp , 3 , [])
    prx.players[playerId].nonDropSoldier = game.get_number_of_troops_to_put()['number_of_troops']
    print("troops" , prx.players[playerId].nonDropSoldier)
    for i in range(pd.mapp.n) :
        prx.verts[i].team = teams[str(i)]
        prx.verts[i].numNorm = numNorms[str(i)]
        prx.verts[i].numDef = numDefs[str(i)]
        # print(prx.verts[i].team , prx.verts[i].numNorm , prx.verts[i].numDef)
    hr = HuristicFunction.makeNew(ProxyMap.makeCopy(prx) , playerId)
    print(hr.calculateValue() , hr.viewDataForDbug())
    res = ts.miniMax(hr , 5 , playerId , [0 , 0 , 0] , 1 , 1 , 1) # optimize needed ...defualt 5 4 
    print(res[1])
    
    # drop
    for mv in res[1] :
        if mv.kind == MoveKind.DropSoldier :
            mv : Movement
            v = mv.move[0]
            cnt = mv.move[1]
            if cnt > 0 :
                print("dropped " , cnt)
                game.put_troop(v , cnt)
                prx.verts[v].numNorm += cnt

            
    game.next_state()
    # attack
    for mv in res[1] :
        if mv.kind == MoveKind.Attack :
            mv : Movement
            v = mv.move[0]
            u = mv.move[1]
            if (prx.verts[v].team!=playerId) : 
                continue
            numV = prx.verts[v].numNorm
            numU = prx.verts[u].numNorm + prx.verts[u].numDef
            state = pd.staticData.getState(numV , numU)
            if state[3][1] == 0 :
                game.attack(v , u , pd.genomee.data['riskyFraction'] , 0.999)
                teams = game.get_owners()
                numNorms = game.get_number_of_troops()
                numDefs = game.get_number_of_fort_troops()
                for i in range(pd.mapp.n) :
                    prx.verts[i].team = teams[str(i)]
                    prx.verts[i].numNorm = numNorms[str(i)]
                    prx.verts[i].numDef = numDefs[str(i)]
    game.next_state()
    # move
    hr = HuristicFunction.makeNew(ProxyMap.makeCopy(prx) , playerId)
    res = ts.miniMax(hr , 5 , playerId , [0 , 0 , 0] , 0 , 1 , 1) # 4 2 
    for mv in res[1] :
        if mv.kind == MoveKind.Move :
            mv : Movement
            v = mv.move[0]
            u = mv.move[1]
            cnt = mv.move[2]
            game.move_troop(v , u , cnt)
            prx.verts[v].numNorm -= cnt
            prx.verts[u].numNorm += cnt
            break
    game.next_state()
    # fort  TODO
    
    print()
    print('timer : ' , time.time() - timer)
    print()
    # for mv in res[1] :
    #     if mv.kind == MoveKind.Fort :
    #         mv : Movement
    
    # done
    
    
    # global flag
    # print(game.get_number_of_troops_to_put())
    # owner = game.get_owners()
    # for i in owner.keys():
    #     if owner[str(i)] == -1 and game.get_number_of_troops_to_put()['number_of_troops'] > 1:
    #         print(game.put_troop(int(i), 1))

    # list_of_my_nodes = []
    # for i in owner.keys():
    #     if owner[str(i)] == game.get_player_id()['player_id']:
    #         list_of_my_nodes.append(i)

    # print(game.put_troop(random.choice(list_of_my_nodes), game.get_number_of_troops_to_put()['number_of_troops']))
    # print(game.get_number_of_troops_to_put())

    # print(game.next_state())

    # # find the node with the most troops that I own
    # max_troops = 0
    # max_node = -1
    # owner = game.get_owners()
    # for i in owner.keys():
    #     if owner[str(i)] == game.get_player_id()['player_id']:
    #         if game.get_number_of_troops()[i] > max_troops:
    #             max_troops = game.get_number_of_troops()[i]
    #             max_node = i
    # # find a neighbor of that node that I don't own
    # adj = game.get_adj()
    # for i in adj[max_node]:
    #     if owner[str(i)] != game.get_player_id()['player_id'] and owner[str(i)] != -1:
    #         print(game.attack(int(max_node), int(i), 1, 0.5))
    #         break
    
    # print(game.next_state())
    # print(game.get_state())
    # # get the node with the most troops that I own
    # max_troops = 0
    # max_node = -1
    # owner = game.get_owners()
    # for i in owner.keys():
    #     if owner[str(i)] == game.get_player_id()['player_id']:
    #         if game.get_number_of_troops()[i] > max_troops:
    #             max_troops = game.get_number_of_troops()[i]
    #             max_node = i
    # print(game.get_reachable(int(max_node)))
    # x = game.get_reachable(int(max_node))['reachable']
    # x.remove(int(max_node))
    # if len(x) > 0:
    #     destination = random.choice(x)
    #     print(game.move_troop(int(max_node), int(destination), 1))
    
    # print(game.next_state())

    # if flag == False:
    #     max_troops = 0
    #     max_node = -1
    #     owner = game.get_owners()
    #     for i in owner.keys():
    #         if owner[str(i)] == game.get_player_id()['player_id']:
    #             if game.get_number_of_troops()[i] > max_troops:
    #                 max_troops = game.get_number_of_troops()[i]
    #                 max_node = i

    #     print(game.get_number_of_troops()[max_node])
    #     print(game.fort(int(max_node), 3))
    #     print(game.get_number_of_fort_troops())
    #     flag = True
    
