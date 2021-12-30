import node
import Blockchain
import ast
import time
from requests import get

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
                Blockchain.Block_valid(int(message[2]), message[0], message[3],message[4])
                print(message)

            if message[1] == "TRANS_INVALID":
                if ip != message[0]:
                    Blockchain.invalid_trans(int(message[2]),int(message[3]))
                    print(message)


            else:
                pass



if __name__ == "__main__":
    read()

