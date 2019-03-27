import os, sys, subprocess, time, select
from threading import Timer

try:
    from IPython.core.display import HTML, display # used to display the progress in the IPython notebook
    def stdout(msg):
        if msg:
            display(HTML("<pre style=\"color:blue\">" + msg  + "</pre>"))
            
    def stderr(msg):
        if msg:
            display(HTML("<pre style=\"color:red\">" + msg + "</pre>"))

except ImportError:
    def stdout(msg):
        sys.stdout.write(msg)
            
    def stderr(msg):
        sys.stderr.write(msg)

def runrotalumis(model_file, output_directory, library_paths=[]):
    """model is a path to a model (relative to the rotalumis executable, or absolute)
    The runner will execute the model and print the output to the IPython/Jupyter notebook.
    Returns the exit code of the Rotalumis process
    """
    basedir = os.path.abspath(os.path.dirname(str(__file__)))
    
    prev_dir = os.getcwd()
    
    if not os.path.isdir(output_directory):
        os.makedirs(output_directory)
    
    try:
        rotalumis_bin = os.path.join(basedir, "rotalumis.exe")
        if not os.path.isfile(rotalumis_bin):
            raise Exception("Could not locate Rotalumis in " + rotalumis_bin)
            
        if not os.path.isabs(model_file):
            inputmodel = os.path.join(prev_dir, model_file)
        else:
            inputmodel = model_file

        lib_includes = []
        
        for l in library_paths:
            lib_includes += ["-I", l]

        os.chdir(output_directory) # make sure the outputs are going into this folder!                    
        0
        try:
            
            p = subprocess.Popen([os.path.join(basedir, "rotalumis.exe"), '--poosl', inputmodel] + lib_includes, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            def stop_process():
                try: 
                    p.terminate()
                except:
                    pass
            t = Timer(200,stop_process)
            t.start()            
            while p.poll() is None:
                #print(p.stdout.read().decode('utf-8'))
                print(p.stderr.read().decode('utf-8'))
                
                time.sleep(0.1)
        finally:
            returncode = p.returncode
            p.terminate()
           
                
    finally:
        # always put the current working directory back!
        os.chdir(prev_dir)
        
    return returncode
    
if __name__ == "__main__":    
    runrotalumis(sys.argv[1], sys.argv[2], sys.argv[3:])
