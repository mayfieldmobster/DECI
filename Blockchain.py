import pickle
import itertools
import hashlib
from ecdsa import SigningKey, VerifyingKey, SECP112r2
import node
import time

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
    key = SigningKey.generate(curve=SECP112r2)
    hex_key = key.to_string().hex()
    return key, hex_key

def pub_key_gen(private_key):
    public_KEY = private_key.verifying_key
    hex_key = public_KEY.to_string().hex()
    return public_KEY, hex_key

def sign_trans(private_key, transaction):
    signature = private_key.sign(transaction.encode())
    return signature



def add_transaction(transaction):
    with open("info/Blockchain.pickle", "rb") as file:
        blockchain = pickle.load(file)
        if len(blockchain[-1])< 50: # 50 transactions, prev and block hash
            print(blockchain[-1])
            if transaction not in blockchain:
                blockchain[-1].append(transaction)
            with open("info/Blockchain.pickle", "wb") as file:
                pickle.dump(blockchain, file)

        elif len(blockchain[-1]) >= 50:#51 as that the amount in the array without hash
            neg_block_hash = [hash_block(blockchain[-1])]#current block
            trans_fees = 0
            for trans in blockchain[-1]:
                try:
                    trans_fees += trans[3]*0.001
                except:
                    pass
            blockchain[-1].append([neg_block_hash,transaction[0]])
            blockchain[-1].append([trans_fees])
            blockchain[-1].append([False, transaction[0]])#validation status
            new_block = [neg_block_hash,transaction]
            blockchain.append(new_block)
            with open("info/Blockchain.pickle", "wb") as file:
                pickle.dump(blockchain, file)


def validate(block_hash):
    with open("info/Blockchain.pickle", "rb") as file:
        blockchain = pickle.load(file)
    current_index = 0
    for block in blockchain:#find block index
        if block[51][0] == block_hash:
            block_index = current_index
            break
        current_index += 1

    transindex = 0
    prev_time = 0

    for transaction in blockchain[block_index]:
        trans_no_sig = []
        trans_no_sig.append(transaction)
        trans_no_sig = list(itertools.chain.from_iterable(trans_no_sig))
        del trans_no_sig[4]
        trans_no_sig = " ".join(trans_no_sig)
        public_key = VerifyingKey.from_string(bytes.formathex(transaction[1]), curve=SECP112r2)
        try:
            assert public_key.verify(bytes.fromhex(transaction[4]), trans_no_sig.encode())
            if float(transaction[0]) >prev_time:
                prev_time = transaction[0]
            else:
                raise ValueError('times out of order')
            transindex += 1
        except:
            print("WTF")
            message = ["TRANS_INVALID", str(block_index), str(transindex)]
            message = " ".join(message)
            node.send_to_all(message)

        node.send_to_all("VALID "+ str(block_index))

    if transindex == 50:
        blockchain[block_index][52] = True
        with open("info/Blockchain.pickle", "wb") as file:
            pickle.dump(blockchain, file)



def invalid_trans(Block_index, trans_index):#for when theres a invalid transaction found
    with open("info/Blockchain.pickle", "rb") as file:
        blockchain = pickle.load(file)

    del blockchain[Block_index][trans_index]#delete false transaction
    secondary_blockchain = blockchain
    pre_hashed_blocks = []
    block_hashes = []
    for i in range(len(blockchain)-Block_index):
        del secondary_blockchain[Block_index + i][52]
        del secondary_blockchain[Block_index + i][51]
        pre_hashed_blocks.append(secondary_blockchain[Block_index + i])

    for block in pre_hashed_blocks:
        ONED_block = list(itertools.chain.from_iterable(block))
        block_str = " ".join(ONED_block)
        block_hashes.append(hash(block_str))

    for i in range(len(blockchain) - Block_index):#update hashes
        blockchain[Block_index + i][51] = [block_hashes[i]]

    with open("info/Blockchain.pickle", "w") as file:
        pickle.dump(blockchain, file)



def wallet_value(pub_adrress):
    with open("info/Blockchain.pickle", "rb") as file:
        blockchain = pickle.load(file)

    amount_in_wallet = 0.0

    for block in blockchain:
        if block[52][0]:
            for transaction in block:
                if transaction[2] == pub_adrress:
                    amount_in_wallet += float(transaction[3])
                if transaction[1] == pub_adrress:
                    amount_in_wallet -= float(transaction[3])
                    amount_in_wallet -= float(transaction[3]) * 0.001

    return amount_in_wallet


def trans_fee_calc(block_index):
    with open("info/Blockchain.pickle", "rb") as file:
        blockchain = pickle.load(file)

    trans_fee = 0.0
    for transaction in blockchain[block_index]:
        trans_fee += float(transaction[3])*0.001

    return trans_fee


def coin_val():
    GOD_WAL = wallet_value("8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033") #amount in god wallet
    sold = 50000000 - GOD_WAL
    val = sold*0.0037
    return val

def buy_cost(amount):
    start_val = coin_val()
    new_val = start_val + amount*0.0037
    total_val = start_val + new_val
    avg_val = total_val/2.0
    cost = avg_val*amount
    return cost

def sell_cost(amount):
    start_val = coin_val()
    new_val = start_val - amount * 0.0037
    total_val = start_val + new_val
    avg_val = total_val / 2.0
    cost = avg_val * amount
    return cost

def Block_valid(index, address):
    with open("info/Blockchain.pickle", "rb") as file:
        blockchain = pickle.load(file)
        if not blockchain[index][53][0]:
            blockchain[index][53] = [True, address, time.time()]

    with open("./info/Blockchain.pickle", "wb") as file:
        pickle.dump(blockchain, file)


def validator():
    with open("info/Blockchain.pickle", "rb") as file:
        blockchain = pickle.load(file)


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


                 









