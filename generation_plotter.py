import pandas as pd
import numpy as np
from selection import pareto_rank,tournament,crowding_distance

import matplotlib
import matplotlib.pyplot as plt

matplotlib.style.use('ggplot')
generation_df = pd.read_csv('generation1.csv')
generation_df = generation_df[generation_df['Latency']<9000]

def plot_corr(df,size=10):
    '''Function plots a graphical correlation matrix for each pair of columns in the dataframe.

    Input:
        df: pandas DataFrame
        size: vertical and horizontal size of the plot'''

    corr = df.corr()
    fig, ax = plt.subplots(figsize=(size, size))
    ax.matshow(corr)
    plt.xticks(range(len(corr.columns)), corr.columns);
    plt.yticks(range(len(corr.columns)), corr.columns);

plot_corr(generation_df)
plt.show()

#pd.scatter_matrix(generation_df, alpha=0.2)


# plt.figure()
# for i in range(max(ranks)):
#     rank_ids = np.where(ranks == i+1)
#     rank_data = generation_df.iloc[rank_ids]
#     rank_data = rank_data.sort_values('PowerConsumption')
#     plt.plot(rank_data['Latency'],rank_data['PowerConsumption'],marker = 'o')

#     print(rank_data)
# plt.xlabel('Energy Conumption')
# plt.ylabel('Latency')
# plt.grid(1)
# plt.show()

