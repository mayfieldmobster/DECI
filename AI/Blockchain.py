import pickle
import itertools
import hashlib
from ecdsa import SigningKey, VerifyingKey, SECP112r2
import node
import time
from ecdsa.util import randrange_from_seed__trytryagain
import os
from blockchain import validator


def hash_block(data):
    data = list(itertools.chain.from_iterable(data))
    print(data)
    str_data = " ". join(data)
    hashed = hashlib.sha256(str_data.encode())
    hex_hashed = hashed.hexdigest()
    return hex_hashed

def hash(data):
    hashed = hashlib.sha256(data.encode())
    hex_hashed = hashed.hexdigest()
    return hex_hashed

def priv_key_gen():
    seed = os.urandom(SECP112r2.baselen)
    secexp = randrange_from_seed__trytryagain(seed, SECP112r2.order)
    key,hex_key = SigningKey.from_secret_exponent(secexp,curve=SECP112r2)
    return key, hex_key

def pub_key_gen(private_key):
    public_KEY = private_key.verifying_key
    hex_key = public_KEY.to_string().hex()
    return public_KEY, hex_key

def sign_trans(private_key, transaction):
    signature = private_key.sign(transaction.encode())
    return signature



def add_transaction(transaction):
    with open("../info/Blockchain.pickle", "rb") as file:
        blockchain = pickle.load(file)
        if len(blockchain[-1])< 500: # 500 transactions, prev and block hash
            print(blockchain[-1])
            if not transaction in blockchain[-1] or transaction in blockchain[-2]:
                blockchain[-1].append(transaction)
                block = blockchain[-1]
                blockchain[-1] = sorted(block, key=lambda block:block[0])
                with open("../info/Blockchain.pickle", "wb") as file:
                    pickle.dump(blockchain, file)




        elif len(blockchain[-1]) >= 500:#500 as that the amount in the array without hash
            neg_block_hash = [hash_block(blockchain[-1])]#current block
            trans_fees = 0
            for trans in blockchain[-1]:
                try:
                    trans_fees += trans[3]*0.01
                except:
                    pass
            blockchain[-1].append([neg_block_hash,transaction[0]])
            blockchain[-1].append([trans_fees])
            blockchain[-1].append([False, transaction[0]])#validation status
            new_block = [neg_block_hash,transaction]
            blockchain.append(new_block)
            with open("../info/Blockchain.pickle", "wb") as file:
                pickle.dump(blockchain, file)


def validate(block_hash, block_index, time_of_validation, validator=True):
    with open("../info/Blockchain.pickle", "rb") as file:
        blockchain = pickle.load(file)

    transindex = 0
    prev_time = blockchain[block_index-1][503][1]#time of prev block for reference
    not_transactions = [0,-3,-2,-1]

    for transaction in blockchain[block_index]:
        if transindex not in not_transactions:
            trans_no_sig = []
            for value in transaction:
                trans_no_sig.append(value)
            del trans_no_sig[4] #left with trans without sig
            trans_no_sig = " ".join(trans_no_sig)
            public_key = VerifyingKey.from_string(bytes.formathex(transaction[1]), curve=SECP112r2)
            try:

                assert public_key.verify(bytes.fromhex(transaction[4]), trans_no_sig.encode())#check if sig correct

                if float(transaction[0]) > prev_time:#check if time stamp correct
                    prev_time = transaction[0]

                elif float(transaction[0]) < float(prev_time):
                    raise ValueError('times out of order')

                if float(wallet_value(transaction[1])) <= float(transaction[3]):
                    raise ValueError("not enough money")


            except:
                if validator:
                    print("WTF")
                    message = ["TRANS_INVALID", str(block_index), str(transindex)]#BIG PROBLEM ADD SEND TO ALL EXCEPT SELF
                    message = " ".join(message)
                    node.send_to_all(message)
                    invalid_trans(block_index,transindex)

                if not validator:
                    return False
            transindex += 1

    with open("../info/Blockchain.pickle", "rb")as file:
        blockchain = pickle.load(file)
        block = blockchain[block_index]
        del block[-1]#get just transactions to hash
        del block[-1]
        del block[-1]
        hash = hash_block(block)

    if validator:
        node.send_to_all("VALID "+ str(block_index) + " " + str(time_of_validation) + " " + hash)

    if not validator:
        return True




def invalid_trans(block_index, trans_index):#for when theres a invalid transaction found
    with open("../info/Blockchain.pickle", "rb") as file:
        blockchain = pickle.load(file)

    block_index = int(block_index)
    trans_index = int(trans_index)
    if trans_index == 1:
        prev_time = blockchain[block_index-1][-1][1]
    else:
        prev_time = blockchain[block_index][trans_index-1][0]

    transaction = blockchain[block_index][trans_index]
    prev_time = blockchain[block_index][trans_index-1][0]
    trans_no_sig = []
    for value in transaction:
        trans_no_sig.append(value)
    del trans_no_sig[4]  # left with trans without sig
    trans_no_sig = " ".join(trans_no_sig)


    public_key = VerifyingKey.from_string(bytes.formathex(transaction[1]), curve=SECP112r2)
    try:
        assert public_key.verify(bytes.fromhex(transaction[4]), trans_no_sig.encode())  # check if sig correct

        if float(transaction[0]) < float(prev_time):
            raise ValueError('times out of order')

        if float(wallet_value(transaction[1])) < float(transaction[3]):
            raise ValueError("not enough money")

        invalid_tran = False

    except:
        invalid_tran = True

    if invalid_tran:
        del blockchain[block_index][trans_index]#delete false transaction
        secondary_blockchain = []
        for value in blockchain:
            secondary_blockchain.append(value)
        pre_hashed_blocks = []
        block_hashes = []
        for i in range(len(blockchain)-block_index):
            del secondary_blockchain[block_index + i][-1]
            del secondary_blockchain[block_index + i][-1]
            del secondary_blockchain[block_index + i][-1]
            pre_hashed_blocks.append(secondary_blockchain[block_index + i])

        for block in pre_hashed_blocks:
            ONED_block = list(itertools.chain.from_iterable(block))
            block_str = " ".join(ONED_block)
            block_hashes.append(hash(block_str))

        for i in range(len(blockchain) - block_index):#update hashes
            blockchain[block_index + i][-3] = [block_hashes[i]]
            blockchain[block_index + i+1][0] = [block_hashes[i]]

        with open("../info/Blockchain.pickle", "w") as file:
            pickle.dump(blockchain, file)



def wallet_value(pub_adrress):
    with open("../info/Blockchain.pickle", "rb") as file:
        blockchain = pickle.load(file)

    amount_in_wallet = 0.0

    for block in blockchain:
        if block[-1][0]:
            for transaction in block:
                if transaction[2] == pub_adrress:
                    amount_in_wallet += float(transaction[3])
                if transaction[1] == pub_adrress:
                    amount_in_wallet -= float(transaction[3])
                    amount_in_wallet -= float(transaction[3]) * 0.01

    return amount_in_wallet


def trans_fee_calc(block_index):
    with open("../info/Blockchain.pickle", "rb") as file:
        blockchain = pickle.load(file)

    trans_fee = 0.0
    for transaction in blockchain[block_index]:
        trans_fee += float(transaction[3])*0.01

    return trans_fee



def Block_valid(index, address, time_of_valid, hash):
    with open("../info/Blockchain.pickle", "rb") as file:

        blockchain = pickle.load(file)
        node = validator.rb(hash, blockchain[index][-1][0])
        cor_validation = validate(hash,index,time_of_valid,False)
        if cor_validation:
            if node[1] == address:
                if not blockchain[index][-1][0]:
                    blockchain[index][-1] = [True, time_of_valid, address]

    with open("../info/Blockchain.pickle", "wb") as file:
        pickle.dump(blockchain, file)




def trans(sender, receiver, amount, priv_key):
    trans = []
    trans_time = time.time()
    trans.append(str(trans_time))
    trans.append(sender)
    trans.append(receiver)
    trans.append(str(amount))
    str_trans = " ".join(trans)
    priv_key = SigningKey.from_string(bytes.fromhex(priv_key), curve=SECP112r2)
    signature = priv_key.sign(str_trans.encode())
    trans.append(signature)
    if amount < wallet_value(sender):
        str_trans = str(trans)
        str_trans = str_trans.replace(" ", "")
        node.send_to_all("TRANS " + str_trans)











