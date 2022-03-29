import pickle

node1 = {"time": 1645188735.3090425, "ip": "192.168.68.140", "pub_key": "c917f27bfb852e6667036c9f44767a226d4f8105ad3c9ea09370f8d0", "port": 1379, "version": 1.0, "node_type": "Blockchain"}
node2 = {"time": 1645188735.3090446, "ip": "192.168.68.145", "pub_key": "0b3553c4f5d86f76ef1b686b953bce9f69922c8c1141fb9b1a5c892f", "port": 1379, "version": 1.0, "node_type": "Blockchain"}
node3 = {"time": 1645188735.3090457, "ip": "192.168.68.112", "pub_key": "93419305da43adb7b91b6d4f0526ccda8130a9385b9c6b2acf7f38a1", "port": 1379, "version": 1.0, "node_type": "Blockchain"}

with open("../Blockchain/info/Nodes.pickle", "wb") as file:
    pickle.dump([node1, node2], file)