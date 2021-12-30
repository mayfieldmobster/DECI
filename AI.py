import zipfile
import ast
import node
import os
import json
import TF_run
import Torch_run
import re


def write_script(string):
    open("model.py", "w").close()
    script = " ".join(string)
    script = ast.literal_eval(script)
    with open("model.py", "w") as file:
        for line in script:
            file.write(line)
    return script

def write_dependencies(string):
    with open("text.zip","wb") as file:
        file.write(bytes(string))

    #with zipfile.ZipFile("depen.zip", 'r') as zip_ref:
        #zip_ref.extractall(".")#


def no_read(lines):
    no_virus = True

    lines= lines.replace('\n','')
    lines

    linux = ["/bin", "/boot", "/cdrom", "/dev", "/etc", "/home", "/lib", "/lost+found", "/media", "/mnt", "/opt", "/proc", "/root", "/run", "/sbin", "/selinux", "/srv", "/tmp", "/usr", "/var"]

    aloud = ["'r'", "'rb'", '"r"', '"rb"']
    for line in lines:
        if "open" in line:
            info = re.findall(r'\(.*?\)', line)[0]
            info = info.replace("(", "").replace(")", "").split(",")

            for mode in aloud:
                if mode != info[1]:#if second val in open("lol.txt","wb")
                    no_virus = False
                    break

            for val in info: #if mode used open(mode="wb", "file=lol.txt")
                if "mode" in val:
                    for mode in aloud:
                        if mode in val:
                            no_virus = False
                            break
        if "C:" in line:
            no_virus = False
            break

        if ".." in line:
            no_virus = False
            break

        if "raise" in line:
            no_virus = False
            break

        if "compile(" in line:
            no_virus = False
            break

        if "eval" in line:
            no_virus = False
            break

        if "exec" in line:
            no_virus = False
            break

        if "__import__"in line:
            no_virus = False
            break


        for directory in linux:
            if directory in line:
                no_virus = False
                break

    return no_virus



def please_no_hack():

    libraries = ["tensorflow",
                 "torch",
                 "keras",
                 "glob",
                 "cv2",
                 "numpy",
                 "matplotlib",
                 "time",
                 "PIL"]

    with open("model.py", "r") as file:
        lines = file.readlines()
        no_malware = no_read(lines)
        virus = False
        framework = ""
        if not no_malware:
            return True, ""
        for line in lines:
            if "import" in line:
                if "#" in line or "'" in line or '"' in line or "," in line:
                    return True, ""
                for library in libraries:
                    if library in line:
                        if library == "tensorflow":
                            virus = False
                            framework = "tensorflow"
                        if library == "torch":
                            virus = False
                            framework = "torch"
                    else:
                        return True, ""


    return virus, framework



def tf_config(nodes, index):
    tf_config = {
        "cluster": {
            "worker": nodes
        },
        "task": {"type": "worker", "index": index}
    }
    os.environ['TF_CONFIG'] = json.dumps(tf_config)

def AI_REQ(message):
    del message[0]#delete IP
    del message[0]#delete protocol
    worker_index = int(message[0])
    del message[0]
    script_identity = message[0]
    del message[0]
    nodes = ast.literal_eval(message[0])
    del message[0]#wipe info so just left with script
    batch_size = int(message[0])
    del message[0]
    write_script(message)
    dependencies = node.request_reader("DEP")
    print("d: ",dependencies)
    dependencies = dependencies[0].split(" ")
    dep_identity = dependencies[2]

    if dep_identity == script_identity:
        print([dependencies[3]])
        if len(dependencies[3]) % 2 != 0:
            print(str(type(len(dependencies[3])/2)))
            write_dependencies(bytes.fromhex("0" + dependencies[3])) #https://stackoverflow.com/questions/56742408/valueerror-non-hexadecimal-number-found-in-fromhex-arg-at-position/56742540
        else:
            print(str(type(len(dependencies[3])/2)))
            write_dependencies(bytes.fromhex(str(dependencies[3])))

    """
    virus, framework = please_no_hack()
    if not virus:

        if framework == "tensorflow":
            tf_config(nodes, worker_index)
            print(os.environ['TF_CONFIG'])
            TF_run.run(batch_size)

        if framework == "torch":
            master_node = nodes[0].split(":")
            os.environ['MASTER_ADDR'] = master_node[0]
            os.environ['MASTER_PORT'] = master_node[1]
            Torch_run.run()

    
    """


