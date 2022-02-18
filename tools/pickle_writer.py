import pickle

node = {"time": 1645188735.3090425, "ip": "192.168.68.112", "pub_key": "8655b6ac239324324d2ee22dc2358323180d3e4bb9ecb934e6623f9a", "port": 1379, "version": 1.0, "node_type": "Blockchain"}

with open("../Blockchain/info/Nodes.pickle", "wb") as file:
    pickle.dump([node], file)