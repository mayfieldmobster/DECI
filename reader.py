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
                node.rec_protocols.get_node(message[0])
                print(message)

            if message[1] == "VERIFY":
                node.rec_protocols.verify(message[0])
                print(message)

            if message[1] == "TRANS":
                Blockchain.add_transaction(ast.literal_eval(message[2]))
                print(message)

            if message[1] == "HELLO":
                node.rec_protocols.new_node(message[2], message[0], message[3])
                print(message)

            if message[1] == "VALID":#update block to true
                Blockchain.Block_valid(int(message[2]), message[0])#need to discover POS random picker find at blockchain.vaildator
                print(message)

            if message[1] == "TRANS_INVALID":
                Blockchain.invalid_trans(int(message[2]),int(message[3]))
                print(message)


        open("recent_messages.txt", "w").close()
        with open("recent_messages.txt", "w") as file:
            file.write("\n 0 0")


if __name__ == "__main__":
    read()

