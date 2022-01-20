import AI
import node

def read():
    while True:
        AI_Lines = node.request_reader("AI")
        if AI_Lines != []:
            for message in AI_Lines:
                message = message.split(" ")

                if message[1] == "ONLINE?":
                    node.send_node(message[0], "yh")
                    print(message)

                elif message[1] == "AI":
                    AI.AI_REQ(message)

                else:
                    pass


if __name__ == "__main__":
    read()