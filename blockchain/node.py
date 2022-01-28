"""
node
"""

import socket
import random
import pickle
import time
import ast
import blockchain
import time
from ecdsa import SigningKey, VerifyingKey, SECP112r2

__version__ = "1.0"

#recieve from nodes
def receive(local_ip):
    """ message is split into array the first value the type of messge
        the second value is the messgae"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((local_ip,1379))
    server.listen()
    while True:
        client, address = server.accept()
        message = client.recv(pow(2,50)).decode("utf-8").split(" ")
        try:
            return message, address
            break
        except:
            pass


#send to node
def send(host,message):
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
    message = request_reader("YH")
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
    NREQ_protocol = ["NREQ"]#node request
    yh_protocol = ["yh"]
    Trans_protocol = ["TRANS"]
    BREQ_protocol = ["BLOCKCHAIN?"]
    NODE_Lines = []
    NREQ_Lines = []
    yh_Lines = []
    Trans_Lines = []
    BREQ_Lines = []
    if str(lines) != "[]":
        for line in lines:
            line = line.split(" ")

            if line[0] == "":
                del line # delete blank lines

            elif line[1] in NREQ_protocol:
                NREQ_Lines.append(" ".join(line))

            elif line[1] in yh_protocol:
                yh_Lines.append(" ".join(line))

            elif line[1] in Trans_protocol:
                Trans_Lines.append(" ".join(line))

            elif line[1] in BREQ_protocol:
                Trans_Lines.append(" ".join(line))

            else:
                NODE_Lines.append(" ".join(line))


        if type == "YH":
            if len(yh_Lines) != 0:
                new_lines = []
                with open("recent_messages.txt", "r") as file:
                    file_lines = file.readlines()
                for f_line in file_lines:
                    f_line.split(" ")
                    if not yh_Lines[0] in f_line:
                        if not f_line.strip("\n") == "":
                            new_lines.append(f_line)
                open("recent_messages.txt", "w").close()
                with open("recent_messages.txt", "a") as file:
                    for n_line in new_lines:
                        file.write(n_line)
            return yh_Lines

        elif type == "NODE":
            if len(NODE_Lines) != 0:
                new_lines = []
                with open("recent_messages.txt", "r") as file:
                    file_lines = file.readlines()
                for f_line in file_lines:
                    f_line.split(" ")
                    if not NODE_Lines[0] in f_line:
                        if not f_line.strip("\n") == "":
                            new_lines.append(f_line)
                open("recent_messages.txt", "w").close()
                with open("recent_messages.txt", "a") as file:
                    for n_line in new_lines:
                        file.write(n_line)
            return NODE_Lines

        elif type == "NREQ":
            if len(NREQ_Lines) != 0:
                new_lines = []
                with open("recent_messages.txt", "r+") as file:
                    file_lines = file.readlines()
                for f_line in file_lines:
                    f_line.split(" ")
                    if not NREQ_Lines[0] in f_line:
                        if not f_line.strip("\n") == "":
                            new_lines.append(f_line)
                open("recent_messages.txt", "w").close()
                with open("recent_messages.txt", "a") as file:
                    for n_line in new_lines:
                        file.write(n_line)
            return NREQ_Lines

        elif type == "TRANS":
            if len(Trans_Lines) != 0:
                new_lines = []
                with open("recent_messages.txt", "r") as file:
                    file_lines = file.readlines()
                for f_line in file_lines:
                    if not Trans_Lines[0] in f_line:#update to check multiple lines to lazy to do rn
                        if not f_line.strip("\n") == "":
                            new_lines.append(f_line)
                open("recent_messages.txt", "w").close()
                with open("recent_messages.txt", "a") as file:
                    for n_line in new_lines:
                        file.write(n_line)
            return Trans_Lines

        elif type == "BREQ":
            if len(BREQ_Lines) != 0:
                new_lines = []
                with open("recent_messages.txt", "r") as file:
                    file_lines = file.readlines()
                for f_line in file_lines:
                    if not BREQ_Lines[0] in f_line:#update to check multiple lines to lazy to do rn
                        if not f_line.strip("\n") == "":
                            new_lines.append(f_line)
                open("recent_messages.txt", "w").close()
                with open("recent_messages.txt", "a") as file:
                    for n_line in new_lines:
                        file.write(n_line)
            return BREQ_Lines


def send_to_all(message):
    with open("../info/Nodes.pickle", "rb") as file:
        all_nodes = pickle.load(file)
    for node in all_nodes:
        try:
            send(node[1], message)
        except:
            pass #node is offline

    
def announce(pub_key, port, version, node_type, priv_key):
    announcement_time = str(time.time())
    if not isinstance(priv_key, bytes):
        priv_key = SigningKey.from_string(bytes.formathex(priv_key), curve=SECP112r2)
    sig = priv_key.sign(announcement_time.encode("utf-8"))
    send_to_all(f"HELLO {announcement_time} {pub_key} {str(port)} {version} {node_type} {sig}")

def update(pub_key, port, version, priv_key):
    update_time = str(time.time())
    if not isinstance(priv_key, bytes):
        priv_key = SigningKey.from_string(bytes.formathex(priv_key), curve=SECP112r2)
    sig = priv_key.sign(update_time.encode("utf-8"))
    send_to_all(f"UPDATE {update_time} {pub_key} {str(port)} {version} {sig}")

def delete(pub_key, priv_key):
    update_time = str(time.time())
    if not isinstance(priv_key, bytes):
        priv_key = SigningKey.from_string(bytes.formathex(priv_key), curve=SECP112r2)
    sig = priv_key.sign(update_time.encode("utf-8"))
    send_to_all(f"DELETE {update_time} {pub_key} {sig}")

def get_nodes():
    node = rand_act_node()
    send(node[1],"GET_NODES")
    while True:
        time.sleep(1)
        line = request_reader("NREQ")
        line = line.split(" ")
        nodes = line[2]
        nodes = ast.literal_eval(nodes)
        with open("../info/Nodes.pickle", "wb") as file:
            pickle.dump(nodes, file)

def get_blockchain():#send ask the website for blockchain as most up todate
    node = rand_act_node()
    send(node[1], "BLOCKCHAIN?")
    while True:
        lines = request_reader("BREQ")
        if lines:
            for line in lines:
                line = line.split(" ")
                if line[0] == node[1]:
                    chain = ast.literal_eval(line[1])
                    blockchain.write_blockchain(chain)
                    return

def send_node(host):
    with open("../info/Nodes.pickle", "rb") as file:
        Nodes = pickle.load(file)
    str_node = str(Nodes)
    str_node = str_node.replace(" ", "")
    send(host, "NREQ " + str_node)


def new_node(time, ip, pub_key, port, version, node_type, sig):
    with open("info/Nodes.pickle", "rb") as file:
        nodes = pickle.load(file)
    public_key = VerifyingKey.from_string(bytes.formathex(pub_key), curve=SECP112r2)
    try:
        assert public_key.verify(bytes.fromhex(sig), time.encode())
        new_node = [time, ip, pub_key, port, version, node_type]
        for node in nodes:
            if node[2] == pub_key:
                return
            if node[1] == ip:
                return
        nodes.append(new_node)
        with open("info/Nodes.pickle","wb") as file:
            pickle.dump(nodes, file)
    except:
        return "node invalid"

def update_node(ip, update_time, pub_key, port, version, sig):
    with open("info/Nodes.pickle", "rb") as file:
        nodes = pickle.load(file)
    public_key = VerifyingKey.from_string(bytes.formathex(pub_key), curve=SECP112r2)
    try:
        assert public_key.verify(bytes.fromhex(sig), update_time.encode())
        for node in nodes:
            if node[1] == ip:
                node[2] = pub_key
                node[3] = port
                node[4] = version
        with open("info/Nodes.pickle","wb") as file:
            pickle.dump(nodes, file)
    except:
        return "update invalid"

def delete_node(time, ip, pub_key, sig):
    with open("info/Nodes.pickle", "rb") as file:
        nodes = pickle.load(file)
    public_key = VerifyingKey.from_string(bytes.formathex(pub_key), curve=SECP112r2)
    try:
        assert public_key.verify(bytes.fromhex(sig), time.encode())
        for node in nodes:
            if node[1] == ip and node[2] == pub_key:
                del node
        with open("info/Nodes.pickle", "wb") as file:
            pickle.dump(nodes, file)
    except:
        return "cancel invalid"


def version(ver):
    send_to_all(f"VERSION {ver}")

def version_update(ip, ver):
    with open("./info/Nodes.pickle", "rb") as file:
        nodes = pickle.load(file)
    for nod in nodes:
        if nod[1] == ip:
            nod[4] = ver
            break


if __name__ == "__main__":
    receive()
