def merge(lines,combi_low,combi_high,prefix,postfix):
    
    combi_low_str = str(combi_low)
    combi_high_str = str(combi_high)

    for i,line in enumerate(lines):
        words = line.split()
        delete = False
        for i_word,word in enumerate(words):
            if word == prefix + combi_low_str + postfix:
               words[i_word] = prefix + combi_low_str + combi_high_str + postfix
            if word == prefix + combi_high_str + postfix:
               delete = True
        if delete:
            del lines[i]                
        else:
          lines[i] = " ".join(words)+ "\n"

def merge_replace_high_word(lines,combi_low,combi_high,prefix,postfix):
    
    combi_low_str = str(combi_low)
    combi_high_str = str(combi_high)

    for i,line in enumerate(lines):
        words = line.split()
        for i_word,word in enumerate(words):
            if word == prefix + combi_low_str + postfix:
               words[i_word] = prefix + combi_low_str + combi_high_str + postfix
            if word == prefix + combi_high_str + postfix:
                del words[i_word]
                
        lines[i] = " ".join(words)+ "\n"
      
            
def merge2(lines,combi_low,combi_high,prefix):
    
    combi_low_str = str(combi_low)
    combi_high_str = str(combi_high)

    for i,line in enumerate(lines):
        words = line.split()
        for i_word,word in enumerate(words):
            
            result = word.find(prefix + combi_low_str)
            if result!=-1:
                words[i_word] = word[:result] + prefix + combi_low_str + combi_high_str + word[result + len(prefix) + 1:] 
            result = word.find(prefix + combi_high_str)
            if result!=-1:
                words[i_word] = word[:result] + prefix + combi_low_str + combi_high_str + word[result + len(prefix) + 1:] 
        
        lines[i] = " ".join(words)+ "\n"

def merge3(lines,combi_low,combi_high,prefix):
    
    combi_low_str = str(combi_low)
    combi_high_str = str(combi_high)

    for i,line in enumerate(lines):
        words = line.split()
        for i_word,word in enumerate(words):
            
            result = word.find(prefix + combi_low_str)
            if result!=-1:
                words[i_word] = word[:result] + prefix + combi_low_str + combi_high_str + word[result + len(prefix) + 1:] 
            result = word.find(prefix + combi_high_str)
            if result!=-1:
                words[i_word] = "" 
        
        lines[i] = " ".join(words)+ "\n"



def generate_template(combi_low,combi_high,dest):
    f = open('poosl_model_source/dse_template.poosl')
    lines = f.readlines()
    merge(lines,combi_low,combi_high,"MapTask","To")
    merge(lines,combi_low,combi_high,"PriorityTask","")
    f = open(dest,'w')
    f.writelines(lines)

def generate_application(combi_low,combi_high,dest):
    f = open('poosl_model_source/dse/application/application.poosl')
    lines = f.readlines()
    pre_channel_lines = lines[:84]
    post_channel_lines = lines[84:]

    m = lambda prefix,postfix : merge(pre_channel_lines,combi_low,combi_high,prefix,postfix)
    
    m('"Task','.poosl"')
    merge_replace_high_word(pre_channel_lines,combi_low,combi_high,"MapTask","To,")
    merge_replace_high_word(pre_channel_lines,combi_low,combi_high,"PriorityTask",",")
    merge(pre_channel_lines,combi_low-1,combi_high-1,'G',':')
    m("Task",":")
    m("Task","(MapTo")
    m("PriorityTask",")")   

    #merge_replace_high_word(post_channel_lines,combi_low,combi_high,"G",".Communication,")


    merge2(post_channel_lines,combi_low,combi_high,"Task")
    merge3(post_channel_lines,combi_low-1,combi_high-1,"G")

    lines = pre_channel_lines + post_channel_lines

   #  merge2(post_channel_lines,combi_low,combi_high,"Task")


def merge4(lines,combi_low,combi_high,prefix):
    
    combi_low_str = str(combi_low)
    combi_high_str = str(combi_high)

    for i,line in enumerate(lines):
        words = line.split()
        for i_word,word in enumerate(words):
            result = word.find(prefix + combi_high_str)
            if result!=-1:
                words[i_word] = "" 
        
        lines[i] = " ".join(words)+ "\n"

def generate_task1(combi_low,combi_high,dest):
    f = open('poosl_model_source/dse/application/task1.poosl')
    lines = f.readlines()
    merge4(lines,combi_low-1,combi_high-1,"G")
    for i,line in enumerate(lines[:-1]):
        if "and" in line and len(lines[i+1].split()) == 0:
            del lines[i]
            del lines[i]
    f = open(dest,'w')
    f.writelines(lines)


def copypaste_til_emptyline(lines_main,lines_extra,triggerword,sepchar):
    adding = False
    copiedlines = []
    for line in lines_extra:
        if not adding:
            words = line.split()
            for i,word in enumerate(words):
              
                if word == triggerword:
                    adding = True
                    copiedlines.append(" ".join(words[i+1:])+"\n")
        else:
            if line.strip() == "":
                print("Empty line")
                break
            else:
                copiedlines.append(line)
    searching = False
    paste_line = 0
    for i_line,line in enumerate(lines_main):
        words = line.split()
        if not searching:
            for i,word in enumerate(words):
           
                if word == triggerword:
                    searching = True

        else:
            
            if line.strip() == "":
                paste_line = i_line
                lines_main[i_line-1]=lines_main[i_line-1][:-1] + sepchar + "\n"
                break
    return lines_main[:paste_line] + copiedlines + lines_main[paste_line:]







def generate_combi_task(combi_low,combi_high,dest):
    f1 = open('poosl_model_source/dse/application/task{0}.poosl'.format(combi_low))
    lines = f1.readlines()
    lines[2] = lines[2].replace("Task{0}".format(combi_low),"Task{0}{1}".format(combi_low,combi_high))
    f2 = open('poosl_model_source/dse/application/task{0}.poosl'.format(combi_high))
    lines2 = f2.readlines()
    # lines = copypaste_til_emptyline(lines,lines2,"ports")
    # lines = copypaste_til_emptyline(lines,lines2,"Control!MappedTo(String),")
    lines = copypaste_til_emptyline(lines,lines2,"CheckTokenAvailabilityForReads(Scenario:String)()",";")

    f = open(dest,'w')
    f.writelines(lines)

#generate_template(2,3,"temp.poosl")
generate_combi_task(3,4,"temp.poosl")

    








        
        



