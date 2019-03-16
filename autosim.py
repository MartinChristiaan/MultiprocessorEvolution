import pandas as pd
#from bus import simulate
import numpy as np
import time
import sys
def get_all_combinations(df):
    dims = []
    datas = []
    combi_data = []

    for column in df:
        col_data = [data for data in df[column].values if  str(data) != 'nan']
        dims.append(len(col_data))
        datas.append(col_data)

    for i,dim in enumerate(dims):
        combi_data.append([])

        post_i_mul =1    
        if i < len(dims)-1:
            post_i_mul =int(np.prod(dims[i+1:]))

        pre_i_mul = 1
        if i > 0:
            pre_i_mul = int(np.prod(dims[:i]))

        for pre in range(pre_i_mul):
            for data in datas[i]:
                for z in range(post_i_mul):
                    combi_data[i].append(data)
    combi_df = pd.DataFrame()
    for i,column in enumerate(df):
        combi_df[column] = combi_data[i]
    return combi_df

def example_sim(valA,valB,valC,valD):
    names = ["colE","colF"]
    vals = [valA + valB + valC,"Test : " + valD]
    return names,vals


def autosim(simfun,config_df,resultpath="result.csv"):

    result_df = pd.DataFrame()
    names = []
    newcols = []
    dt = 0
    for i,row in config_df.iterrows():

        tstart = time.time()
        str_1 = "Now simulating : "
        for j,cname in enumerate(config_df.columns):
            str_1 += " " + cname + " : " + str(row.values[j])

        itemsleft = config_df.shape[0]-i
        mystr = "items left : " + str(itemsleft)+ " ,time last sim :  {:.2f}".format(dt) + " sec ,est time rem : " + str(itemsleft * dt) + " sec"  
        
        print(str_1)
        print(mystr)
#        try:
        names,vals = simfun(list(row))
        colnames = names
        colnames.extend(config_df.columns)
        
        newrow = vals
        newrow.extend(row)
        row_df = pd.DataFrame([newrow],columns = colnames)
        result_df = result_df.append(row_df)
        # except Exception as e:
        #     print("There was a failure for " + str_1)
        #     print(e)
            
 
        dt = time.time()-tstart

    if resultpath!=None:
        result_df.to_csv("result.csv",index = False)
    return result_df
  






