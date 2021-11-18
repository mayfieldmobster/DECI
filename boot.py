import os
import node
import concurrent.futures
import reciever
import reader
import AI_reader
import time
import validator
import test
import socket
"""
update tensorflow
update blockchain and nodes
"""
#open("recent_messages.txt", "w").close()#clear recent message file
#with open("recent_messages.txt", "w") as file:
    #file.write("")

local_ip = "127.0.0.1"#socket.gethostbyname(socket.gethostname())

"""
try:
    os.remove("install.py")
    os.remove("install.exe")
except:
    pass#wont work after first time ill come up with better way later
"""

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.submit(reciever.rec, local_ip)#start recieving
    executor.submit(node.get_blockchain)#update blockchain
    executor.submit(node.get_nodes)#update nodes
    executor.submit(reader.read)
    executor.submit(validator.am_i_validator, "7fd8a5ba6916444357da92a5648e757af6ace943c05894ea53f7967f")
    #executor.submit(AI_reader.read)












