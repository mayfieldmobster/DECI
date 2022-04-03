import AI
import node
import pickle
import time

def distributor(epochs, data_size, num_params):
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
    




    pass
