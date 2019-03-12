import math
import random
import matplotlib.pyplot as plt
import numpy as np
from geneticdrift import *
from paretosurvival import *


def create_offspring(parents,parents_per_child,no_offspring,mutation_chance,possible_genes):
    n = len(parents)
    children = []
    for i in range(no_offspring):
        parents = [random.choice(parents) for p in range(parents_per_child)]
        child = []
        for gene in range(len(parents[0])):
            r = random.random()
            if r > mutation_chance:
                available_genes = [parent[gene] for parent in parents]
                child.append(random.choice(available_genes))
            else:
                child.append(random.choice( possible_genes[gene]))
        children.append(child)
    return children