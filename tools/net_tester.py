"""
node2 is for testing
"""

import socket
import threading

def handle(client):
    while True:
        message = client.recv(1024)

def receive():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 1379))
    server.listen()
    while True:
        client, address = server.accept()
        message = client.recv(2048).decode("utf-8")
        try:
            print(message)
        except:
            pass
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


def send(host):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, 1379))
    message = " ".join(["HELLO",input(":::"),input(":::")])
    client.send(message.encode("utf-8"))


send("192.168.0.33")


