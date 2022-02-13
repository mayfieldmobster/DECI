import objsize#
import socket

import random
arr = ["a","b","c"]
bias = [0.1,0.2,0.3]
print(random.choices(arr,bias,k=6))

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 12))
    client.send("hello".encode("utf-8"))
except Exception as e:
    if isinstance(e, ConnectionRefusedError):
        print("hello")