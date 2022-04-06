import node


def rec(my_ip):
    print("---RECEIVER STARTED---")
    while True:
        message, address = node.receive(my_ip)
        print(f"Message from {address} , {message}\n")
        if "DIST" in message:
            with open("recent_messages.txt", "a") as file:
                file.write(f"{message.replace('DIST ','')}\n")
        else:
            with open("recent_messages.txt", "a") as file:
                file.write(f"{address[0]} {message}\n")
            


if __name__ == "__main__":
    rec("192.168.68.112")
