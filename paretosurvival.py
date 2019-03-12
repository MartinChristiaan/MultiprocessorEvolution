import numpy as np

def get_pareto_front(objectives):
    is_efficient = np.ones(objectives.shape[0], dtype = bool)
    for i, c in enumerate(objectives):
        if is_efficient[i]:
            is_efficient[is_efficient] = np.any(objectives[is_efficient]<c, axis=1)  # Keep any point with a lower cost
            is_efficient[i] = True  # And keep self
    
    return is_efficient

def pareto_rank(objectives):
    rank = 1
    pop_ids = np.arange(objectives.shape[0],dtype=int)
    ranks = np.zeros(objectives.shape[0],dtype=int)
    done = False
    fronts = []
    print()
    while not done:
        myids = np.argwhere(ranks == 0).T[0]
        if len(myids) > 0:
            isfront = get_pareto_front(objectives[myids,:])
            rank_ids = myids[isfront]
            fronts.append(objectives[rank_ids,:])
            ranks[rank_ids] = rank     
            rank+=1       
        else:
            done = True
    return fronts,ranks



def crowding_distance(fronts,ranks):
    distance = np.zeros(ranks.shape)
    for front_rank,front in enumerate(fronts):
        front_ids = np.argwhere(ranks == front_rank+1)
        per_objective_sorted_front = [front[np.argsort(front[:,obj_id]),obj_id] 
            for obj_id in range(front.shape[1])]

        distance[front_ids[0]] = np.inf
        distance[front_ids[-1]] = np.inf
        
        for obj_id in range(front.shape[1]):
            obj = front[:,obj_id]
            sort_ids = np.argsort(obj)
            sorted_front_ids = front_ids[sort_ids]
            obj_sort = obj[sort_ids]
            for k in range(1,len(front)-1):
                distance[sorted_front_ids[k]] += (obj_sort[k+1] - obj_sort[k-1])/(max(obj)-min(obj))
        
    return distance

def pareto_tournament(paretorank,no_matches,rounds,crowd_distance = []):
    n = len(paretorank)
    matingpool = []#np.zeros(no_matches,dtype = int)
    for i in range(no_matches):
        a = np.random.randint(n)
        for j in range(rounds):
            b = np.random.randint(n)
            if paretorank[b] < paretorank[a]:
                a = b
            elif paretorank[b] == paretorank[a] and len(crowd_distance) > 0:
                if crowd_distance[b] > crowd_distance[a]:
                    a = b

        matingpool.append(a)    
    return matingpool

def calculate_score_and_pareto_rank(population,objfuns):
    objective_scores = [[obj_fun(*tuple(creature)) for creature in population] for obj_fun in objfuns]
    objective_scores = np.array(objective_scores).T
    fronts,ranks = pareto_rank(objective_scores)
    return fronts,ranks,objective_scores




