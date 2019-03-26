
def add_paretorank_and_save(generation_df,gen):
    latency = list(generation_df['Latency'])
    PowerConsumption = list(generation_df['PowerConsumption'])
    no_processors = list(generation_df['Number of Processors'])
    
    objective_scores = np.array([latency,PowerConsumption,no_processors]).T
    fronts,ranks = pareto_rank(np.array(objective_scores))

    generation_df['pareto rank'] = ranks
    generation_df.to_csv('generation{0}.csv'.format(gen),index=False)