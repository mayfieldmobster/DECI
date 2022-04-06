import node
import pickle
import logging

#send to all non dist nodes

def relay():
    do_not_send = ["NREQ","NODES?", "GET_NODES", "ONLINE?", "yh", "ERROR", "BLOCKCHAIN?", "BREQ"]
    logging.basicConfig(filename='relay.log',filemode='a', format='%(asctime)s  :  %(message)s', datefmt='%d-%b-%Y %H:%M:%S %p')  
    while True:
        with open("./info/Nodes.pickle", "rb") as file:
            nodes = pickle.load(file)
        with open("./info/relay_messages.txt", "w+") as file:
            messages = file.read().split("\n")
            file.write("")
        for message in messages:
            logging.info(message)
            for protocol in do_not_send:
                if protocol in message:
                    prot_in = True
            if prot_in:
                continue
            for node in nodes:
                if node["type"] != "dist":
                    try:
                        node.send(node["ip"],"DIST " + message)
                    except:
                        break#node offline

"""
functions that need to be run:
ONLINE?
NREQ
ALL NODE UPDATE COMMANDS
"""