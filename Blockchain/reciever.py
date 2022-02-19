import node


def rec(my_ip):
    print("---RECEIVER STARTED---")
    while True:
        message, address = node.receive(my_ip)
        print(message)
        print(address)
        with open("recent_messages.txt", "a") as file:
            file.write("\n" + address[0] + " " + " ".join(message))


if __name__ == "__main__":
    rec("192.168.68.112")
