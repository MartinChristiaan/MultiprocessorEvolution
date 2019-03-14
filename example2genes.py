
import numpy as np
import matplotlib.pyplot as plt
import random
import numpy as np
from paretosurvival import pareto_rank,pareto_tournament,crowding_distance,calculate_score, calculate_paretoranks
from geneticdrift import create_offspring

class Evolver():
    def __init__(self):
        obj_fun1 = lambda a,b,c,d : a + b*b + c *d
        obj_fun2 = lambda a,b,c,d : 1/(0.2*a+1)*10 + np.sin(10*a) + np.sin(b)
        self.obj_funs= [obj_fun1,obj_fun2]
        self.pop_size = 30
        self.parents_per_child=2
        self.mutation_chance = 0.2
        self.possible_genes_combined = [np.linspace(0,20,200),np.linspace(0,20,200),np.linspace(0,20,200),np.linspace(0,20,200)] 
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
        self.population = np.array(population)
        self.objective_scores = calculate_score(self.population,self.obj_funs)
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
            self.objective_scores = calculate_score(self.population,self.obj_funs)
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
