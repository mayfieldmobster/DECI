import AI
import node

def read():
    while True:
        AI_Lines = node.request_reader("AI")
        for message in AI_Lines:
            if len(message) != 0:
                AI.AI_REQ(message)


if __name__ == "__main__":
    read()