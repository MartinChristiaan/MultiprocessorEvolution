import random
from selection import pareto_rank,tournament,crowding_distance
from geneticdrift import create_offspring,create_initial_population
from simulation import perform_simulation
from task_scheduler import schedule_tasks
import pandas as pd
import autosim_multiproc
import autosim
import poosl_model_generator
def quotate(mystr):
    return '"' + mystr + '"'
columns = ["NodeProcessorTypeDistribution","No_Proc_Preffered","Combi_Task","VSF1","VSF2","VSF3","VSF4","VSF5","VSF6","OSPolicy1","OSPolicy2","OSPolicy3","OSPolicy4","OSPolicy5","OSPolicy6"]

pop_size = 70
parents_per_child=2
mutation_chance = 0.15
no_parallel_simulations = 6

def get_possible_task_combinations():
    combi_tasks = []
    for low in range(1,4): # task 2 till 5
        for high in range(low,4):
            combi_tasks.append((low,high))

    for low in range(4,8):
        for high in range(low,8):
            combi_tasks.append((low,high))
    return combi_tasks



df_pdr = pd.read_csv('ProcessorDistribution_ranked.csv')
df_pdr = df_pdr[df_pdr['pareto rank'] < 3]
df = pd.DataFrame()
Processor_type_distributions = df_pdr['NodeProcessorTypeDistribution']
vsfs = [str(1.0)]*6
combi_tasks = get_possible_task_combinations()

for ptd in Processor_type_distributions:
    for combi_task in combi_tasks:
        nodepref  = int(ptd[1])+int(ptd[4])+int(ptd[7])
        data = [ptd,nodepref,combi_task] + [str(1.0)]*6 + ['"PB"']*6
        row_df = pd.DataFrame([data],columns = columns)
        df = df.append(row_df)

if __name__ == "__main__":
    for i in range(no_parallel_simulations):
        poosl_model_generator.setup_simulation(i)
    results = autosim_multiproc.autosim_multiproc(perform_simulation,df,no_parallel_simulations)
    results.to_csv("generations/ProcessorDistribution.csv",index=False)



