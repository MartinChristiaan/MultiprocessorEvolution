import pandas as pd
import numpy as np
from selection import pareto_rank,tournament,crowding_distance

def insert_source_config(generation_df):
    source_df = pd.read_csv('generations/source.csv') 
    result_df = pd.DataFrame()
    for i,row in generation_df.iterrows():
        mydata = list(row)
        platform_id = mydata[15]
        platform = source_df.iloc[platform_id]
        proc_type_distribution = platform['NodeProcessorTypeDistribution']
        node_pref = platform['Number of Processors']
        combi_task = platform['Combined Tasks']
        mydata[15] = proc_type_distribution
        row_df = pd.DataFrame([mydata],columns = source_df.columns[:-5])
        result_df = result_df.append(row_df)
    return result_df







def add_paretorank_and_save(generation_df,gen):
    generation_df = generation_df[generation_df['Latency']<9000]
    generation_df = generation_df[generation_df['Number of Processors']<9000]
    generation_df = generation_df[generation_df['Number of Processors']>3]
    
    generation_df = generation_df[generation_df['PowerConsumption']>0.01]
    
    latency = list(generation_df['Latency'])
    PowerConsumption = list(generation_df['PowerConsumption'])
    no_processors = list(generation_df['Number of Processors'])
    objective_scores = np.array([latency,PowerConsumption,no_processors]).T
    fronts,ranks = pareto_rank(np.array(objective_scores))

    # Processor distribution
    # 
    combi_tasks = []


    generation_df['pareto rank'] = ranks
    no_mips = []
    no_arm = []
    no_adreno = []
    full_volt = []
    for i,row in generation_df.iterrows():
        # processors = list(row[15:21])
        proc_dist = row[15]
        nmips = int(proc_dist[1])
        nadreno = int(proc_dist[4])
        narm = int(proc_dist[7])
        # Which nodes are actually used?
        schedule = list(set(list(row[4:15])))
        vsfs = (list(row[16:22]))
        no_full_voltage = 0
        proc_used = []
        for task in schedule:
            proc_used+=[int(task[-2])-1]

        for v,vs in enumerate(vsfs):
            if v in proc_used:
                no_full_voltage+=float(vs)
        
        # for p,proc in enumerate(processors):
        #     if p in proc_used:
        #         if "MIPS" in proc:
        #             nmips +=1
        #         if "Adreno" in proc:
        #             nadreno+=1
        #         if "ARM" in proc:
        #             narm+=1

        no_mips+=[nmips]
        no_adreno+=[nadreno]
        no_arm+=[narm]
        full_volt +=[no_full_voltage/(nmips+nadreno+narm)]
        combi_task = row['Combined Tasks']
        
        if combi_task[1] == combi_task[4]:
            combi_tasks.append("(1, 1)")
        else:
            combi_tasks.append(combi_task)

    generation_df["no_1.0_VSFS"] = full_volt
    generation_df["no_MIPS"] = no_mips
    generation_df["no_Adreno"] = no_adreno
    generation_df["no_ARMv8"] = no_arm
    generation_df['Combined Tasks'] = combi_tasks
    
    generation_df.to_csv(gen,index=False)

#result = insert_source_config(pd.read_csv("generations/generation21.csv"))
#add_paretorank_and_save(result,"generations/evolution_result.csv")
#dd_paretorank_and_save(pd.read_csv('generations/ComboNodesAndProcTypes.csv'),0)
#add_paretorank_and_save(pd.read_csv('generations/Evolution_vs_Source.csv'),'generations/Evolution_vs_source_reranked.csv')