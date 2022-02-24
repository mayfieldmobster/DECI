import node
import time
from requests import get
import pickle
import blockchain


def read():
    time.sleep(60)
    print("---READER STARTED---")
    ip = get('https://api.ipify.org').text
    while True:
        NODE_Lines = node.request_reader("NODE")
        if NODE_Lines:
            for message in NODE_Lines:
                no_error = False
                message = message.split(" ")
                try:
                    node.message_handler(message)
                    no_error = True
                except Exception as e:
                    node.send(message[0], f"ERROR {e}")

                if no_error:
                    if message[1] == "GET_NODES":
                        print(message)
                        node.send_node(message[0])

                    elif message[1] == "HELLO":
                        print(message)
                        node.new_node(float(message[2]), message[0], message[3], int(message[4]), float(message[5]), message[6], message[7])

                    elif message[1] == "VALID":  # update block to true
                        print(message)
                        blockchain.validate_blockchain(int(message[2]), message[0], float(message[3]))

                    elif message[1] == "TRANS_INVALID":
                        if ip != message[0]:
                            print(message)
                            blockchain.invalid_blockchain(int(message[2]), int(message[3]), message[0])

                    elif message[1] == "ONLINE?":
                        print(message)
                        node.send(message[0], "yh")

                    elif message[1] == "BLOCKCHAIN?":
                        chain = blockchain.read_blockchain()
                        print(message)
                        node.send(message[0], "BREQ " + chain.send_blockchain())

                    elif message[1] == "UPDATE":
                        print(message)
                        node.update_node(message[0], float(message[2]), message[3], int(message[4]), float(message[5]), message[6])

                    elif message[1] == "DELETE":
                        print(message)
                        node.delete_node(float(message[2]), message[0], message[3], message[4])

                    else:
                        pass


if __name__ == "__main__":
    read()
