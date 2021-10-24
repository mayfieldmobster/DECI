import node
import Blockchain

while True:
    NODE_Lines = node.file_reader("NODE")
    for message in NODE_Lines:
        if message[1] == "GET_NODES":
            message = message.split(" ")
            node.rec_protocols.get_node(message[0])

        if message[1] == "VERIFY":
            message = message.split(" ")
            node.rec_protocols.verify(message[0])

        if message[1] == "TRANS":
            message = node.ONE_D_message_compress(message)
            Blockchain.add_transaction(message)

