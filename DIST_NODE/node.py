"""
node
"""

import socket
import random
import pickle
import time
import ast
import time
from ecdsa import SigningKey, VerifyingKey, SECP112r2
import asyncio

__version__ = "1.0"


# recieve from nodes
def receive(local_ip):
    """
    message is split into array the first value the type of message the second value is the message
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((local_ip, 1379))
    server.listen()
    while True:
        try:
            client, address = server.accept()
            message = client.recv(2048).decode("utf-8").split(" ")
            server.close()
            return message, address
        except Exception as e:
            print(e)


# send to node
def send(host, message, port=1379, send_all=False):
    """
    sends a message to the given host
    tries the default port and if it doesn't work search for actual port
    this process is skipped if send to all for speed
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
        client.send(message.encode("utf-8"))
        print(f"Message to {host} {message}\n")
        return
    except Exception as e:
        if not send_all:
            if isinstance(e, ConnectionRefusedError):
                try:
                    with open("info/Nodes.pickle", "rb") as file:
                        nodes = pickle.load(file)
                    for node in nodes:
                        if node[1] == host:
                            if not int(node["port"]) == 1379:
                                client.connect((host, int(node["port"])))
                                client.send(message.encode("utf-8"))
                                print(f"Message to {host} {message}\n")
                                return
                except Exception as e:
                    return "node offline"

async def async_send(host, message, port=1379, send_all=False):
    """
    sends a message to the given host
    tries the default port and if it doesn't work search for actual port
    this process is skipped if send to all for speed
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
        client.send(message.encode("utf-8"))
        print(f"Message to {host} {message}\n")
        return
    except Exception as e:
        if not send_all:
            if isinstance(e, ConnectionRefusedError):
                try:
                    with open("info/Nodes.pickle", "rb") as file:
                        nodes = pickle.load(file)
                    for node in nodes:
                        if node[1] == host:
                            if not int(node["port"]) == 1379:
                                client.connect((host, int(node["port"])))
                                client.send(message.encode("utf-8"))
                                print(f"Message to {host} {message}\n")
                                return
                except Exception as e:
                    return "node offline"

# check if nodes online
def online(address):
    """
    asks if a node is online and if it is it returns yh
    """
    print(address)
    socket.setdefaulttimeout(1.0)
    try:
        send(address, "ONLINE?")
    except:
        socket.setdefaulttimeout(3.0)
        return False
    socket.setdefaulttimeout(3.0)
    time.sleep(5)
    message = request_reader("YH", ip=address)
    if message:
        message = message[0].split(" ")
        if message[1] == "yh":
            return True
    else:
        return False


def rand_act_node(num_nodes=1):
    """
    returns a list of random active nodes which is x length
    """
    with open("./info/Public_key.txt", "r") as file:
        key = file.read()
    nodes = []
    i = 0
    while i != num_nodes:  # turn into for loop
        with open("info/Nodes.pickle", "rb") as file:
            all_nodes = pickle.load(file)
        node_index = random.randint(0, len(all_nodes) - 1)
        node = all_nodes[node_index]
        print(node)
        if node["pub_key"] == key:
            continue
        alive = online(node["ip"])
        if alive:
            nodes.append(node)
            i += 1

    if len(nodes) == 1:
        return nodes[0]
    else:
        return nodes


def request_reader(type, ip="192.168.68.1"):
    """
    reads the recent messages and returns the message of the requested type
    """
    with open("recent_messages.txt", "r") as file:
        lines = file.read().splitlines()
    nreq_protocol = ["NREQ"]  # node request
    yh_protocol = ["yh"]
    trans_protocol = ["TRANS"]
    breq_protocol = ["BREQ"]
    pre_protocol = ["ONLINE?", "GET_NODES", "BLOCKCHAIN?"]
    node_lines = []
    nreq_lines = []
    yh_lines = []
    trans_lines = []
    breq_lines = []
    online_lines = []
    if str(lines) != "[]":
        for line in lines:
            line = line.split(" ")

            if line[0] == "" or line[0] == "\n":
                del line  # delete blank lines

            elif line[1] in nreq_protocol:
                nreq_lines.append(" ".join(line))

            elif line[1] in yh_protocol and line[0] == ip:
                yh_lines.append(" ".join(line))

            elif line[1] in trans_protocol:
                trans_lines.append(" ".join(line))

            elif line[1] in pre_protocol:
                online_lines.append(" ".join(line))

            elif line[1] in breq_protocol:
                breq_lines.append(" ".join(line))

            else:
                node_lines.append(" ".join(line))

        if type == "YH":
            if len(yh_lines) != 0:
                new_lines = []
                with open("recent_messages.txt", "r") as file:
                    file_lines = file.readlines()
                for f_line in file_lines:
                    f_line.split(" ")
                    if not yh_lines[0] in f_line:
                        if not f_line.strip("\n") == "":
                            new_lines.append(f_line)
                open("recent_messages.txt", "w").close()
                with open("recent_messages.txt", "a") as file:
                    for n_line in new_lines:
                        file.write(n_line)
            return yh_lines

        elif type == "NODE":
            if len(node_lines) != 0:
                new_lines = []
                with open("recent_messages.txt", "r") as file:
                    file_lines = file.readlines()
                for f_line in file_lines:
                    f_line.split(" ")
                    if not node_lines[0] in f_line:
                        if not f_line.strip("\n") == "":
                            new_lines.append(f_line)
                open("recent_messages.txt", "w").close()
                with open("recent_messages.txt", "a") as file:
                    for n_line in new_lines:
                        file.write(n_line)
            return node_lines

        elif type == "NREQ":
            if len(nreq_lines) != 0:
                new_lines = []
                with open("recent_messages.txt", "r+") as file:
                    file_lines = file.readlines()
                for f_line in file_lines:
                    f_line.split(" ")
                    if not nreq_lines[0] in f_line:
                        if not f_line.strip("\n") == "":
                            new_lines.append(f_line)
                open("recent_messages.txt", "w").close()
                with open("recent_messages.txt", "a") as file:
                    for n_line in new_lines:
                        file.write(n_line)
            return nreq_lines

        elif type == "ONLINE":
            if len(online_lines) != 0:
                new_lines = []
                with open("recent_messages.txt", "r+") as file:
                    file_lines = file.readlines()
                for f_line in file_lines:
                    f_line.split(" ")
                    if not online_lines[0] in f_line:
                        if not f_line.strip("\n") == "":
                            new_lines.append(f_line)
                open("recent_messages.txt", "w").close()
                with open("recent_messages.txt", "a") as file:
                    for n_line in new_lines:
                        file.write(n_line)
            return online_lines

        elif type == "TRANS":
            if len(trans_lines) != 0:
                new_lines = []
                with open("recent_messages.txt", "r") as file:
                    file_lines = file.readlines()
                for f_line in file_lines:
                    if not trans_lines[0] in f_line:  # update to check multiple lines to lazy to do rn
                        if not f_line.strip("\n") == "":
                            new_lines.append(f_line)
                open("recent_messages.txt", "w").close()
                with open("recent_messages.txt", "a") as file:
                    for n_line in new_lines:
                        file.write(n_line)
            return trans_lines

        elif type == "BREQ":
            if len(breq_lines) != 0:
                new_lines = []
                with open("recent_messages.txt", "r") as file:
                    file_lines = file.readlines()
                for f_line in file_lines:
                    if not breq_lines[0] in f_line:  # update to check multiple lines to lazy to do rn
                        if not f_line.strip("\n") == "":
                            new_lines.append(f_line)
                open("recent_messages.txt", "w").close()
                with open("recent_messages.txt", "a") as file:
                    for n_line in new_lines:
                        file.write(n_line)
            return breq_lines


async def send_to_all(message):
    """
    sends to all nodes
    """
    with open("./info/Nodes.pickle", "rb") as file:
        all_nodes = pickle.load(file)
    for f in asyncio.as_completed([async_send(node_["ip"], message, port=node_["port"], send_all=True) for node_ in all_nodes]):
        result = await f

async def send_to_all_no_dist(message):
    """
    sends to all nodes
    """
    with open("./info/Nodes.pickle", "rb") as file:
        all_nodes = pickle.load(file)
    for f in asyncio.as_completed([async_send(node_["ip"], message, port=node_["port"], send_all=True) for node_ in all_nodes if node_["type"] != "dist"]):
        result = await f


def announce(pub_key, port, version, node_type, priv_key):
    announcement_time = str(time.time())
    if not isinstance(priv_key, bytes):
        priv_key = SigningKey.from_string(bytes.fromhex(priv_key), curve=SECP112r2)
    sig = str(priv_key.sign(announcement_time.encode()).hex())
    asyncio.run(send_to_all(f"HELLO {announcement_time} {pub_key} {str(port)} {version} {node_type} {sig.hex()}"))


def update(pub_key, port, version, priv_key):
    update_time = str(time.time())
    if not isinstance(priv_key, bytes):
        priv_key = SigningKey.from_string(bytes.fromhex(priv_key), curve=SECP112r2)
    sig = str(priv_key.sign(update_time.encode()).hex())
    asyncio.run(send_to_all(f"UPDATE {update_time} {pub_key} {str(port)} {version} {sig}"))


def delete(pub_key, priv_key):
    update_time = str(time.time())
    if not isinstance(priv_key, bytes):
        priv_key = SigningKey.from_string(bytes.fromhex(priv_key), curve=SECP112r2)
    sig = str(priv_key.sign(update_time.encode()).hex())
    asyncio.run(send_to_all(f"DELETE {update_time} {pub_key} {sig}"))


def get_nodes():
    print("---GETTING NODES---")
    node = rand_act_node()
    send(node["ip"], "GET_NODES")
    tries = 0
    while True:
        if tries == 10:
            quit()
        time.sleep(5)
        line = request_reader("NREQ")
        if line:
            line = line[0].split(" ")
            nodes = line[2]
            nodes = ast.literal_eval(nodes)
            if line[0] == node["ip"]:
                with open("../info/Nodes.pickle", "wb") as file:
                    pickle.dump(nodes, file)
                print("---NODES RECEIVED---")
                return
        else:
            tries += 1
            continue





def send_node(host):
    with open("./info/Nodes.pickle", "rb") as file:
        Nodes = pickle.load(file)
    str_node = str(Nodes)
    str_node = str_node.replace(" ", "")
    send(host, "NREQ " + str_node)


def new_node(initiation_time, ip, pub_key, port, node_version, node_type, sig):
    with open("info/Nodes.pickle", "rb") as file:
        nodes = pickle.load(file)
    public_key = VerifyingKey.from_string(bytes.fromhex(pub_key), curve=SECP112r2)
    try:
        assert public_key.verify(bytes.fromhex(sig), str(initiation_time).encode())
        new_node = {"time": initiation_time, "ip": ip, "pub_key": pub_key, "port": port, "version": node_version,
                    "node_type": node_type}
        for node in nodes:
            if node["pub_key"] == pub_key:
                return
            if node["ip"] == ip:
                return
        nodes.append(new_node)
        with open("info/Nodes.pickle", "wb") as file:
            pickle.dump(nodes, file)
    except Exception as e:
        print(e)
        return "node invalid"


def update_node(ip, update_time, pub_key, port, node_version, sig):
    with open("info/Nodes.pickle", "rb") as file:
        nodes = pickle.load(file)
    public_key = VerifyingKey.from_string(bytes.fromhex(pub_key), curve=SECP112r2)
    try:
        assert public_key.verify(bytes.fromhex(sig), str(update_time).encode())
        for node in nodes:
            if node["ip"] == ip:
                node["pub_key"] = pub_key
                node["port"] = port
                node["version"] = node_version
        with open("info/Nodes.pickle", "wb") as file:
            pickle.dump(nodes, file)
            print("NODE UPDATED")
    except:
        return "update invalid"


def delete_node(deletion_time, ip, pub_key, sig):
    with open("info/Nodes.pickle", "rb") as file:
        nodes = pickle.load(file)
    public_key = VerifyingKey.from_string(bytes.fromhex(pub_key), curve=SECP112r2)
    try:
        assert public_key.verify(bytes.fromhex(sig), str(deletion_time).encode())
        for node in nodes:
            if node["ip"] == ip and node["pub_key"] == pub_key:
                del node
        with open("info/Nodes.pickle", "wb") as file:
            pickle.dump(nodes, file)
    except:
        return "cancel invalid"



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


def message_handler(message):
    try:
        protocol = message[1]
    except:
        raise UnrecognisedArg("No Protocol Found")

    node_types = ["Lite", "Blockchain", "dist", "AI"]

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

        if not port > 0 and port < 65535:
            raise ValueTypeError("TCP port out of range")

        try:
            float(message[5])
            if "." not in message[5]:
                Exception()
        except:
            raise ValueTypeError("version not given as float")

        if message[6] not in node_types:
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

        if not port >= 0 and port < 65535:
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

    elif protocol == "ERROR":
        pass

    else:
        raise UnrecognisedCommand("protocol unrecognised")
