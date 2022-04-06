import node
import distributor


def rec(my_ip):
    print("---RECEIVER STARTED---")
    while True:
        message, address = node.receive(my_ip)
        print(f"Message from {address} , {message}\n")
        with open("recent_messages.txt", "a") as file:
            file.write(f"{address[0]} {' '.join(message)}\n")
        with open("relay_messages.txt", "a") as file:
            file.write(f"{address[0]} {' '.join(message)}\n")
        



if __name__ == "__main__":
    rec("192.168.68.112")
