import AI
import node
import pickle
import time
import random

def distributor(epochs, data_size, num_params, script):
    total_size = data_size*epochs
    with open("./info/Nodes.pickle", "rb") as file:
        nodes = pickle.load(file) #node atributes: time_init, IP, pub_key, num_gpus, benchmark_epoch_per_second
    node.send_to_all("ONLINE?")
    time.sleep(5)
    online_lines = node.request_reader("YH")
    available_nodes = []
    for line in online_lines:
        line = line.split(" ")
        for AI_node in nodes:
            if line[0] == AI_node["ip"]:
                available_nodes.append(AI_node)
                continue
    weights = []
    for av_node in available_nodes:
        weights.append(-av_node["benchmark"])
    if len(available_nodes) >=10:
        k=10
    else:
        k=len(available_nodes) 
    #this is a bad way of picking nodes design a dynamic method later 
    job_nodes = random.choices(available_nodes), weights=weights, k=k)
    node.request_reader("DEP")
    dep = node.request_reader("DEP")#add method to not get wrong dep
    dep = dep.split(" ")
    for job_node in job_nodes:
        node.send(job_node["ip"], f"AI {job_nodes} {script}")
        node.send(job_node["ip"], f"DEP {dep[2]}")

