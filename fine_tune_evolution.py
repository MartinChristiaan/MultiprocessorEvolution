
import numpy as np
#import matplotlib.pyplot as plt
import random
from selection import pareto_rank,tournament,crowding_distance
from geneticdrift import create_offspring,create_initial_population
from simulation import perform_simulation_finetune
from task_scheduler import schedule_tasks
import pandas as pd
import autosim_multiproc
import autosim
import poosl_model_generator
def quotate(mystr):
    return '"' + mystr + '"'
columns = ["Config","VSF1","VSF2","VSF3","VSF4","VSF5","VSF6","OSPolicy1","OSPolicy2","OSPolicy3","OSPolicy4","OSPolicy5","OSPolicy6"]

pop_size = 80
parents_per_child=2
mutation_chance = 0.15
no_parallel_simulations = 2


def get_all_distributions(max_size):
    distr = []
    for x in range(0,max_size+1):
        for y in range(0,max_size+1 - x):
            z = max_size - x- y
            distr.append((x,y,z))
    return distr


Processor_type_distribution = get_all_distributions(6)

VSFs =  [str(1.0)] * 5+[str(2.0/3.0)]*2+[str(1.0/2.0)] + [str(1.0/4)]
OSPolicys = [quotate(s) for s in ["FCFS","PB"]]
gene_pool = [list(range(35))] + [VSFs]*6 + [OSPolicys]*6
tournament_rounds = 3
max_gen = 70
gen_no = 0



while True:
    try:
        generation_df = pd.read_csv('generations/generation' + str(gen_no) + '.csv')
        gen_no+=1    
    except:
        if gen_no ==0:
             generation_df = pd.DataFrame()
        break
known_dna = set()

def create_generation_offspring(generation_df,known_dna):
    latency = list(generation_df['Latency'])
    PowerConsumption = list(generation_df['PowerConsumption'])
    no_processors = list(generation_df['Number of Processors'])
    objective_scores = np.array([latency,PowerConsumption,no_processors]).T
    fronts,ranks = pareto_rank(np.array(objective_scores))
    crowd_distances =crowding_distance(fronts,ranks)
    mating_pool = tournament(ranks, pop_size, tournament_rounds,crowd_distances)
    mating_pool = np.unique(mating_pool)
    parents =list(generation_df[generation_df.columns[15:]].iloc[mating_pool].values)
    offspring,known_dna,_ = create_offspring(parents,parents_per_child,pop_size,mutation_chance,gene_pool,known_dna)
    return offspring,known_dna
if gen_no!=0:
    for i,row in generation_df.iterrows():
        row_genes = generation_df[generation_df.columns[15:]]
        known_dna.add(tuple(list(row_genes)))

if __name__ == "__main__":
    if gen_no == 0:
        generation_genes_df = pd.DataFrame()
        generation,known_dna = create_initial_population(gene_pool,pop_size,known_dna)
        for processor in generation:
            row = pd.DataFrame([processor],columns = columns)
            generation_genes_df = generation_genes_df.append(row)
        for i in range(no_parallel_simulations):
            poosl_model_generator.setup_simulation(i)
        results = autosim_multiproc.autosim_multiproc(perform_simulation_finetune,generation_genes_df,no_parallel_simulations)
        generation_df = generation_df.append(results)
        generation_df.to_csv("generations/generation0.csv",index=False)
        gen_no+=1
    while gen_no < max_gen:
        print("Generation : {0}".format(gen_no))
        offspring,known_dna = create_generation_offspring(generation_df,known_dna)
        generation_genes_df = pd.DataFrame()
        for processor in offspring:
            row = pd.DataFrame([processor],columns = columns)
            generation_genes_df = generation_genes_df.append(row)
        results = autosim_multiproc.autosim_multiproc(perform_simulation_finetune,generation_genes_df,no_parallel_simulations)
        generation_df = generation_df.append(results)
        generation_df.to_csv('generations/generation{0}.csv'.format(gen_no),index=False)
        gen_no+=1

    



