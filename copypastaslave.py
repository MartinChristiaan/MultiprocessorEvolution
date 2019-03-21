def merge(lines,combi_low,combi_high,prefix,postfix):
    
    combi_low_str = str(combi_low)
    combi_high_str = str(combi_high)

    for i,line in enumerate(lines):
        words = line.split()
        for i_word,word in enumerate(words):
            if word == prefix + combi_low_str + postfix:
               words[i_word] = prefix + combi_low_str + combi_high_str + postfix
            if word == prefix + combi_low_str + postfix:
                lines.remove(line)
                break
        lines[i] = " ".join(words)
            
def merge2(lines,combi_low,combi_high,prefix):
    
    combi_low_str = str(combi_low)
    combi_high_str = str(combi_high)

    for i,line in enumerate(lines):
        words = line.split()
        for i_word,word in enumerate(words):
            if prefix + combi_low_str in word :
               words[i_word] = prefix + combi_low_str + combi_high_str + word[len(prefix):]
            if word == prefix + combi_high_str:
               words[i_word] = prefix + combi_low_str + combi_high_str + word[len(prefix):]
            
        lines[i] = " ".join(words)

def merge3(lines,combi_low,combi_high,prefix):
    
    combi_low_str = str(combi_low)
    combi_high_str = str(combi_high)

    for i,line in enumerate(lines):
        words = line.split()
        for i_word,word in enumerate(words):
            if prefix + combi_low_str in word :
               words[i_word] = prefix + combi_low_str + combi_high_str + word[len(prefix):]
            if word == prefix + combi_high_str:
               del lines[i]
               break
            
        lines[i] = " ".join(words)





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

    m = lambda prefix,postfix : merge(lines,combi_low,combi_high,prefix,postfix)
    m("Task",".poosl")
    m('G',':')
    m("Task",":")
    m("MapTask","To")
    merge2(post_channel_lines,combi_low,combi_high,"Task")
    merge3(post_channel_lines,combi_low,combi_high,"Task")
    merge2(post_channel_lines,combi_low,combi_high,"Task")


    
    


    








        
        



