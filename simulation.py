import run_network_model
import os
import random
from poosl_model_generator import setup_simulation
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

def simulate_processor(model_parameters,mydir):
    output_directory_template = mydir
    model_path = os.getcwd()+"\\"+ mydir
    output_directory = os.path.abspath(output_directory_template)
    if run_network_model.run_network_model(
         [model_path], # library paths
         open(model_path + "\\dse_template.poosl").read(), # system instance template
         6,model_parameters, output_directory) == False:
             raise Exception("Model did not terminate to completion, check the output of Rotalumis!")


def perform_simulation(dna,mydir):
    taskmaps = dna[:11]
    node_processor_types = dna[11:17]
    vsfs = dna[17:23]
    os_policies = dna[23:]
    model_params = create_model_params(taskmaps,node_processor_types,vsfs,os_policies)
    #print(model_params)
    simulate_processor(model_params,mydir)
    f = open(mydir+"/Application.log", "r")
    output = f.read()
    words = output.split()
    if words[0] == "Failed":
        print("Failed!")
        return 0,0,0,0
    else:
        print("Succes")
    throughput = float(words[11])
    latency = float(words[28])
    f= open(mydir+"/Battery.log", "r")
    output = f.read()
    words = output.split()
    print(words)
    avg_power = float(words[8])

    f= open(mydir+"/BatteryTrace.xml", "r")
    output = f.read()
    words = output.split()
    total_time = float(words[-3].split("'")[1])
    power_consumption = total_time * avg_power

    no_processors = len(set(taskmaps))
    return throughput,latency,power_consumption,no_processors

    


if __name__ == "__main__":
    taskmaps = [MapTaskTos[i] for i in[0,1,2,3,4,5,1,2,0,3,3]]# [0,0,0,0,0,0,0,0,0,0,0]]# 
    node_processor_types = [NodeProcessorTypes[i] for i in [0,1,1,2,0,2]] #[0,0,0,0,0,0]] #
    vsfs = [VSFs[i] for i in [1,0,0,0,1,0]]
    os_policies= [OSPolicys[i] for i in [0,0,0,0,0,0]]
    dna = taskmaps + node_processor_types + vsfs + os_policies
    mydir = setup_simulation(0)
    print(perform_simulation(dna,mydir))

