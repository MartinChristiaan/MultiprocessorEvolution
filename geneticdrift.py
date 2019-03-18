import math
import random
import matplotlib.pyplot as plt
import numpy as np
from geneticdrift import *
from selection import *


def create_inital_population(gene_pool,pop_size):
    population = []
    known_dna = set()
    while len(population) < pop_size:
        pot_dna = [random.choice(possible_gene) for possible_gene in gene_pool]
        pot_dna_hash = tuple(pot_dna)
        if pot_dna_hash not in known_dna:
            known_dna.add(pot_dna_hash)
            population.append(pot_dna)
    return population,known_dna



def create_offspring(parents,parents_per_child,no_offspring,mutation_chance,possible_genes,known_dna):
    n = len(parents)
    children = []
    i_attempt = 0
    failed = False
    my_mut_change =mutation_chance
    while len(children) < (no_offspring): 
        i_attempt+=1
        if i_attempt>3*no_offspring:
            mutation_chance+=0.3            
            
        
        if i_attempt > no_offspring*5:
            failed = True
            break
        parents = [random.choice(parents) for p in range(parents_per_child)]
        dna = []
        for gene in range(len(parents[0])):
            r = random.random()
            if r > mutation_chance:
                available_genes = [parent[gene] for parent in parents]
                dna.append(random.choice(available_genes))
            else:
                dna.append(random.choice( possible_genes[gene]))
        dna_hash = tuple(dna)
        if dna_hash not in known_dna:
            known_dna.add(dna_hash)
            children.append(dna)
        
    return children,known_dna,failed