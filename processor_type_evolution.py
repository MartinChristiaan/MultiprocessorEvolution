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
no_parallel_simulations = 4


def get_all_distributions(max_size):
    distr = []
    for x in range(0,max_size+1):
        for y in range(0,max_size+1 - x):
            z = max_size - x- y
            distr.append((x,y,z))
    return distr

df = pd.DataFrame()
vsfs = [str(1.0)]*6
combi_task = (1,1)

for nodepref in [4,5,6]:
    Processor_type_distributions = get_all_distributions(nodepref)
    for ptd in Processor_type_distributions:
        data = [ptd,nodepref,combi_task] + [str(1.0)]*6 + ['"PB"']*6
        row_df = pd.DataFrame([data],columns = columns)
        df = df.append(row_df)

if __name__ == "__main__":
    for i in range(no_parallel_simulations):
        poosl_model_generator.setup_simulation(i)
    results = autosim_multiproc.autosim_multiproc(perform_simulation,df,no_parallel_simulations)
    results.to_csv("generations/ProcessorDistribution.csv",index=False)



