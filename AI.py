import zipfile
import ast
import node
import os
import json
import AI_run


def write_script(string):
    open("model.py", "w").close()
    script = " ".join(string)
    print(type(script))
    script = ast.literal_eval(script)
    with open("model.py", "w") as file:
        for line in script:
            file.write(line)
    return script

def write_dependencies(string):
    with open("text.zip","wb") as file:
        file.write(string)

    #with zipfile.ZipFile("depen.zip", 'r') as zip_ref:
        #zip_ref.extractall(".")
        
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
    worker_index = message[0]
    del message[0]
    script_identity = message[0]
    del message[0]
    nodes = ast.literal_eval(message[0])
    del message[0]
    write_script(message)
    while True:
        dependencies = node.request_reader("DEP")
        dependencies = dependencies.split(" ")
        try:
            dep_identity = dependencies[2]
            print("TRUE")
            if dep_identity == script_identity:
                write_dependencies(dependencies[3])
                break
        except Exception as e:
            print(e)

    tf_config(nodes,worker_index)
    print(os.environ['TF_CONFIG'])
    #AI_run.run(64)
    



