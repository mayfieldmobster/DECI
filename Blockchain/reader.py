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
        time.sleep(1)
        NODE_Lines = node.request_reader("NODE")
        if NODE_Lines:
            print(f"NODE LINES: {NODE_Lines}")
            for message in NODE_Lines:
                no_error = False
                message = message.split(" ")
                try:
                    node.message_handler(message)
                    no_error = True
                except Exception as e:
                    node.send(message[0], f"ERROR {e}")
                    print(message[1], e)

                if no_error:
                    if message[1] == "GET_NODES":
                        print("GET_NODES")
                        node.send_node(message[0])

                    elif message[1] == "HELLO":
                        print("HELLO")
                        node.new_node(float(message[2]), message[0], message[3], int(message[4]), float(message[5]), message[6], message[7])

                    elif message[1] == "VALID":  # update block to true
                        print("VALID")
                        blockchain.validate_blockchain(int(message[2]), message[0], float(message[3]))

                    elif message[1] == "TRANS_INVALID":
                        print("TRANS_INVALID")
                        blockchain.invalid_blockchain(int(message[2]), int(message[3]), message[0])

                    elif message[1] == "ONLINE?":
                        print("ONLINE")
                        node.send(message[0], "yh")

                    elif message[1] == "BLOCKCHAIN?":
                        chain = blockchain.read_blockchain()
                        print("BLOCKCHAIN?")
                        node.send(message[0], "BREQ " + chain.send_blockchain())

                    elif message[1] == "UPDATE":
                        print("UPDATE")
                        node.update_node(message[0], float(message[2]), message[3], int(message[4]), float(message[5]), message[6])

                    elif message[1] == "DELETE":
                        print("DELETE")
                        node.delete_node(float(message[2]), message[0], message[3], message[4])

                    else:
                        pass

                else:
                    pass


if __name__ == "__main__":
    read()
