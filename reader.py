import node
import Blockchain
import ast
import time

def read():
    time.sleep(5)
    print("reader started")
    while True:
        NODE_Lines = node.request_reader("NODE")
        for message in NODE_Lines:
            message = message.split(" ")

            if message[1] == "GET_NODES":
                node.send_node(message[0])
                print("test",message)

            if message[1] == "TRANS":
                Blockchain.add_transaction(ast.literal_eval(message[2]))
                print("test",message)

            if message[1] == "HELLO":
                node.new_node(message[2], message[0], message[3])
                print("test",message)

            if message[1] == "VALID":#update block to true
                Blockchain.Block_valid(int(message[2]), message[0])#need to discover POS random picker find at blockchain.vaildator
                print("test",message)

            if message[1] == "TRANS_INVALID":
                Blockchain.invalid_trans(int(message[2]),int(message[3]))
                print("test",message)

            else:
                pass



if __name__ == "__main__":
    read()

