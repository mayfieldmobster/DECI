import os
import node
import reciever
import reader
import trans_reader
import validator
import steak_trans
import concurrent.futures


"""
update tensorflow
update blockchain and nodes
"""
#open("recent_messages.txt", "w").close()#clear recent message file

local_ip = "127.0.0.1"#socket.gethostbyname(socket.gethostname())

os.system("pip3 install --upgrade tensorflow")
os.system("pip3 install --upgrade ecdsa")

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
    executor.submit(trans_reader.read)
    executor.submit(steak_trans.updator)
    executor.submit(validator.am_i_validator)













