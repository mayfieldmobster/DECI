import ast
import node
import os
import json
import TF_run
import Torch_run
import re
import numpy as np


def write_script(string):
    open("../model.py", "w").close()
    script = " ".join(string)
    script = ast.literal_eval(script)
    with open("../model.py", "w") as file:
        for line in script:
            file.write(line)
    return script


def write_dependencies(string):
    with open("text.zip", "wb") as file:
        file.write(bytes(string))

    # with zipfile.ZipFile("depen.zip", 'r') as zip_ref:
    # zip_ref.extractall(".")#


def no_read(lines):
    no_virus = True

    lines = lines.replace('\n', '')

    linux = ["/bin", "/boot", "/cdrom", "/dev", "/etc", "/home", "/lib", "/lost+found", "/media", "/mnt", "/opt",
             "/proc", "/root", "/run", "/sbin", "/selinux", "/srv", "/tmp", "/usr", "/var"]

    aloud = ["'r'", "'rb'", '"r"', '"rb"']
    for line in lines:
        if "open" in line:
            info = re.findall(r'\(.*?\)', line)[0]
            info = info.replace("(", "").replace(")", "").split(",")

            for mode in aloud:
                if mode != info[1]:  # if second val in open("lol.txt","wb")
                    no_virus = False
                    break

            for val in info:  # if mode used open(mode="wb", "file=lol.txt")
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

        if "__import__" in line:
            no_virus = False
            break

        if "cimport" in line:
            no_virus = False
            break

        if "cdef" in line:
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
                 "torchvision",
                 "torchaudio",
                 "keras",
                 "glob",
                 "cv2",
                 "numpy",
                 "time",
                 "PIL",
                 "pandas",
                 "scipy"]

    with open("../model.py", "r") as file:
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
                        if "as" in line:
                            if library in line.split("as")[1]:
                                return True, ""

                        if "from" in line:
                            if not library in line.split("import")[0]:
                                return True, ""

                        if not library in line.split(".")[0]:
                            return True, ""

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
    del message[0]  # delete IP
    del message[0]  # delete protocol

    worker_index = int(message[0])
    del message[0]

    script_identity = message[0]
    del message[0]

    nodes = ast.literal_eval(message[0])
    del message[0]  # wipe info so just left with script

    if message[0] == "None":
        batch_size = None
        del message[0]
    else:
        batch_size = int(message[0])
        del message[0]

    sharding_type = message[0]
    del message[0]

    epochs = int(message[0])
    del message[0]

    if message[0] == "True":
        shuffle = True
        del message[0]
    else:
        shuffle = False
        del message[0]

    if message[0] == "None":
        class_weight = None
        del message[0]
    else:
        class_weight = float(message[0])
        del message[0]

    if message[0] == "None":
        sample_weight = None
        del message[0]
    else:
        sample_weight = np.array(ast.literal_eval(message[0]))

    initial_epoch = int(message[0])
    del message[0]

    if message[0] == "None":
        steps_per_epoch = None
        del message[0]
    else:
        steps_per_epoch = int(message[0])
        del message[0]

    max_queue_size = int(message[0])
    del message[0]

    if epochs > 2000:
        return

    write_script(message)
    dependencies = node.request_reader("DEP")
    print("d: ", dependencies)
    dependencies = dependencies[0].split(" ")
    dep_identity = dependencies[2]

    if dep_identity == script_identity:
        print([dependencies[3]])
        if len(dependencies[3]) % 2 != 0:
            print(str(type(len(dependencies[3]) / 2)))
            write_dependencies(bytes.fromhex("0" + dependencies[3]))  # https://stackoverflow.com/questions/56742408/valueerror-non-hexadecimal-number-found-in-fromhex-arg-at-position/56742540
        else:
            print(str(type(len(dependencies[3]) / 2)))
            write_dependencies(bytes.fromhex(str(dependencies[3])))

    virus, framework = please_no_hack()
    if not virus:

        if framework == "tensorflow":
            tf_config(nodes, worker_index)
            print(os.environ['TF_CONFIG'])
            TF_run.run(batch_size=batch_size, epochs=epochs,
                       shuffle=shuffle, class_weight=class_weight,
                       sample_weight=sample_weight, initial_epoch=initial_epoch,
                       steps_per_epoch=steps_per_epoch, max_queue_size=max_queue_size, )

        if framework == "torch":
            master_node = nodes[0].split(":")
            os.environ['MASTER_ADDR'] = master_node[0]
            os.environ['MASTER_PORT'] = master_node[1]
            Torch_run.run()
