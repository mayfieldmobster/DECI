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


# recieve from nodes
def receive(local_ip):
    """
    message is split into array the first value the type of message the second value is the message
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((local_ip, 1379))
    server.listen()
    while True:
        client, address = server.accept()
        message = client.recv(pow(2, 50)).decode("utf-8").split(" ")
        try:
            return message, address
            break
        except:
            pass


# send to node
def send(host, message, port=1379, all=False):
    """
    sends a message to the given host
    tries the default port and if it doesn't work search for actual port
    this process is skipped if send to all for speed
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
        client.send(message.encode("utf-8"))
        return
    except:
        pass  # bad practice will fix later
    if not all:
        try:
            with open("info/Nodes.pickle", "rb") as file:
                nodes = pickle.load(file)
            for node in nodes:
                if node[1] == host:
                    if not int(node["port"]) == 1379:
                        client.connect((host, int(node["port"])))
                        client.send(message.encode("utf-8"))
                        return
        except:
            return "node offline"


# check if nodes online
def online(address):
    """
    asks if a node is online and if it is it returns yh
    """
    try:
        send(address, "ONLINE?")
    except:
        return False
    message = request_reader("YH")
    if message == "yh":
        return True
    else:
        return False


def rand_act_node(num_nodes=1):
    """
    returns a list of random active nodes which is x length
    """
    nodes = []
    i = 0
    while i != num_nodes:  # turn into for loop
        with open("info/Nodes.pickle", "rb") as file:
            all_nodes = pickle.load(file)
        node_index = random.randint(len(all_nodes) - 1)
        node = all_nodes[node_index]
        alive = online(node["ip"])
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
    """
    reads the recent messages and returns the message of the requested type
    """
    with open("recent_messages.txt", "r") as file:
        lines = file.read().splitlines()
    NREQ_protocol = ["NREQ"]  # node request
    yh_protocol = ["yh"]
    Trans_protocol = ["TRANS"]
    BREQ_protocol = ["BREQ"]
    NODE_Lines = []
    NREQ_Lines = []
    yh_Lines = []
    Trans_Lines = []
    BREQ_Lines = []
    if str(lines) != "[]":
        for line in lines:
            line = line.split(" ")

            if line[0] == "":
                del line  # delete blank lines

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
                    if not Trans_Lines[0] in f_line:  # update to check multiple lines to lazy to do rn
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
                    if not BREQ_Lines[0] in f_line:  # update to check multiple lines to lazy to do rn
                        if not f_line.strip("\n") == "":
                            new_lines.append(f_line)
                open("recent_messages.txt", "w").close()
                with open("recent_messages.txt", "a") as file:
                    for n_line in new_lines:
                        file.write(n_line)
            return BREQ_Lines


def send_to_all(message):
    """
    sends to all nodes
    """
    with open("../info/Nodes.pickle", "rb") as file:
        all_nodes = pickle.load(file)
    for node in all_nodes:
        try:
            send(node[1], message, port=node[3], all=True)
        except:
            pass  # node is offline


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
    send(node["ip"], "GET_NODES")
    while True:
        time.sleep(1)
        line = request_reader("NREQ")
        line = line.split(" ")
        nodes = line[2]
        nodes = ast.literal_eval(nodes)
        with open("../info/Nodes.pickle", "wb") as file:
            pickle.dump(nodes, file)


def get_blockchain():  # send ask the website for blockchain as most up todate
    node = rand_act_node()
    send(node["ip"], "BLOCKCHAIN?")
    while True:
        lines = request_reader("BREQ")
        if lines:
            for line in lines:
                line = line.split(" ")
                if line[0] == node["ip"]:
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
        new_node = {"time": float(time), "ip": ip, "pub_key": pub_key, "port": int(port), "version": float(version),
                    "node_type": node_type}
        for node in nodes:
            if node["pub_key"] == pub_key:
                return
            if node["ip"] == ip:
                return
        nodes.append(new_node)
        with open("info/Nodes.pickle", "wb") as file:
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
            if node["ip"] == ip:
                node["pub_key"] = pub_key
                node["port"] = port
                node["version"] = version
        with open("info/Nodes.pickle", "wb") as file:
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
            if node["ip"] == ip and node["pub_key"] == pub_key:
                del node
        with open("info/Nodes.pickle", "wb") as file:
            pickle.dump(nodes, file)
    except:
        return "cancel invalid"


def version():
    send_to_all(f"VERSION {__version__}")


def version_update(ip, ver):
    with open("./info/Nodes.pickle", "rb") as file:
        nodes = pickle.load(file)
    for nod in nodes:
        if nod["ip"] == ip:
            nod["version"] = ver
            break


class NodeError(Exception):
    pass


class UnrecognisedCommand(NodeError):
    pass


class ValueTypeError(NodeError):
    pass


class UnrecognisedArg(NodeError):
    pass


def error_handler(message):
    try:
        protocol = message[1]
    except:
        raise UnrecognisedArg("No Protocol Found")

    if protocol == "GET_NODES":
        # host, GET_NODES
        if len(message) != 2:
            raise UnrecognisedArg("number of args given incorrect")

    elif protocol == "HELLO":
        # host, HELLO, announcement_time, public key, port, version, node type, sig
        if len(message) != 8:
            raise UnrecognisedArg("number of args given incorrect")

        try:
            float(message[2])
            if "." not in message[2]:
                Exception()
        except:
            raise ValueTypeError("time not given as float")

        if len(message[3]) != 56:
            raise UnrecognisedArg("Public Key is the wrong size")

        try:
            port = int(message[4])
        except:
            raise ValueTypeError("port not given as int")

        if port >= 0 and port < 65535:
            raise ValueTypeError("TCP port out of range")

        try:
            float(message[5])
            if "." not in message[5]:
                Exception()
        except:
            raise ValueTypeError("version not given as float")

        if message[6] != "Lite" or "AI" or "Blockchain":
            raise UnrecognisedArg("Node Type Unknown")

    elif protocol == "VALID":
        # host, VALID , block index, time of validation
        if len(message) != 4:
            raise UnrecognisedArg("number of args given incorrect")

        try:
            int(message[2])
        except:
            raise ValueTypeError("Block Index not given as int")

        try:
            float(message[3])
            if "." not in message[3]:
                Exception()
        except:
            raise ValueTypeError("time not given as float")

    elif protocol == "TRANS_INVALID":
        # host, TRANS_INVALID, Block Index, Transaction invalid
        if len(message) != 4:
            raise UnrecognisedArg("number of args given incorrect")

        try:
            int(message[2])
        except:
            raise ValueTypeError("Block Index not given as int")

        try:
            int(message[3])
        except:
            raise ValueTypeError("Transaction Index not given as int")

    elif protocol == "ONLINE?":
        # host, ONLINE?
        if len(message) != 2:
            raise UnrecognisedArg("number of args given incorrect")

    elif protocol == "BLOCKCHAIN?":
        # host, BLOCKCHAIN?
        if len(message) != 2:
            raise UnrecognisedArg("number of args given incorrect")

    elif protocol == "UPDATE":
        # host, UPDATE, update time, public key, port, version, sig
        if len(message) != 7:
            raise UnrecognisedArg("number of args given incorrect")

        try:
            float(message[2])
            if "." not in message[2]:
                Exception()
        except:
            raise ValueTypeError("time not given as float")

        if len(message[3]) != 56:
            raise UnrecognisedArg("Public Key is the wrong size")

        try:
            port = int(message[4])
        except:
            raise ValueTypeError("port not given as int")

        if port >= 0 and port < 65535:
            raise ValueTypeError("TCP port out of range")

        try:
            float(message[5])
            if "." not in message[5]:
                Exception()
        except:
            raise ValueTypeError("version not given as float")

    elif protocol == "DELETE":
        # host, DELETE, public key, sig
        if len(message) != 4:
            raise UnrecognisedArg("number of args given incorrect")

        if len(message[2]) != 56:
            raise UnrecognisedArg("Public Key is the wrong size")

    elif protocol == "BREQ":
        # host, BREQ, Blockchain
        try:
            ast.literal_eval(message[2])
        except:
            raise ValueTypeError("Blockchain not given as Blockchain")

    elif protocol == "NREQ":
        # host, NREQ, Nodes
        try:
            ast.literal_eval(message[2])
        except:
            raise ValueTypeError("Blockchain not given as Node List")

    elif protocol == "TRANS":
        # host, TRANS, time of transaction, sender public key, receiver public key, amount sent, sig
        if len(message) != 7:
            raise UnrecognisedArg("number of args given incorrect")

        try:
            float(message[2])
            if "." not in message[2]:
                Exception()
        except:
            raise ValueTypeError("time not given as float")

        if len(message[3]) != 56:
            raise UnrecognisedArg("Senders Public Key is the wrong size")

        if len(message[4]) != 56:
            raise UnrecognisedArg("Receivers Public Key is the wrong size")

        try:
            float(message[5])
            if "." not in message[5]:
                Exception()
        except:
            raise ValueTypeError("amount not given as float")

    else:
        raise UnrecognisedCommand("protocol unrecognised")
