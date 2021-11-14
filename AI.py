import zipfile
import ast

def write_script(string):
    script = " ".join(string)
    with open("main.py", "w") as file:
        file.write(script)
    return script

def write_dependencies(string):
    with open("depen.zip","wb") as file:
        file.write(string)

    with zipfile.ZipFile("depen.zip", 'r') as zip_ref:
        zip_ref.extractall(".")

def AI_REQ(message):
    del message[0]#delete IP
    del message[0]#delete protocol
    worker_index = message[0]
    del message[0]
    script_identity = message[0]
    del message[0]
    nodes = ast.literal_eval(message[0])
    del message[0]
    script = " ".join(message)
    write_script(script)

