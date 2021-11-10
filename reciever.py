import node

def rec():
    while True:
        message,address = node.receive()

        print(address)
        file = open("recent_messages.txt", "a")

        file.write("\n" + address[0] + " " + " ".join(message))
        file.close()