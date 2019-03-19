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
        os.remove("result" + str(id) + ".csv")
    #final_result.to_csv("Final_result.csv")
    return final_result


def perform_sim(q,simfun,dim_names,id):
    result_df = pd.DataFrame() 

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
    for i in range(1,no_parallel_simulations):
       p = Process(target=perform_sim, args=(q,simfun,config_df.columns,i))
       p.start()
       processes.append(p)
 
    while q.qsize()>0:
        tstart = time.time()
        row = list(q.get())
        row.append(0)
        itemsleft = q.qsize()
        str_1 = "Now simulating : "
        for j,cname in enumerate(config_df.columns):
            str_1 += " " + cname + " : " + str(row[j])

        mystr = "items left : " + str(itemsleft)+ " ,time last sim :  {:.2f}".format(dt) + " sec ,est time rem : " + str(itemsleft * dt) + " sec"  
        
        print(str_1)
        print(mystr)
        names,vals = simfun(list(row),0)
        colnames = names
        colnames.extend(config_df.columns)
        
        newrow = vals
        newrow.extend(row[:-1])
        row_df = pd.DataFrame([newrow],columns = colnames)
        result_df = result_df.append(row_df)
        result_df.to_csv("result0.csv",index = False)
        dt = time.time()-tstart
    for i,p in enumerate(processes):
       p.join()
    return merge_results(no_parallel_simulations)
           



  






