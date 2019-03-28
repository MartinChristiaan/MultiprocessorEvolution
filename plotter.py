import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
matplotlib.style.use('ggplot')
import numpy as np
import random
from selection import pareto_rank,tournament,crowding_distance
import matplotlib.cm as cm
def get_dims(nplots):
    if nplots == 1 : return 1,1
    if nplots == 2 : return 1,2
    if nplots == 3 : return 1,3
    if nplots == 4 : return 2,2
    if nplots == 5 : return 1,5
    if nplots == 6 : return 2,3
    if nplots == 7 : return 1,7
    if nplots == 8 : return 2,4
    if nplots == 9 : return 3,3


def filter_df(df, eq_filter = [],neq_filter = []):
    for fval in eq_filter:
        df = df[df[fval[0]] == fval[1]]
    for fval in neq_filter:
        df = df[df[fval[0]] != fval[1]]
    return df
def create_figure(figtype = "paper"):
    plt.figure(figsize=(3.8,2.7))    

def seperate_dim(df,dim):
    sep_id = df[dim].unique()
    sep_id.sort()
    sep = [df[df[dim] == i] for i in sep_id]
    return sep,sep_id

def make_fig(names,dataframes,xdim,ydim,tracedim,usesize =False):
    for k,df in enumerate(dataframes):
        create_figure()
        
        latency = list(df['Latency (s)'])
        PowerConsumption = list(df['Energy Consumption (j)'])
 #       no_processors = list(generation_df['Number of Processors'])
        objective_scores = np.array([latency,PowerConsumption]).T
        fronts,ranks = pareto_rank(np.array(objective_scores))

        df['pareto rank'] = ranks
        df_par = df[df['pareto rank'] ==1]
        df_par = df_par.sort_values(xdim)
        pareto_x = df_par[xdim]
        pareto_y = df_par[ydim]
        if usesize:
            plot_with_size(df,xdim,ydim,tracedim,xlims = (0.025,0.06),ylims = (0.0028,0.005),xline=pareto_x,yline = pareto_y)        
        
        else:
            plot_traces(df,xdim,ydim,tracedim,xlims = (0.025,0.06),ylims = (0.0028,0.005),xline=pareto_x,yline = pareto_y)        
        plt.savefig("figures/" + str(names[k]).replace(" ",'') +ydim.replace(" ",'').replace("(",'').replace(")",'')+tracedim.replace(" ",'')+".pdf")



def plot_traces(df,x_dim,y_dim,trace_dim,trace_label_fun = None, title_fun = None,annotate = False,xlims = [], ylims = [],xline = [],yline=[]):
    df = df.sort_values(x_dim)
    markers = ["o","v","^","<",">","8","s","p","*","h","H"]
    
#     for i,plotd in enumerate(plots):
#         ax = plt.subplot(dimy,dimx,i+1)
#         plt_title = str(plotd)
#         if not title_fun == None:
#             plt_title = title_fun(plotd)
#         ax.set_title(plt_title)
#         plot_df = df[df[d.plot_dim] == plotd]
#         traces = plot_df[d.trace_dim].unique()
#         traces.sort()
# #            mylines = []
    
    traces,trace_values = seperate_dim(df,trace_dim)
    for k,trace in enumerate(trace_values):
        trace_df = traces[k]
        x = trace_df[x_dim]
        y = trace_df[y_dim]
        mylabel = str(trace)
        if trace_label_fun!=None:
            mylabel = trace_label_fun(trace)
        plt.plot(x,y,linestyle = "None",label = mylabel,marker = markers[k])
        if annotate:
            line_end = x.values[-1], y.values[-1]
            plt.annotate(mylabel, xy=line_end,  xycoords='data',
                xytext=line_end,horizontalalignment='right', verticalalignment='top'
                )
    if len(xline)>0:
        plt.plot(xline,yline,label = "F",linestyle = ":",color = "red")


        plt.fill_between(np.concatenate((xline,[1000])),np.concatenate((yline,[min(yline)])),1000,alpha=0.2)
    plt.legend()
    plt.xlabel(x_dim)
    plt.ylabel(y_dim)
    plt.grid(1)
    plt.tight_layout()
    if len(xlims) == 2:
        plt.xlim(xlims)
    if len(ylims) == 2:
        plt.ylim(ylims)
    
    return plt

import matplotlib.colors as mcolors
import matplotlib.cm as cm

def plot_with_size(df,x_dim,y_dim,trace_dim,trace_label_fun = None, title_fun = None,annotate = False,xlims = [], ylims = [],xline = [],yline=[]):
    df = df.sort_values(x_dim)
    
#     for i,plotd in enumerate(plots):
#         ax = plt.subplot(dimy,dimx,i+1)
#         plt_title = str(plotd)
#         if not title_fun == None:
#             plt_title = title_fun(plotd)
#         ax.set_title(plt_title)
#         plot_df = df[df[d.plot_dim] == plotd]
#         traces = plot_df[d.trace_dim].unique()
#         traces.sort()
# #            mylines = []
    
    traces,trace_values = seperate_dim(df,trace_dim)
    print(trace_values)
    normalize = mcolors.Normalize(vmin=min(trace_values), vmax=max(trace_values))
    colormap = cm.YlOrBr
    for k,trace in enumerate(trace_values):
        trace_df = traces[k]
        x = trace_df[x_dim]
        y = trace_df[y_dim]
        mylabel = str(trace)
        if trace_label_fun!=None:
            mylabel = trace_label_fun(trace)
        
        plt.plot(x,y,linestyle = "None",label = mylabel,marker = "o",color=colormap(normalize(trace_values[k])))
        if annotate:
            line_end = x.values[-1], y.values[-1]
            plt.annotate(mylabel, xy=line_end,  xycoords='data',
                xytext=line_end,horizontalalignment='right', verticalalignment='top'
                )
    if len(xline)>0:
        plt.plot(xline,yline,label = "F",linestyle = ":",color = "red")


        plt.fill_between(np.concatenate((xline,[1000])),np.concatenate((yline,[min(yline)])),1000,alpha=0.2)
    #plt.legend()
    plt.xlabel(x_dim)
    plt.ylabel(y_dim)
    plt.grid(1)
    plt.tight_layout()
    if len(xlims) == 2:
        plt.xlim(xlims)
    if len(ylims) == 2:
        plt.ylim(ylims)
    scalarmappaple = cm.ScalarMappable(norm=normalize, cmap=colormap)
    scalarmappaple.set_array(trace_values)
    plt.colorbar(scalarmappaple)











