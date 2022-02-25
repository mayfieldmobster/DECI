import pickle

node = {"time": 1645188735.3090425, "ip": "192.168.68.140", "pub_key": "c917f27bfb852e6667036c9f44767a226d4f8105ad3c9ea09370f8d0", "port": 1379, "version": 1.0, "node_type": "Blockchain"}
node2 = {"time": 1645188735.3090446, "ip": "192.168.0.33", "pub_key": "0b3553c4f5d86f76ef1b686b953bce9f69922c8c1141fb9b1a5c892f", "port": 1379, "version": 1.0, "node_type": "Blockchain"}

with open("../Blockchain/info/Nodes.pickle", "wb") as file:
    pickle.dump([node, node2], file)