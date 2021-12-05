import os
import socket
import random
import time

import requests
import json
import zipfile

def send(host, message):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, 1379))
        client.send(message.encode("utf-8"))
    except:
        return "node offline"




def upload(filename, depen_zip , AM_I = False): #am i a worker
    script_identity = str(random.random())
    with open(filename, "r") as file:
        script = file.readlines()

    with open(depen_zip, "rb") as file:
        zip_file = file.read()


    random_nodes = ["127.0.0.1"]   #requests.get() # get request for random node
    nodes = []
    my_ip = requests.get('https://api.ipify.org').text
    nodes.append(my_ip)
    for node in random_nodes:
        nodes.append(node)
    node_config = []
    node_config.append(my_ip + ":1379")

    if AM_I:
        worker_index = 1
        for node in random_nodes:
            send(node, "AI " + str(worker_index) + " " + script_identity + " " + str(nodes).replace(" ","")+ " " + script)
            send(node, "DEPEN " + script_identity + " " + zip_file.hex())
            node_config.append(node + ":1379" )

        tf_config = {
            "cluster" : {
                "worker" : node_config
            },
            "task": {"type": "worker", "index" : 0}
        }
        os.environ['TF_CONFIG'] = json.dumps(tf_config)


    if not AM_I:
        worker_index = 0
        for node in random_nodes:
            send(node, "AI " + str(worker_index) + " " + script_identity + " " + str(nodes).replace(" ","") +" " + str(script))
            time.sleep(0.5)
            send(node, "DEP " + script_identity + " " + zip_file.hex())
            node_config.append(node + ":1379")


if __name__ == "__main__":
    file= "./model.py"
    dependencies = "./text.zip"
    upload(file, dependencies)