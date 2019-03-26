import pandas as pd
import numpy as np
from selection import pareto_rank,tournament,crowding_distance

import matplotlib
import matplotlib.pyplot as plt

matplotlib.style.use('ggplot')
plt.ion()



while True:
    for g in range(14):


        generation_df = pd.read_csv('generation{0}.csv'.format(g))
        generation_df = generation_df[generation_df['Latency']<9000]

        latency = list(generation_df['Latency'])
        PowerConsumption = list(generation_df['PowerConsumption'])
        no_processors = list(generation_df['Number of Processors'])
        objective_scores = np.array([latency,PowerConsumption,no_processors]).T
        fronts,ranks = pareto_rank(np.array(objective_scores))

        for p in [4,5,6]:
            plt.subplot(2,2,p-3)
            for i in range(max(ranks)):
                plt.title("Num Processors {0}, Gen : {1}".format(p,g))
                rank_ids = np.where(ranks == i+1)
                rank_data = generation_df.iloc[rank_ids]
                rank_data = rank_data[rank_data['Number of Processors'] == p]
                rank_data = rank_data.sort_values('PowerConsumption')
                plt.plot(rank_data['Latency'],rank_data['PowerConsumption'],marker = 'o')
            
            plt.xlabel('Latency')
            plt.ylabel('Power Consumption')

        plt.draw()
        plt.pause(1)
        plt.clf()

        


