import numpy as np






class ARMv8():
    def __init__(self,V):
        cycles_per_task_s1 = [192450,276390,477300,0,1125420,950540,692800,782590,442410,305310,60300]
        cycles_per_task_s2 = [192450,272500,561600,970500,911500,950540,511540,660810,391580,306990,60300]
        k_f = 192450/(295*10**-9)
        self.time_per_task_s1 = np.array(cycles_per_task_s1)/(k_f * V)

class Adreno():
    def __init__(self,V):
        cycles_per_task_s1 = [113060 ,165660 ,284000 ,0,685320 ,656110 ,398220 ,472050 ,274370 ,203750,39050]
        cycles_per_task_s2 = [113060 ,160630 ,329560 ,593120 ,542880 ,553000 ,300600 ,450600 ,237750 ,209750 ,39050 ]
        k_f = 165660/(545*10**-9)
        self.time_per_task_s1 = np.array(cycles_per_task_s1)/(k_f * V)

class MIPS():
    def __init__(self,V):
        cycles_per_task_s1 = [98540  ,124380  ,217450  ,0,545310  ,456790  ,325670  ,369120  ,208450  ,136170 ,28640 ]
        cycles_per_task_s2 = [98540  ,117900  ,267450  ,482050  ,434320  ,423400  ,236540  ,302370  ,195780  ,138320  ,28640]
        k_f = 165660/(545*10**-9)
        self.time_per_task_s1 = np.array(cycles_per_task_s1)/(k_f * V)



# Load some node array
nodes = [ARMv8(1),ARMv8(1),ARMv8(1),ARMv8(1),ARMv8(1),ARMv8(1)]


dependencies = [[],[0],[0],[0],[1],[1],[2],[2,3],[4,5,6],[6,7],[8,9]]

com_times = [[],[1],[1],[1]]

no_attempts = 100
# expand
divergence = 2 

def schedule_task(schedule,t_completions):
    task_id = len(schedule)
    task_dependencies = dependencies[task_id]
    comunication_times = com_times[task_id]
    potential_times = np.zeros(6) 
    for i_node,node in enumerate(nodes):
        time_task_available = 0
        for i_task,task in schedule:
            if task == i_node:
                time_task_available = t_completions[i_task]
        for i_dep,dependency in task_dependencies:
            if not schedule[dependency] == i_node: # Has the dependency not been executed by me
                time_task_available = max(t_completions[dependency] + comunication_times[i_dep],time_task_available)
        my_potential_completion_time = time_task_available + node.time_per_task_s1[task_id]
        potential_times[i_node] = my_potential_completion_time
        
    if task_id == len(dependencies)-1:
        best_node = potential_times.argmin()
        schedule.append(best_node)
        final_time = max(t_completions+potential_times[best_node])
        return schedule,final_time
    else:
        nodes_sorted = np.argsort(potential_times)
        potential_schedules = np.zeros(divergence)
        final_times = np.zeros(divergence)
        for i in range(divergence):
            task_completion_time = potential_times[nodes_sorted][i]
            new_t_completions = t_completions + task_completion_time
            new_schedule = schedule + nodes_sorted[i]
            potential_schedules[i],final_times[i] = (schedule_task(new_schedule,t_completions))
        best_time_id = final_times.argmin()
        return potential_schedules[best_time_id],final_times[best_time_id]








cur_task = 0
task_times = [p.time_per_task_s1[cur_task] for p in nodes]

#select



    






# 




