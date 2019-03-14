
import numpy as np
import matplotlib.pyplot as plt
import random
import numpy as np
from paretosurvival import pareto_rank,pareto_tournament,crowding_distance,calculate_score, calculate_paretoranks
from geneticdrift import create_offspring
from simulation import perform_simulation

MapTaskTos = [ quotate("Node" + str(i)) for i in range(1,7)]
NodeProcessorTypes = [quotate(s) for s in [ "ARMv8", "Adreno" , "MIPS"]]
VSFs =  ["1.0/1.0","2.0/3.0"]
OSPolicys = [quotate(s) for s in ["FCFS","PB"]]


def quotate(mystr):
    return '"' + mystr + '"'

def simulate_population(population):
    # Possibly use multiple processes
    return [perform_simulation(*tuple(dna)) for dna in population] 

def filter_tolowthroughput(results):
    return [result[:2] for result in results if result[0] > 500]


class Evolver():
    def __init__(self):
        self.pop_size = 30
        self.parents_per_child=2
        self.mutation_chance = 0.2



        self.possible_genes_combined = [MapTaskTos,NodeProcessorTypes,VSFs,OSPolicys] 
        self.tournament_rounds = 2
        self.known_dna = set()
        self.front_population = []
        self.failed= False
    # Initialize First Population

        population = []
        while len(population) < self.pop_size:
            pot_dna = [random.choice(possible_gene) for possible_gene in self.possible_genes_combined]
            pot_dna_hash = tuple(pot_dna)
            if pot_dna_hash not in self.known_dna:
                population.append(pot_dna)
                self.known_dna.add(pot_dna_hash)
        self.population = population
        results = simulate_population(self.population)
        self.objective_scores = filter_tolowthroughput(results)
        fronts,ranks = calculate_paretoranks(self.objective_scores)
        first_front = np.argwhere(ranks == 1)[:,0]
        self.front_population = self.population[first_front]
        self.front_scores = self.objective_scores[first_front,:]

        mating_pool = pareto_tournament(ranks, self.pop_size, self.tournament_rounds)
        parents = self.population[mating_pool]
        offspring,self.failed = create_offspring(parents,self.parents_per_child,self.pop_size,self.mutation_chance,self.possible_genes_combined,self.known_dna)
        offspring = np.array(offspring)
        self.population = offspring
     
    def evolve(self):
        if not self.failed:
            results = simulate_population(self.population)
            self.objective_scores = filter_tolowthroughput(results)
            combined_scores =np.concatenate((self.front_scores,self.objective_scores))
            combined_population = np.concatenate((self.front_population,self.population))
            fronts,ranks = calculate_paretoranks(combined_scores)
            crowd_distances =crowding_distance(fronts,ranks) # Crowding distance should memorized front 
            first_front = np.argwhere(ranks == 1)[:,0]
            self.front_population = combined_population[first_front]
            self.front_scores = combined_scores[first_front,:]
            
            mating_pool = pareto_tournament(ranks, self.pop_size, self.tournament_rounds,crowd_distances)
            parents = combined_population[mating_pool]
            offspring,self.failed = create_offspring(parents,self.parents_per_child,self.pop_size,self.mutation_chance,self.possible_genes_combined,self.known_dna)
            offspring = np.array(offspring)
            self.population = offspring
        else:
            print("Evolution completed") 


evolver = Evolver()

# Update function
# Start App

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
app = QtGui.QApplication([])

win = pg.GraphicsWindow(title="Evolution Plotter")
win.resize(1000,600)
p5 = win.addPlot(title="Generation")

plt = p5.plot(evolver.objective_scores[:,0], evolver.objective_scores[:,1], pen=None, symbol='t', symbolPen=None, symbolSize=10, symbolBrush=(255, 0, 0, 200))
plt_front = p5.plot(evolver.front_scores[:,0], evolver.front_scores[:,1], pen=None, symbol='t', symbolPen=None, symbolSize=10, symbolBrush=(0, 255, 0, 200))

x = np.linspace(0,20,200)
y =evolver.obj_funs[1](x)

plt2 = p5.plot(x,y)


def update():
    evolver.evolve()
    plt.setData(evolver.objective_scores[:,0], evolver.objective_scores[:,1])
    plt_front.setData(evolver.front_scores[:,0], evolver.front_scores[:,1])

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(100)

if __name__ == '__main__':
    import sys
    QtGui.QApplication.instance().exec_()

# Population
