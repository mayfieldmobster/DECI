from blockchain import node
import time
from requests import get
import pickle
import blockchain

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

            elif message[1] == "HELLO":
                node.new_node(message[2], message[0], message[3])
                print(message)

            elif message[1] == "VALID":#update block to true
                blockchain.validate_blockchain(int(message[2], message[0], message[3]))

            elif message[1] == "TRANS_INVALID":
                if ip != message[0]:
                    blockchain.invalid_blockchain(int(message[2], int(message[3])))

            elif message[1] == "ONLINE?":
                node.send_node(message[0], "yh")
                print(message)

            elif message[1] == "BLOCKCHAIN?":
                chain = blockchain.read_blockchain
                node.send_node(message[0], "BLOCKCHAIN " + chain.send_blockchain())


            else:
                pass



if __name__ == "__main__":
    read()

