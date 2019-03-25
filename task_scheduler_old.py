import numpy as np
from geneticdrift import create_offspring,create_initial_population
from selection import tournament




class ARMv8():
    def __init__(self,V):
        cycles_per_task_s1 = [192450,276390,477300,0,1125420,950540,692800,782590,442410,305310,60300]
        cycles_per_task_s2 = [192450,272500,561600,970500,911500,950540,511540,660810,391580,306990,60300]
        k_f = 192450/(295*10**-9)/(2/3)
        self.time_per_task_s1 = np.array(cycles_per_task_s1)/(k_f * V)
        self.time_per_task_s2 = np.array(cycles_per_task_s2)/(k_f * V)

class Adreno():
    def __init__(self,V):
        cycles_per_task_s1 = [113060 ,165660 ,284000 ,0,685320 ,656110 ,398220 ,472050 ,274370 ,203750,39050]
        cycles_per_task_s2 = [113060 ,160630 ,329560 ,593120 ,542880 ,553000 ,300600 ,450600 ,237750 ,209750 ,39050 ]
        k_f = 165660/(301*10**-9)
        self.time_per_task_s1 = np.array(cycles_per_task_s1)/(k_f * V)
        self.time_per_task_s2 = np.array(cycles_per_task_s2)/(k_f * V)

class MIPS():
    def __init__(self,V):
        cycles_per_task_s1 = [98540  ,124380  ,217450  ,0,545310  ,456790  ,325670  ,369120  ,208450  ,136170 ,28640 ]
        cycles_per_task_s2 = [98540  ,117900  ,267450  ,482050  ,434320  ,423400  ,236540  ,302370  ,195780  ,138320  ,28640]
        k_f = 208450/(349*10**-9)
        self.time_per_task_s1 = np.array(cycles_per_task_s1)/(k_f * V)
        self.time_per_task_s2 = np.array(cycles_per_task_s2)/(k_f * V)


def combine_tasks(combi_task,nodes_time_per_task):
    low = combi_task[0]
    high = combi_task[1]
    # high gets removed

    nodes_time_per_task_combined = []
    for i,time_per_task in enumerate(nodes_time_per_task):
        c1 = time_per_task[low]
        c2 = time_per_task[high]
        low_c = min([c1,c2])
        high_c = max([c1,c2])
        c_combi = low_c*.4 +high_c
        time_per_task[low] = c_combi
        nodes_time_per_task_combined.append(np.concatenate((time_per_task[:high],time_per_task[high+1:])))
    return nodes_time_per_task_combined

def get_possible_task_combinations():
    combi_tasks = []
    for low in range(1,4): # task 2 till 5
        for high in range(low,4):
            combi_tasks.append((low,high))

    for low in range(4,8):
        for high in range(low,8):
            combi_tasks.append((low,high))
    return combi_tasks



def calculate_schedule_time(genes,nodes):
    schedule = genes[:11]
    combi_task = genes[11]
    node_occupation_t1 = np.zeros(6)
    node_occupation_t2 = np.zeros(6)

    tasks_dependencies = [[],[0], [0], [0],  [1],  [1],  [2], [2 , 3 ],[4,5,6],[6,7],[8,9]]
                #      F1  F2    F3   F4   F5     F6     F7  F8 F9 F10 F11   F12 F13 F14 F15
    com_times= [[],[205],[205],[0],[205],[103],[205],   [103,0],[205,205,820],[103,103],[409,205]]
    com_times2 = [[],[205],[205],[409],[205],[103],[205],[205,409],[205,205,820],[103,103],[409,205]]

    com_times = [[t*10**-9 for t in times] for times in com_times]
    com_times2 = [[t*10**-9 for t in times] for times in com_times2]



    node_times_s1 = [node.time_per_task_s1 for node in nodes]
    node_times_s2 = [node.time_per_task_s2 for node in nodes]
   

    
    if not combi_task[0] == combi_task[1]:

        schedule = np.delete(schedule,combi_task[1])
        
        node_times_s1 = combine_tasks(combi_task,node_times_s1)
        node_times_s2 = combine_tasks(combi_task,node_times_s2)

    # Add dependencies of higher combined task to the lower combined task.
        tasks_dependencies[combi_task[0]].extend(tasks_dependencies.pop(combi_task[1]))
        com_times[combi_task[0]].extend(com_times.pop(combi_task[1]))
        com_times2[combi_task[0]].extend(com_times2.pop(combi_task[1]))

        # Switch all higher dependencies on the higher task to the lower task.
        for task_dependencies in tasks_dependencies:
            for i_dep,dependency in enumerate(task_dependencies):
                if dependency == combi_task[1]:
                    task_dependencies[i_dep] = combi_task[0]

    for i_task, node_assigned in enumerate(schedule):
        task_dependencies = tasks_dependencies[i_task]
        
        com_times_t1 = com_times[i_task]
        com_times_t2 = com_times2[i_task]

        time_task_available_t1 = node_occupation_t1[node_assigned]
        time_task_available_t2 = node_occupation_t2[node_assigned]
        #time_task_available_t2 = max(t_completions_t2[i_task],time_task_available_t2)

        
        for i_dep,dependency in enumerate(task_dependencies):
            if not schedule[dependency] == node_assigned: # Has the dependency not been executed by me
                time_task_available_t1 = max(node_occupation_t1[schedule[dependency]] + com_times_t1[i_dep],time_task_available_t1)
                time_task_available_t2 = max(node_occupation_t2[schedule[dependency]] + com_times_t2[i_dep],time_task_available_t2)
        
        completion_time_t1 = time_task_available_t1 + nodes[node_assigned].time_per_task_s1[i_task]
        completion_time_t2 = time_task_available_t2 + nodes[node_assigned].time_per_task_s2[i_task]

        node_occupation_t1[node_assigned] = completion_time_t1
        node_occupation_t2[node_assigned] = completion_time_t2
    return (max(node_occupation_t1) + max(node_occupation_t2))/2
import time

pop_size = 80
no_gen = 70
mutation_chance = 0.15


def schedule_tasks(nodes_cmd,voltages_cmd):
    nodes = []

    possible_task_combinations = get_possible_task_combinations()
    gene_pool = [list(range(6)) for _ in range(11)] + [possible_task_combinations]
    for i,node in enumerate(nodes_cmd):
        v = float(voltages_cmd[i])
        
        if node == '"ARMv8"':
            nodes+= [ARMv8(v)]
        if node ==  '"Adreno"':
            nodes+= [Adreno(v)]
        if node == '"MIPS"':
            nodes+= [MIPS(v)]
    # Load some node array
    schedule_cmds = []
    combi_cmds = []
    for nodepref in [6]:
        population,known_dna = create_initial_population(gene_pool,pop_size)
        #population = np.array(population)
        best_times = []
        avg_times = []
        for gen in range(no_gen):
            start = time.time()
            avg_duration = [calculate_schedule_time(genes,nodes) for genes in population]
         
            for i,genes in enumerate(population):
                if len(set(genes)) == nodepref+1:
                    avg_duration[i]-=1e-6
            parents_ids = tournament(avg_duration,pop_size,2)
            parents_ids = np.unique(parents_ids)
            parents =  [population[parents_id] for parents_id in parents_ids]
            

            offspring,known_dna,_ = create_offspring(parents,2,pop_size*2-len(parents),mutation_chance,gene_pool,known_dna)
            population = parents+offspring
            best_times += [min(avg_duration)]
            avg_times +=[np.mean(avg_duration)]

        avg_duration = [calculate_schedule_time(genes,nodes) for genes in population]
        for i,genes in enumerate(population):
            if len(set(genes)) == nodepref+1:
                avg_duration[i]-=1e-6
        sort_ids = np.argsort(avg_duration)
        population_sorted = [population[sort_id] for sort_id in sort_ids]
        population_sorted = population_sorted[:11]
        for genes in population_sorted:
            schedule_cmd = []
            for node_asigened in genes[:-1]:
                schedule_cmd += ['"Node' + str(node_asigened+1) + '"']
            combi_cmds+= [genes[-1]]
            schedule_cmds += [(schedule_cmd)]
    return schedule_cmds,combi_cmds




# nodes_cmd = ['"ARMv8"','"Adreno"','"Adreno"','"MIPS"','"ARMv8"','"MIPS"']
# voltages_cmd = [str(2/3),str(1.0),str(1.0),str(1.0),str(2/3),str(1.0)]



schedule_cmds = schedule_tasks(nodes_cmd,voltages_cmd)
# # 
print(schedule_cmds)





