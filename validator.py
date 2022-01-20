import time
import node
import random
import pickle
import math


"""
check amount staked by node from that info
get current block hash seed 
"""


def hash_num(hash):
    num = int(hash,16)
    return num


def rb(hash, time, return_length=1):#random bias function returns index of node
    with open("info/Nodes.pickle", "rb") as file:
        nodes = pickle.load(file)

    with open("info/stake_trans.pickle", "rb") as file:
        stake_trans = pickle.load(file)

    rb = []#random biased
    for node in nodes:
        public = node[2]
        amount_steaked = 0.0
        for transaction in stake_trans:
            if float(transaction["time"]) < time:

                if transaction["sender"] == public:
                    amount_steaked -= transaction["amount"]*0.99

                if transaction["reciever"] == public:
                    amount_steaked += transaction["amount"]*0.99

        amount_steaked = math.ceil(amount_steaked)
        rb.append(amount_steaked)

    random.seed(hash_num(hash))
    rand_node = random.choices(nodes, weights=rb, k=return_length)

    return rand_node, time
    

def am_i_validator():
    time.sleep(4)
    with open("info/Public_key.txt", "r") as file:
        my_pub = file.read()
    while True:
        with open("info/Blockchain.pickle", "rb") as file:
            blockchain = pickle.load(file)
            blockchain = blockchain
        block_num =0
        for block in blockchain:
            if not block[-1][0]:
                if int(time.time() - float(blockchain[-1][1]["time"])) > 900:
                    block_time = block[-1][1]
                    hash = block[-3][0]
                    node,time_valid = rb(hash, block_time)
                    if node[2] == my_pub:
                        blockchain.validate(hash, block_num, time_valid)


            block_num += 1


