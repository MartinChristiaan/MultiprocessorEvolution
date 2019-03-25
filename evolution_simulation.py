
import numpy as np
#import matplotlib.pyplot as plt
import random
from selection import pareto_rank,tournament,crowding_distance
from geneticdrift import create_offspring,create_initial_population
from simulation import perform_simulation
from task_scheduler import schedule_tasks
import pandas as pd
import autosim_multiproc
import poosl_model_generator
def quotate(mystr):
    return '"' + mystr + '"'
columns = ["NodeProcessorType1","NodeProcessorType2","NodeProcessorType3","NodeProcessorType4","NodeProcessorType5","NodeProcessorType6","VSF1","VSF2","VSF3","VSF4","VSF5","VSF6","OSPolicy1","OSPolicy2","OSPolicy3","OSPolicy4","OSPolicy5","OSPolicy6"]

pop_size = 70
parents_per_child=2
mutation_chance = 0.15
no_parallel_simulations = 1
NodeProcessorTypes = [quotate(s) for s in [ "Adreno"]*2 +["MIPS"]*2+["ARMv8"]]  
VSFs =  [str(1.0)] * 5+[str(2.0/3.0)]*2+[str(1.0/2.0)] + [str(1.0/4)]
OSPolicys = [quotate(s) for s in ["FCFS","PB"]]
gene_pool = [NodeProcessorTypes]*6 + [VSFs]*6 + [OSPolicys]*6
tournament_rounds = 2
max_gen = 70
gen_no = 0

def add_paretorank_and_save(generation_df,gen):
    latency = list(generation_df['Latency'])
    PowerConsumption = list(generation_df['PowerConsumption'])
    no_processors = list(generation_df['Number of Processors'])
    objective_scores = np.array([latency,PowerConsumption,no_processors]).T
    fronts,ranks = pareto_rank(np.array(objective_scores))

    generation_df['pareto rank'] = ranks
    generation_df.to_csv('generation{0}.csv'.format(gen),index=False)



while True:
    try:
        generation_df = pd.read_csv('generation' + str(gen_no) + '.csv')
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
        results = autosim_multiproc.autosim_multiproc(perform_simulation,generation_genes_df,no_parallel_simulations)
        generation_df = generation_df.append(results)
        generation_df.to_csv("generation0.csv",index=False)
        gen_no+=1
    while gen_no < max_gen:
        print("Generation : {0}".format(gen_no))
        offspring,known_dna = create_generation_offspring(generation_df,known_dna)
        generation_genes_df = pd.DataFrame()
        for processor in offspring:
            row = pd.DataFrame([processor],columns = columns)
            generation_genes_df = generation_genes_df.append(row)
        results = autosim_multiproc.autosim_multiproc(perform_simulation,generation_genes_df,no_parallel_simulations)
        generation_df = generation_df.append(results)
        add_paretorank_and_save(generation_df,gen_no)
        gen_no+=1

    



