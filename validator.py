import time
import node
import Blockchain
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

def validator_updator(time):#can probably delete this function             could be used to have specific file for validator transactions
    with open("info/Validator.pickle", "rb") as file:
        validator = pickle.load(file)
        
    with open("info/Nodes.pickle", "rb") as file:
        nodes = pickle.load(file)
    
    with open("info/Blockchain.pickle", "rb") as file:
        blockchain = pickle.load(file)
    
    for node in nodes:
        if node[0] <= time:
            public = node[2]
            steak = "4aa5f462171c2c71129d6064b5c986a9a0610ff4afb1f90b13f4e29e"
            amount_steaked = 0.0
            for block in blockchain:
                if block[52][0]:
                    for transaction in block:
                        if transaction[1] == public and transaction[2] == steak:
                            amount_steaked += transaction[3]

                        if transaction[2] == public and transaction[1] == steak:
                            amount_steaked -= transaction[3]
        


def rb(hash, time):#random bias function returns index of node
    with open("info/Nodes.pickle", "rb") as file:
        nodes = pickle.load(file)

    with open("info/Blockchain.pickle", "rb") as file:
        blockchain = pickle.load(file)
        

    rb = []#random biased
    for node in nodes:
        if node[0] <= time:
            public = node[2]
            steak = "4aa5f462171c2c71129d6064b5c986a9a0610ff4afb1f90b13f4e29e"
            amount_steaked = 0.0
            for block in blockchain:
                if block[0][1] >= time:
                    break
                if block[52][0]:
                    for transaction in block:
                        if transaction[1] == public and transaction[2] == steak:
                            amount_steaked += transaction[3]

                        if transaction[2] == public and transaction[1] == steak:
                            amount_steaked -= transaction[3]

            amount_steaked = math.ceil(amount_steaked)

            for _ in range(int(amount_steaked)):
                rb.append(node)

    random.seed(hash_num(hash))
    ran_ind = random.randint(0, len(rb))

    return rb[ran_ind], time
    

def am_i_validator():
    time.sleep(4)
    with open("info/Public_key.txt", "r") as file:
        my_pub = file.read()
    while True:
        with open("info/Blockchain.pickle", "rb") as file:
            blockchain = pickle.load(file)
        block_num =0
        for block in blockchain:
            if not block[-1][0]:
                if int(time.time() - float(blockchain[-1][1]["time"])) > 900:
                    block_time = block[-1][1]
                    hash = block[51][0]
                    node,time_valid = rb(hash, block_time)
                    if node[2] == my_pub:
                        Blockchain.validate(hash, block_num, time_valid)


            block_num += 1


