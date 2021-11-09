import node
import Blockchain
import ast

def main():
    while True:
        NODE_Lines = node.request_reader("NODE")
        for message in NODE_Lines:
            message = message.split(" ")

            if message[1] == "GET_NODES":
                node.rec_protocols.get_node(message[0])

            if message[1] == "VERIFY":
                node.rec_protocols.verify(message[0])

            if message[1] == "TRANS":
                Blockchain.add_transaction(message)

            if message[1] == "HELLO":
                node.rec_protocols.new_node(message[2], message[0], message[3])

            if message[1] == "VALID":#update block to true
                Blockchain.Block_valid(message[2], message[0])#need to discover POS random picker find at blockchain.vaildator

            if message[1] == "TRANS_INVALID":
                Blockchain.invalid_trans(int(message[2]),int(message[3]))

            


