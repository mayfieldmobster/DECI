from blockchain import node
import time
from requests import get#
import pickle

def read():
    time.sleep(5)
    print("reader started")
    ip = get('https://api.ipify.org').text
    while True:
        NODE_Lines = node.request_reader("NODE")
        for message in NODE_Lines:
            message = message.split(" ")

            if message[1] == "GET_NODES":
                node.send_node(message[0])
                print(message)

            if message[1] == "HELLO":
                node.new_node(message[2], message[0], message[3])
                print(message)

            if message[1] == "VALID":#update block to true
                with open("../info/Blockchain.pickle", "rb") as file:
                    blockchain = pickle.load(file)
                with open("../info/Nodes.pickle", "rb") as file:
                    nodes = pickle.load(file)
                for nod in nodes:
                    if nod[1] == message[0]:
                        address = nod[2]
                        break
                blockchain.block_valid(int(message[2]), address, message[3])
                print(message)
                with open("info/Blocks.pickle","wb") as file:
                    pickle.dump(blockchain, file)

            if message[1] == "TRANS_INVALID":
                if ip != message[0]:
                    with open("../info/Blockchain.pickle", "rb") as file:
                        blockchain = pickle.load(file)
                    blockchain.invalid_trans(int(message[2]),int(message[3]))
                    print(message)
                    with open("info/Blocks.pickle", "wb") as file:
                        pickle.dump(blockchain, file)

            if message[1] == "BLOCKCHAIN?":
                with open("../info/Blockchain.pickle", "rb") as file:
                    blockchain = pickle.load(file)
                node.send_node(message[0], "BLOCKCHAIN " + blockchain.send_blockchain())

            if message[1] == "BLOCKCHAIN":
                with open("../info/Blockchain.pickle", "rb") as file:
                    blockchain = pickle.load(file)
                blockchain.update(message)

            else:
                pass



if __name__ == "__main__":
    read()

