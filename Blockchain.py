import pickle
import itertools
import hashlib
from ecdsa import SigningKey, VerifyingKey, SECP112r2
from ecdsa.util import randrange_from_seed__trytryagain
import node

def hash_block(data):
    data = list(itertools.chain.from_iterable(data))
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
    public_KEY = private_key.verify_key
    hex_key = public_KEY.to_string().hex()
    return public_KEY

def sign_trans(private_key, transaction):
    signature = private_key.sign(transaction.encode())
    return signature



def add_transaction(transaction):
    with open("info/Blockchain.pickle", "rb") as file:
        blockchain = pickle.load(file)
        if len(blockchain[-1])< 51: # 50 transactions, prev and block hash, validation status
            print(blockchain[-1])
            blockchain[-1].append(transaction)
            with open("info/Blockchain.pickle", "wb") as file:
                pickle.dump(blockchain, file)

        elif len(blockchain[-1]) >= 51:#51 as that the amount in the array without hash and val
            neg_block_hash = [hash_block(blockchain[-1])]
            blockchain[-1].append(neg_block_hash)
            blockchain[-1].append([False])#validation status
            new_block = [neg_block_hash,transaction]
            blockchain.append(new_block)
            with open("info/Blockchain.pickle", "wb") as file:
                pickle.dump(blockchain, file)


def validate(block_hash):
    with open("info/Blockchain.pickle", "rb") as file:
        blockchain = pickle.load(file)
    current_index = 0
    for block in blockchain:#find block index
        if block[51] == block_hash:
            block_index = current_index
            break
        current_index += 1

    transindex = 0

    for transaction in blockchain[block_index]:
        trans_no_sig = []
        trans_no_sig.append(transaction)
        trans_no_sig = list(itertools.chain.from_iterable(trans_no_sig))
        del trans_no_sig[4]
        trans_no_sig = " ".join(trans_no_sig)
        public_key = VerifyingKey.from_string(bytes.formathex(transaction[1]), curve=SECP112r2)
        try:
            assert public_key.verify(bytes.fromhex(transaction[4]), trans_no_sig.encode())
            transindex += 1
        except:
            print("WTF")
            message = ["TRANS_INVALID", str(block_index), str(transindex)]
            message = " ".join(message)
            node.send_to_all(message)

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



def wallet_value(pub_adrress):
    with open("info/Blockchain.pickle", "rb") as file:
        blockchain = pickle.load(file)

    amount_in_wallet = 0.0

    for block in blockchain:
        for transaction in block:
            if transaction[2] == pub_adrress:
                amount_in_wallet += float(transaction[3])
            if transaction[1] == pub_adrress:
                amount_in_wallet -= float(transaction[3])

    return amount_in_wallet



        


#add_transaction(trans)









