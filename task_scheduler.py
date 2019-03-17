import numpy as np



class ARMv8():
    def __init__(self,V):
        cycles_per_task_s1 = [192450,276390,477300,0,1125420,950540,692800,782590,442410,305310,60300]
        cycles_per_task_s2 = [192450,272500,561600,970500,911500,950540,511540,660810,391580,306990,60300]
        k_f = 192450/(295*10**-9)
        self.time_per_task_s1 = np.array(cycles_per_task_s1)/(k_f * V)
        self.time_per_task_s2 = np.array(cycles_per_task_s2)/(k_f * V)

class Adreno():
    def __init__(self,V):
        cycles_per_task_s1 = [113060 ,165660 ,284000 ,0,685320 ,656110 ,398220 ,472050 ,274370 ,203750,39050]
        cycles_per_task_s2 = [113060 ,160630 ,329560 ,593120 ,542880 ,553000 ,300600 ,450600 ,237750 ,209750 ,39050 ]
        k_f = 165660/(545*10**-9)
        self.time_per_task_s1 = np.array(cycles_per_task_s1)/(k_f * V)
        self.time_per_task_s2 = np.array(cycles_per_task_s2)/(k_f * V)

class MIPS():
    def __init__(self,V):
        cycles_per_task_s1 = [98540  ,124380  ,217450  ,0,545310  ,456790  ,325670  ,369120  ,208450  ,136170 ,28640 ]
        cycles_per_task_s2 = [98540  ,117900  ,267450  ,482050  ,434320  ,423400  ,236540  ,302370  ,195780  ,138320  ,28640]
        k_f = 208450/(349*10**-9)
        self.time_per_task_s1 = np.array(cycles_per_task_s1)/(k_f * V)
        self.time_per_task_s2 = np.array(cycles_per_task_s2)/(k_f * V)


# Load some node array
nodes = [ARMv8(1),ARMv8(1),ARMv8(1),ARMv8(1),ARMv8(1),ARMv8(1)]


dependencies = [[],[0], [0], [0],  [1],  [1],  [2], [2 , 3 ],[4,5,6],[6,7],[8,9]]
            #      F1  F2    F3   F4   F5     F6     F7  F8 F9 F10 F11   F12 F13 F14 F15
com_times = [[],[205],[205],[0],[205],[103],[205],   [103,0],[205,205,820],[103,103],[409,205]]
com_times2 = [[],[205],[205],[409],[205],[103],[205],[205,409],[205,205,820],[103,103],[409,205]]

# expand
divergence = 2 

def schedule_task(schedule,t_completions_t1,t_completions_t2):
    task_id = len(schedule)
    task_dependencies = dependencies[task_id]
    com_times_t1= com_times[task_id]
    com_times_t2 = com_times2[task_id]
    potential_times_t1 = np.zeros(6) 
    potential_times_t2 = np.zeros(6) 

    for i_node,node in enumerate(nodes):
        time_task_available_t1 = 0
        time_task_available_t2 = 0
        for i_task,node_assigned in enumerate(schedule):
            if node_assigned == i_node:
                time_task_available_t1 = t_completions_t1[i_task]
                time_task_available_t2 = t_completions_t2[i_task]

        for i_dep,dependency in enumerate(task_dependencies):
            if not schedule[dependency] == i_node: # Has the dependency not been executed by me
                time_task_available_t1 = max(t_completions_t1[dependency] + com_times_t1[i_dep],time_task_available_t1)
                time_task_available_t2 = max(t_completions_t2[dependency] + com_times_t2[i_dep],time_task_available_t2)

        my_potential_completion_time_t1 = time_task_available_t1 + node.time_per_task_s1[task_id]
        my_potential_completion_time_t2 = time_task_available_t2 + node.time_per_task_s2[task_id]
        potential_times_t1[i_node] = my_potential_completion_time_t1
        potential_times_t2[i_node] = my_potential_completion_time_t2
        
    if task_id == len(dependencies)-1:
        best_node = (potential_times_t1 + potential_times_t2).argmin()
        schedule.append(best_node)
        final_time = t_completions_t1+potential_times_t1[best_node] + potential_times_t2[best_node]
        return schedule,final_time
    else:
        nodes_sorted = np.argsort(potential_times_t1 + potential_times_t2)
        potential_schedules = []
        final_times = np.zeros(divergence)
        for i in range(divergence):

            task_completion_time_t1 = potential_times_t1[nodes_sorted][i]
            task_completion_time_t2 = potential_times_t2[nodes_sorted][i]

            new_t_completions_t1 = t_completions_t1 + [task_completion_time_t1]
            new_t_completions_t2 = t_completions_t2 + [task_completion_time_t2]

            new_schedule = schedule + [nodes_sorted[i]]
            print(new_schedule)

            potential_schedule,final_time = schedule_task(new_schedule,new_t_completions_t1,new_t_completions_t2)
            print(final_time)
            potential_schedules.append(potential_schedule)
            final_times[i] = final_time
        best_time_id = final_times.argmin()
        return potential_schedules[best_time_id],final_times[best_time_id]

schedule,time = schedule_task([],[],[])
print(schedule)
print(time)



#select



    






# 




