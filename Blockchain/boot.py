import os
import node
import reciever
import reader
import trans_reader
import validator
import pre_reader
import concurrent.futures
import socket


"""
update tensorflow
update Blockchain and nodes
"""

open("recent_messages.txt", "w").close()#clear recent message file
local_ip = socket.gethostbyname(socket.gethostname())
#os.system("pip3 install --upgrade ecdsa")
local_ip = input("IP: ").replace(" ", "")
"""
try:
    os.remove("install.py")
    os.remove("install.exe")
except:
    pass#wont work after first time ill come up with better way later
"""

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.submit(reciever.rec, local_ip)  # start recieving ✅
    executor.submit(node.updator())  # update Blockchain & Nodes ✅
    executor.submit(reader.read)
    executor.submit(trans_reader.read)
    executor.submit(validator.am_i_validator)
    executor.submit(pre_reader.read)













