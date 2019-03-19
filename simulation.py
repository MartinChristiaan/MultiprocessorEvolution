import run_network_model
import os
import random
from poosl_model_generator import setup_simulation
import shutil
from task_scheduler import schedule_tasks

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
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def perform_simulation(dna,i=0):
    task_map_names = ['MapTask1To','MapTask2To','MapTask3To',"MapTask4To","MapTask5To","MapTask6To","MapTask7To","	MapTask8To","MapTask9To","MapTask10To","MapTask11To"]
    node_processor_types = dna[:6]
    vsfs = dna[6:12]
    os_policies = dna[12:]
    taskmaps = schedule_tasks(node_processor_types,vsfs)
    mydir = "poosl_model"+str(i)

    latency = 99999
    power_consumption = 99999
    no_processors = 99999
    names = ["Latency","PowerConsumption","Number of Processors"] + task_map_names
    best_taskmap = taskmaps[0]
    succes = 0
    for taskmap in taskmaps:
        model_params = create_model_params(taskmap,node_processor_types,vsfs,os_policies)
        simulate_processor(model_params,mydir)
        f = open(mydir+"/Application.log", "r")
        output = f.read()
        words = output.split()
        if not words[0] == "Failed":
            succes+=1
            new_latency = float(words[28])
            if new_latency < latency:
                latency = new_latency
                f= open(mydir+"/Battery.log", "r")
                output = f.read()
                words = output.split()
                cnt=0
                avg_power = 0
                for word in words:
                    if is_number(word):
                        cnt+=1
                        if cnt == 2:
                            avg_power = float(word)

                
                f= open(mydir+"/BatteryTrace.xml", "r")
                output = f.read()
                words = output.split()
                total_time = float(words[-3].split("'")[1])
                power_consumption = total_time * avg_power
                no_processors = len(set(taskmap))
                best_taskmap = taskmap
        if succes == 3:
            break
    values = [latency,power_consumption,no_processors]
    values.extend(best_taskmap)
    return names,values
   
