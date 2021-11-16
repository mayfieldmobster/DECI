import node

def rec(my_ip):
    while True:
        message,address = node.receive(my_ip)

        print(address)
        file = open("recent_messages.txt", "a")

        file.write("\n" + address[0] + " " + " ".join(message))
        file.close()


if __name__ == "__main__":
    rec()
