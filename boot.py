import os
import node
import concurrent.futures
import reciever
import reader
import time
import validator
import test
"""
update tensorflow
update blockchain and nodes
"""
#open("recent_messages.txt", "w").close()#clear recent message file


with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.submit(reciever.rec)#start recieving
    executor.submit(node.send_protocols.get_blockchain)#update blockchain
    executor.submit(node.rec_protocols.get_node)#update nodes
    executor.submit(validator.am_i_validator, "7fd8a5ba6916444357da92a5648e757af6ace943c05894ea53f7967f")
    executor.submit(reader.main)























































