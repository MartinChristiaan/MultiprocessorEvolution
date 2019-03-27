import run_network_model
import os
import random
from poosl_model_generator import setup_simulation
import shutil
from task_scheduler import schedule_tasks
from copypastaslave import write_combi_model
import datetime

def create_model_params(taskmaps,node_processor_types,voltage_scaling,os_policies,combi_high = 99):
    model_parameters = {"Application" : "Applicate"}
    for i,taskmap in enumerate(taskmaps):
        if i!=combi_high:
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
    return run_network_model.run_network_model(
         [model_path], # library paths
         open(model_path + "\\dse_template.poosl").read(), # system instance template
         6,model_parameters, output_directory)
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def perform_simulation(dna,i=0):
    task_map_names = ['MapTask1To','MapTask2To','MapTask3To',"MapTask4To","MapTask5To","MapTask6To","MapTask7To","	MapTask8To","MapTask9To","MapTask10To","MapTask11To"]
    proc_type_distribution = dna[0]
    node_pref = dna[1]
    combi_task = dna[2]
    if isinstance(proc_type_distribution, str):
        proc_type_distribution = (int(proc_type_distribution[1]),int(proc_type_distribution[4]),int(proc_type_distribution[7]))
    node_processor_types = ['"MIPS"']*proc_type_distribution[0] + proc_type_distribution[1]*['"Adreno"'] + proc_type_distribution[2] * ['"ARMv8"']
    vsfs = dna[3:9]
    os_policies = dna[9:15]


    #print("Evolving Task Schedule " + str(datetime.datetime.now().minute))
    ctc = (combi_task[0]-1,combi_task[1]-1)
    taskmaps = schedule_tasks(node_processor_types,vsfs,node_pref,ctc)
    for i in range(6-len(node_processor_types)):
        node_processor_types.append('"MIPS"')    
    mydir = "poosl_model"+str(i)
    
    latency = 99999
    power_consumption = 99999
    no_processors = 99999
    names = ["Latency","PowerConsumption","Number of Processors"] + ["Combined Tasks"] + task_map_names
    best_taskmap = taskmaps[0]
    succes = 0
    for i_tm,taskmap in enumerate(taskmaps):
        combi = combi_task
        write_combi_model(combi[0],combi[1],mydir)

        chigh = 99
        if combi[0] != combi[1]:
            chigh = combi[1]-1
        model_params = create_model_params(taskmap,node_processor_types,vsfs,os_policies,chigh)
        #print("Simulating" + str(datetime.datetime.now().minute))
        succeeeded = simulate_processor(model_params,mydir)

        f = open(mydir+"/Application.log", "r")
        output = f.read()
        words = output.split()
        if not words[0] == "Failed" and succeeeded:
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
        if succes == 1:
            break
    values = [latency,power_consumption,no_processors]
    values += [(combi_task[0],combi_task[1])]
    values.extend(best_taskmap)
    return names,values
   
