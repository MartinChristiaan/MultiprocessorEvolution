import pandas as pd
from plotter import *
import matplotlib.pyplot as plt

import os
import numpy as np
df = pd.read_csv("ProcessorDistribution_ranked.csv")

no_ARM = "no_ARMv8"
no_MIPS = "no_MIPS"
no_Adreno = "no_Adreno"

no_proc = "Number of Processors"
Latency = "Latency (s)"
PowerConsumption = "Energy Consumption (j)" 


no_proc_df,no_proc_names = seperate_dim(df,no_proc)

# eq_filter = [(NIBufferCapacity,2)]
# neq_filter = [(LoadValue,0.15),(LoadValue,0.65),(LoadValue,0.45)]
# df_filt = filter_df(df,eq_filter=eq_filter,neq_filter = neq_filter)
make_fig(no_proc_names,no_proc_df,PowerConsumption,Latency,no_ARM)
make_fig(no_proc_names,no_proc_df,PowerConsumption,Latency,no_Adreno)
make_fig(no_proc_names,no_proc_df,PowerConsumption,Latency,no_MIPS)
plt.show()


