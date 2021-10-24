"""
node 
"""

import socket
import numpy
import random
import pickle


#recieve from nodes
def receive():
    """ message is split into array the first value the type of messge
        the second value is the messgae"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 1379))
    server.listen()
    while True:
        client, address = server.accept()
        message = client.recv(2048).decode("utf-8").split(" ")
        try:
            print(client, " ", address)
            print("\n", message)
            return message, address
            break
        except:
            pass


#send to node
def send(host, message):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, 1379))
    client.send(message.encode("utf-8"))



#check if nodes online
def online(address):
    try:
        send(address,"ONLINE?")
    except:
        return False
    message,address = receive()
    if message == "yh":
        return True
    else:
        return False

def rand_act_node(num_nodes):
    nodes = []
    i = 1
    while i != num_nodes:
        with open("info/Nodes.pickle.pickle", "rb") as file:
            all_nodes = pickle.load(file)
        node_index = random.randint(len(all_nodes) - 1)
        node = all_nodes[node_index]
        alive = online(node[0])
        i += 1
        if alive:
            nodes.append(node)
        else:
            i -= 1

    if len(nodes) == 1:
        return nodes[0]
    else:
        return nodes


def file_reader(type):
    with open("recent_messages.txt", "r") as file:
        lines = file.read().splitlines()
        AI_protocols = ["OPT_REQ","DATA_REQ","ONLINE?", "GRAD"]
        AI_Lines = []
        NODE_Lines = []
        for line in lines:
            line = line.split(" ")
            try:
                if line[1] in AI_protocols:
                    AI_Lines.append(" ".join(line))
                else:
                    NODE_Lines.append(" ".join(line))
            except:
                pass
        if type == "AI":
            return AI_Lines
        if type == "NODE":
            return NODE_Lines


def ONE_D_message_compress(message):
    message = message.split(" ")
    del message[0]
    del message[0]
    return message

def TWO_D_message_compress(message):
    message = message.split(" ")
    for i in message:
        try:
            message.split(",")
        except:
            pass
    del message[0]
    del message[0]
    return message

def send_to_all(message):
    with open("info/Nodes.pickle.pickle", "rb") as file:
        all_nodes = pickle.load(file)
    for node in all_nodes:
        try:
            send(node[0], message)
        except:
            pass




#protocols to ask things
class send_protocols():
    def __init__(self):
        with open("info/Nodes.pickle.pickle", "rb") as file:
            self.nodes = pickle.load(file)

    def opt_req(self, data):
        node = rand_act_node(1)
        send(node[0], "OPT_REQ " + data)#redo all the string stuff


    def data_req(self,data):
        nodes = rand_act_node(5)
        for node in nodes:
            send(node[0], "DATA_REQ " + data)
        return nodes
    
    def announce(self, pub_key):
        send_to_all("HELLO "+ pub_key)


#protocols that receive things
class rec_protocols():
    def __init__(self):
        with open("info/Nodes.pickle.pickle", "rb") as file:
            self.nodes = pickle.load(file)
        with open("info/Blockchain.pickle", "rb") as file:
            self.blockchain = pickle.load(file)

    def get_node(self,host):
        send(host, self.nodes)

    def verify(self, host):
        send(host, self.blockchain)

    def transaction(self):
        pass

    def opt_inv(self, data): #if you get a opt request then send data invites to d_nodes and listen for gradients
        nodes = send_protocols.data_req(data)
        loss = 10
        while loss > 0.1:
            message = [None]
            while message[0] != "GRAD":
                message,address = receive()
                loss = message[1]
            newdata = None #<----insert optimizers line here
            for node in nodes:
                send(node[0], "DATA_REQ " + newdata)



    def dn_inv(self, data, host):#if data request run data then send
        gradient, loss = None #<--- run the model
        data = ["GRAD", str(loss)]
        for val in gradient:
            data.append(str(val))
        send(host, "GRAD " + " ".join(data))


    def new_node(self,new_node):
        self.node.append(new_node)
        with open("info/Nodes.pickle", "wb") as file:
            blockchain = pickle.load(file)



"""
def main(data):
    while True:
        message, address = receive()
        if message[0] == "GET_NODES":
            rec_protocols.get_node(address[0])

        elif message[0] == "VERIFY":
            rec_protocols.verify(address[0])

        elif message[0] == "ONLINE?":
            send(address[0], "yh")

        elif message[0] == "TRANS":
            pass

        elif message[0] == "OPT_REQ":
            rec_protocols.opt_inv(message[1])


        elif message[0] == "DATA_REQ":
            rec_protocols.dn_inv(message)

"""



            




if __name__ == "__main__":
    receive()
