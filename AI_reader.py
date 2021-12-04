import AI
import node

def read():
    while True:
        AI_Lines = node.request_reader("AI")
        for message in AI_Lines:
            message = message.split(" ")

            if message[1] == "ONLINE?":
                node.send_node(message[0], "yh")
                print(message)

            if message[1] == "AI":
                AI.AI_REQ(message)

if __name__ == "__main__":
    read()