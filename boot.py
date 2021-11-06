import os
import node
import concurrent.futures
import time
"""
update tensorflow
update blockchain and nodes
"""
open("recent_messages.txt", "w").close()#clear recent message file

with concurrent.futures.ProcessPoolExecutor as executor:
    executor.submit(node.receiver)#start recieving
    executor.submit(node.send_protocols.get_blockchain)#update blockchain
    executor.submit(node.rec_protocols.get_node)#update nodes
    time.sleep(5)#allow for time to get nodes and blockchain























































