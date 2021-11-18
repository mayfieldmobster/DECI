"""
node 
"""

import socket
import random
import pickle
import time
import ast
import concurrent.futures


#recieve from nodes
def receive(local_ip):
    """ message is split into array the first value the type of messge
        the second value is the messgae"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((local_ip, 1379))
    server.listen()
    while True:
        client, address = server.accept()
        message = client.recv(2048).decode("utf-8").split(" ")
        try:
            return message, address
            break
        except:
            pass


#send to node
def send(host, message):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, 1379))
        client.send(message.encode("utf-8"))
    except:
        return "node offline"



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

def rand_act_node(num_nodes = 1):
    nodes = []
    i = 0
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


def request_reader(type):
    with open("recent_messages.txt", "r") as file:
        lines = file.read().splitlines()
        print(lines)
        AI_protocols = ["AI"]
        NREQ_protocol = ["NEW_NODES"]#node request
        DEP_protocol = ["DEP"]
        AI_Lines = []
        NODE_Lines = []
        NREQ_Lines = []
        DEP_Lines = []
        if str(lines) != "[]":
            print("success")
            for line in lines:
                line = line.split(" ")

                if line[0] == "":
                    del line # delete blank lines

                elif line[1] in AI_protocols:
                    AI_Lines.append(" ".join(line))

                elif line[1] in NREQ_protocol:
                    NREQ_Lines.append(" ".join(line))

                elif line[1] in DEP_protocol:
                    DEP_Lines.append(" ".join(line))

                else:
                    NODE_Lines.append(" ".join(line))


        if type == "AI":
            new_lines = []
            with open("recent_messages.txt", "r") as file:
                file_lines = file.readlines()
                for f_line in file_lines:
                    f_line.split(" ")
                    if not f_line in AI_Lines:
                        new_lines.append(" ".join(f_line))
            open("recent_messages.txt", "w").close()
            with open("recent_messages.txt", "a") as file:
                for n_line in new_lines:
                    file.write(n_line)
            return AI_Lines

        if type == "NODE":
            new_lines = []
            with open("recent_messages.txt", "r") as file:
                file_lines = file.readlines()
                for f_line in file_lines:
                    f_line.split(" ")
                    if not f_line in NODE_Lines:
                        new_lines.append(" ".join(f_line))
            open("recent_messages.txt", "w").close()
            with open("recent_messages.txt", "a") as file:
                for n_line in new_lines:
                    file.write(n_line)

            return NODE_Lines

        if type == "NREQ":
            new_lines = []
            with open("recent_messages.txt", "r") as file:
                file_lines = file.readlines()
                for f_line in file_lines:
                    f_line.split(" ")
                    if not f_line in NREQ_Lines:
                        new_lines.append(" ".join(f_line))
            open("recent_messages.txt", "w").close()
            with open("recent_messages.txt", "a") as file:
                for n_line in new_lines:
                    file.write(n_line)
            return NREQ_Lines[0]

        if type == "DEP":
            new_lines = []
            with open("recent_messages.txt", "r") as file:
                file_lines = file.readlines()
                for f_line in file_lines:
                    f_line.split(" ")
                    if not f_line in DEP_Lines:
                        new_lines.append(" ".join(f_line))
            open("recent_messages.txt", "w").close()
            with open("recent_messages.txt", "a") as file:
                for n_line in new_lines:
                    file.write(n_line)
            return DEP_Lines[0]





def send_to_all(message):
    with open("info/Nodes.pickle", "rb") as file:
        all_nodes = pickle.load(file)
    for node in all_nodes:
        try:
            send(node[1], message)
        except:
            pass #node is offline





def opt_req(self, data):
    node = rand_act_node(1)
    send(node[0], "OPT_REQ " + data)#redo all the string stuff


def data_req(self,data):
    nodes = rand_act_node(5)
    for node in nodes:
        send(node[0], "DATA_REQ " + data)
    return nodes
    
def announce(self, pub_key):
    send_to_all("HELLO "+ str(time.time()) + " " + pub_key)

def get_nodes(self):
    node = rand_act_node()
    send(node[1],"GET_NODES")
    while True:
        time.sleep(1)
        line = request_reader("NREQ")
        line = line.split(" ")
        nodes = line[2]
        nodes = ast.literal_eval(nodes)
        with open("./info/Nodes.pickle", "wb") as file:
            pickle.dump(nodes, file)



def get_blockchain(self):#send ask the website for blockchain as most up todate
    pass #send get request to website



def send_node(host):
    with open("info/Nodes.pickle", "rb") as file:
        Nodes = pickle.load(file)
    str_node = str(Nodes)
    str_node = str_node.replace(" ", "")
    send(host, "NREQ " + str_node)


def new_node(time, new_node, address):
    with open("info/Nodes.pickle", "rb") as file:
        Nodes = pickle.load(file)
    new_node = [time, new_node, address]
    Nodes.append(new_node)
    with open("info/Nodes.pickle","wb") as file:
        pickle.dump(Nodes, file)



def receiver():
    while True:
        message, address = receive()

        file = open("recent_messages.txt", "a")

        file.write("\n" + address[0] + " " + " ".join(message))
        file.close()



            




if __name__ == "__main__":
    receive()
