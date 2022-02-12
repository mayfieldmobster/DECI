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
            no_error = False
            message = message.split(" ")
            try:
                node.error_handler(message)
                no_error = True
            except Exception as e:
                node.send(message[0], f"ERROR {e}")

            if no_error:
                if message[1] == "GET_NODES":
                    node.send_node(message[0])
                    print(message)

                elif message[1] == "HELLO":
                    node.new_node(message[2], message[0], message[3], message[4],message[5], message[6], message[7])
                    print(message)

                elif message[1] == "VALID":#update block to true
                    blockchain.validate_blockchain(int(message[2], message[0], message[3]))

                elif message[1] == "TRANS_INVALID":
                    if ip != message[0]:
                        blockchain.invalid_blockchain(int(message[2], int(message[3])))

                elif message[1] == "ONLINE?":
                    node.send(message[0], "yh")
                    print(message)

                elif message[1] == "BLOCKCHAIN?":
                    chain = blockchain.read_blockchain()
                    node.send(message[0], "BREQ " + chain.send_blockchain())

                elif message[1] == "UPDATE":
                    node.update_node(message[0],message[2], message[3], message[4], message[5], message[6])

                elif message[1] == "DELETE":
                    node.delete_node(message[2], message[0], message[3], message[4])

                else:
                    pass



if __name__ == "__main__":
    read()

