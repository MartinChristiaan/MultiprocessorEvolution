import math
import random
import matplotlib.pyplot as plt
import numpy as np
from geneticdrift import *
from paretosurvival import *


def create_offspring(parents,parents_per_child,no_offspring,mutation_chance,possible_genes,known_dna):
    n = len(parents)
    children = []
    i_attempt = 0
    failed = False
    while len(children) < (no_offspring): 
        i_attempt+=1
        if i_attempt>no_offspring*10:
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
        
    return children,failed