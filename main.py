
import numpy as np
import matplotlib.pyplot as plt
import random
import numpy as np
from paretosurvival import pareto_rank,pareto_tournament,crowding_distance,calculate_score_and_pareto_rank
from geneticdrift import create_offspring

class Evolver():
    def __init__(self):
        obj_fun1 = lambda a,b,c : 1/a + np.sin(c)
        obj_fun2 = lambda a,b,c : a + b*c
        self.obj_funs= [obj_fun1,obj_fun2]
        self.pop_size = 30
        self.generations_limit = 20
        self.parents_per_child=2
        self.mutation_chance = 0.1
        self.possible_genes_combined = [np.linspace(0,10,1000),np.linspace(0,10,1000),np.linspace(0,10,1000)] 
        self.tournament_rounds = 2
        

    # Initialize First Population

        population = [[random.choice(possible_gene) for possible_gene in self.possible_genes_combined] for i in range(self.pop_size)]
        self.population = np.array(population)
        fronts,ranks,self.objective_scores = calculate_score_and_pareto_rank(population,self.obj_funs)
        mating_pool = pareto_tournament(ranks, self.pop_size, self.tournament_rounds)
        parents = self.population[mating_pool]
        offspring = create_offspring(parents,self.parents_per_child,self.pop_size,self.mutation_chance,self.possible_genes_combined)
        offspring = np.array(offspring)
        
        self.population = np.concatenate((parents,offspring))
     
    def evolve(self):
        fronts,ranks,self.objective_scores = calculate_score_and_pareto_rank(self.population,self.obj_funs)
        crowd_distances =crowding_distance(fronts,ranks)
        mating_pool = pareto_tournament(ranks, self.pop_size, self.tournament_rounds,crowd_distances)
        parents = self.population[mating_pool]
        offspring = create_offspring(parents,self.parents_per_child,self.pop_size,self.mutation_chance,self.possible_genes_combined)
        self.population = np.concatenate((parents,offspring))


evolver = Evolver()

# Update function


# Start App

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
app = QtGui.QApplication([])

win = pg.GraphicsWindow(title="Evolution Plotter")
win.resize(1000,600)
p5 = win.addPlot(title="Generation")

plt = p5.plot(evolver.objective_scores[:,0], evolver.objective_scores[:,1], pen=None, symbol='t', symbolPen=None, symbolSize=10, symbolBrush=(100, 100, 255, 200))
p5.setXRange(-10, 10)
p5.setYRange(-10, 15)

def update():
    evolver.evolve()
    plt.setData(evolver.objective_scores[:,0], evolver.objective_scores[:,1])

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(100)

if __name__ == '__main__':
    import sys
    QtGui.QApplication.instance().exec_()

# Population
