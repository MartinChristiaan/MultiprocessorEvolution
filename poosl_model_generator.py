# Copies a new directory
# Redirects outputs.
import shutil
import os


def fix_file_destinations(f,simpath,checkword):    
    simpath = simpath.replace("\\",'\\'*2)
    lines = f.readlines()
    for i_line,line in enumerate(lines):
        words = line.split()
        for i_word,word in enumerate(words):
            if word == checkword:
                words[i_word+1] = '"'+simpath+"\\"*2 + '"' + "+"+words[i_word+1]   
                lines[i_line] = " "*8 +" ".join(words)+"\n"
    return lines

def setup_simulation(i):
    mydir="poosl_model" +str(i)
    if os.path.isdir(mydir):
        shutil.rmtree(mydir)
    shutil.copytree("poosl_model_source",mydir ) 
    #f = open("poosl_model_source\libraries\performance.poosl")
    f2 = open("poosl_model_source\dse\platform\ProcessorStatus.poosl")
    path = os.getcwd() + '\\' + mydir + '\\simulator'
    
    #f_dest = mydir + "\libraries\performance.poosl"
    f2_dest = mydir + "\dse\platform\ProcessorStatus.poosl"
    #dest = open(f_dest,'w')
    dest2 = open(f2_dest,'w')
    #dest.writelines(fix_file_destinations(f,path,"destination("))
    dest2.writelines(fix_file_destinations(f2,path,"source("))
    return mydir

