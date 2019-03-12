import run_network_model
import os
import random

def quotate(mystr):
    return '"' + mystr + '"'


MapTaskTos = [ quotate("Node" + str(i)) for i in range(1,7)]
NodeProcessorTypes = [quotate(s) for s in [ "ARMv8", "Adreno" , "MIPS"]]
VSFs =  ["1.0/1.0","2.0/3.0"]
OSPolicys = [quotate(s) for s in ["FCFS","PB"]]


def create_model_params(taskmaps,node_processor_types,voltage_scaling,os_policies):
    model_parameters = {"Application" : "Applicate"}
    for i,taskmap in enumerate(taskmaps):
        model_parameters["MapTask" + str(i+1) + "To"] =taskmap
    for i,proc_type in enumerate(node_processor_types):
        model_parameters["NodeProcessorType"+ str(i+1)] = proc_type
    for i,VSF in enumerate(voltage_scaling):
        model_parameters["VSF"+  str(i+1)] = VSF
    for i,OSPolicy in enumerate(os_policies):
         model_parameters["OSPolicy"+ str(i+1)] = OSPolicy
    return model_parameters

def simulate_processor(model_parameters,myid=0):
    output_directory_template = "\\poosl_model"+str(myid)
    model_path = os.getcwd()+'\\poosl_model'+str(myid)
    output_directory = os.path.abspath(output_directory_template)
    if run_network_model.run_network_model(
         [model_path], # library paths
         open(model_path + "\\dse_template.poosl").read(), # system instance template
         6,model_parameters, output_directory) == False:
             raise Exception("Model did not terminate to completion, check the output of Rotalumis!")

taskmaps = [random.choice(MapTaskTos) for _ in range(11)]
node_processor_types = [random.choice(NodeProcessorTypes) for _ in range(6)]
vsfs = [random.choice(VSFs) for _ in range(6)]
os_policies= [random.choice(OSPolicys) for _ in range(6)]

model_params = create_model_params(taskmaps,node_processor_types,vsfs,os_policies)
#print(model_params)
simulate_processor(model_params)
