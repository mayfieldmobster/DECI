import os
import node
import concurrent.futures
"""
update tensorflow
update blockchain and nodes
"""

with concurrent.futures.ProcessPoolExecutor as executor:
    executor.submit(node.receiver())
    executor.submit(node.send_protocols.get_blockchain())
    executor.submit()




















































