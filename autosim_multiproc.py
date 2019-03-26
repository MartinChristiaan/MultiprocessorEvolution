import pandas as pd
#from bus import simulate
import numpy as np
import time
import sys

from multiprocessing import Process,Queue
import os

def merge_results(nproc):      
    import pandas as pd       
    final_result = pd.DataFrame()
    for id in range(nproc):   
        result = pd.read_csv("result" + str(id) + ".csv")
        final_result = final_result.append(result,ignore_index=False)
        #os.remove("result" + str(id) + ".csv")
    final_result.to_csv("Final_result.csv")
    return final_result


def perform_sim(q,simfun,dim_names,id,result_df):
    

    while q.qsize()>0:
        row = list(q.get())
        row.append(id)
        names,vals = simfun(list(row),id)
        colnames = names
        colnames.extend(dim_names)
        newrow = vals
        newrow.extend(row[:-1])
        row_df = pd.DataFrame([newrow],columns = colnames)
        result_df = result_df.append(row_df)
        result_df.to_csv("result" + str(id) + ".csv",index = False)

    return
    

def autosim_multiproc(simfun,config_df,no_parallel_simulations):

    result_df = pd.DataFrame()
    names = []
    newcols = []
    dt = 0
    q = Queue()

    for i,row in config_df.iterrows():
        q.put(row)

    processes = []
    for i in range(no_parallel_simulations):
       df = pd.DataFrame()
       p = Process(target=perform_sim, args=(q,simfun,config_df.columns,i,df))
       p.start()
       processes.append(p)
    t_start = time.time()
    while q.qsize()>0:
        for p in range(no_parallel_simulations):
            tmod = os.path.getmtime('result{0}.csv'.format(p))
            if time.time() - t_start > 60*10 and time.time() - tmod >60*10:
                print("Process {0} is slacking".format(p))
                processes[p].terminate()
                df = pd.read_csv('result{0}.csv'.format(p))
                new_p = Process(target=perform_sim, args=(q,simfun,config_df.columns,i,df))
                processes.insert(p,new_p)
                t_start = time.time()
            else:
                print("Last result Process {0} {1} seconds ago".format(p,time.time() - tmod))
                
        
        print("{0} items remaining in the queue".format(q.qsize()))
        time.sleep(3)
    time.sleep(150)
    print("terminating")
    for i,p in enumerate(processes):
       p.terminate()
    return merge_results(no_parallel_simulations)
           



  






