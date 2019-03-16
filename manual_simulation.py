import pandas as pd
import autosim
import simulation
import poosl_model_generator
def quotate(mystr):
    return '"' + mystr + '"'


df_taskmaps = pd.read_csv('population.csv')


mydir = poosl_model_generator.setup_simulation(0)
result = autosim.autosim(lambda dna : simulation.perform_simulation(dna,mydir),df_taskmaps)
print(result)

# Read df And convert to a list of genes
# Append stuff
# Simulate with autosim


