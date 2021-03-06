import itertools
import hashlib
import ast
from ecdsa import SigningKey, VerifyingKey, SECP112r2
import node
from ecdsa.util import randrange_from_seed__trytryagain
import os
import validator
import copy
# from numba import jit
import pickle
import time
import random


def priv_key_gen():
    seed = os.urandom(SECP112r2.baselen)
    secexp = randrange_from_seed__trytryagain(seed, SECP112r2.order)
    key = SigningKey.from_secret_exponent(secexp, curve=SECP112r2)
    hex_key = key.to_string().hex()
    return key, hex_key


def pub_key_gen(private_key):
    public_key = private_key.verifying_key
    hex_key = public_key.to_string().hex()
    return public_key, hex_key


def sign_trans(private_key, transaction):
    signature = private_key.sign(transaction.encode())
    return signature

def quick_sort_block(arr):
    less = []
    equal = []
    greater = []

    if len(arr) > 1:
        pivot = arr[len(arr)//2]
        for x in arr:
            if x["time"] < pivot["time"]:
                less.append(x)
            elif x["time"] == pivot["time"]:
                equal.append(x)
            elif x["time"] > pivot["time"]:
                greater.append(x)
        return quick_sort_block(less) + equal + quick_sort_block(greater)
    else:
        return arr

class Blockchain:

    def __init__(self):
        self.chain = [[["0"], {"time": 0.0, "sender": "0", "reciever": "0", "amount": 2 ** 23, "sig": "0"},
                       ["c484eb3cfd69ad6c289dcc1e1b671929cdb7b6a63f75a4d21e8d1e126ad8433d", 0.0], [0],
                       [True, 1.0, "0"]],
                      [["c484eb3cfd69ad6c289dcc1e1b671929cdb7b6a63f75a4d21e8d1e126ad8433d"],
                       {"time": 901.0, "sender": "0",
                        "receiver": "8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033", "amount": 2 ** 23,
                        "sig": "0"}, ["89ecd70035817c54d5aaef888e3e9d9a8ddd2d4c96b20c73032d0a454dc066a2", 901.0], [0],
                       [True, 902.0, "0"]]
                     ]

    def __repr__(self):
        return str(self.chain)  # .replace("]", "]\n")


    def print_block(self, block_index):
        return str(self.chain[block_index]).replace("]", "]\n")

    def __len__(self, block = -1):
        if block == -1:
            return len(self.chain)
        elif block >= 0 :
            return len(self.chain[block])
        else:
            raise IndexError("Block Index now found")

    def __bool__(self):
        print("The Blockchain never lies")
        return True

    def __call__(self):
        return self.chain

    def get_block(self, block_index: int):
        try:
            return self.chain[block_index]
        except IndexError as e:
            print("block not found")

    def block_sort(self, block):
        sort = copy.copy(block)
        block_head = sort.pop(0)
        return block_head + quick_sort_block(sort)


    def all_transactions(self, address: str):
        transactions = []
        for block in self.chain:
            for trans in block:
                if trans["sender"] == address:
                    transactions.append(trans)
                    print(trans)
                if trans["receiver"] == address:
                    transactions.append(trans)
                    print(trans)
        return transactions

    @property
    def transaction_total(self):
        total = 0.0
        for block in self.chain:
            total += block[-2][0]
        return total

    def hash_block(self, block):
        string_block = str(block).replace(" ", "")
        hashed = hashlib.sha256(string_block.encode())
        hex_hashed = hashed.hexdigest()
        return hex_hashed

    def update(self, new_chain):
        self.chain = new_chain
        print("BLOCKCHAIN UPDATED SUCCESSFULLY")

    # @jit(nopython=True)
    def wallet_value(self, wallet_address, block_index = None):
        value = 0.0
        if not block_index:
            block_index = len(self.chain) - 1
        for block in self.chain[:(block_index + 1)]:
            for trans in block:
                if isinstance(trans, dict):
                    if "amount" in trans:
                        if trans["sender"] == wallet_address:
                            value -= float(trans["amount"])
                            continue
                        if trans["receiver"] == wallet_address:
                            if block[-1][0]: # dont add trans amount to value if block not valid
                                value += (float(trans["amount"]) * 0.99)
                                continue
                    elif "stake_amount" in trans and trans["pub_key"]== wallet_address:
                        value -= trans["stake_amount"]
                        continue
                    elif "unstake_amount" in trans and trans["pub_key"] == wallet_address:
                        if block[-1][0]:
                            value += trans["unstake_amount"]

            if block[-1][0]:
                if block[-1][2] == wallet_address:
                    value += block[-2][0] * 0.5

        return value

    def get_stake_value(self, wallet_address, block_index=None):
        value = 0.0
        if not block_index:
            block_index = len(self.chain) - 1
        for block in self.chain[:(block_index + 1)]:  # the reason to not use stake_trans.pickle is you don't know id the trans is valid
            for trans in block:
                if isinstance(trans, dict):
                    if "amount" in trans:
                        continue
                    if trans["pub_key"] == wallet_address:
                        if "stake_amount" in trans:
                            if block[-1][0]:
                                value += trans["stake_amount"]
                        elif "unstake_amount" in trans:
                            value -= trans["stake_amount"]

        return value




    def add_transaction(self, trans: dict):
        relative_time = int(float(trans["time"]) - float(self.chain[-1][1]["time"]))
        prev_relative_time = int(float(trans["time"]) - float(self.chain[-2][1]["time"]))
        # prev_relative_time = 10000

        if relative_time < 900:
            if relative_time < 0:
                if prev_relative_time < 900:
                    if not self.chain[-2][-1][0]:
                        self.chain[-2].insert(-3, trans)

                        temp_block = copy.copy(self.chain)

                        temp_block.pop()
                        temp_block.pop()
                        temp_block.pop()

                        self.chain[-2][-3] = [self.hash_block(temp_block), trans["time"]]
                        self.chain[-1][0] = [self.hash_block(temp_block)]
                        self.chain[-2][-2][0] += (trans["amount"] * 0.01)
                        self.chain[-2][-1][1] = trans["time"]

            elif relative_time > 0:
                self.chain[-1].append(trans)

        elif relative_time > 900:
            b_time = self.chain[-1][-1]["time"]
            block_hash = self.hash_block(self.chain[-1])
            trans_fees = 0
            for b_trans in self.chain[-1]:
                if isinstance(b_trans, dict):
                    if "amount" in b_trans:
                        trans_fees += b_trans["amount"] * 0.01

            block = copy.copy(self.chain[-1])
            self.chain[-1] = self.block_sort(self.chain[-1])
            #  self.chain[-1] = block.insert(0, self.chain[-1][0]) this was coded a while ago there may be a reason but idk
            self.chain[-1].append([block_hash, b_time])
            self.chain[-1].append([trans_fees])
            self.chain[-1].append([False, b_time])

            new_block = [[block_hash], trans]
            self.chain.append(new_block)

    def add_protocol(self, announcement):
        relative_time = int(float(announcement["time"]) - float(self.chain[-1][1]["time"]))
        prev_relative_time = int(float(announcement["time"]) - float(self.chain[-2][1]["time"]))
        # prev_relative_time = 10000

        if relative_time < 900:  # if within the 15 mins of current block
            if relative_time < 0:  # if not from the past
                if prev_relative_time < 900:  # in order to add to previous block if within the aloud lateness time in
                    if not self.chain[-2][-1][0]:

                        self.chain[-2].insert(-3, announcement)

                        temp_block = []
                        temp_block = copy.copy(self.chain)

                        temp_block.pop()
                        temp_block.pop()
                        temp_block.pop()

                        self.chain[-2][-3] = [self.hash_block(temp_block), announcement["time"]]
                        self.chain[-1][0] = [self.hash_block(temp_block)]
                        self.chain[-2][-1][1] = announcement["time"]

            elif relative_time > 0:  # if in current block
                self.chain[-1].append(announcement)

        elif relative_time > 900:  # if new block is needed
            b_time = self.chain[-1][-1]["time"]
            block_hash = self.hash_block(self.chain[-1])
            trans_fees = 0
            for b_trans in self.chain[-1]:
                if isinstance(b_trans, dict):
                    if "amount" in b_trans:
                        trans_fees += b_trans["amount"] * 0.01

            block = copy.copy(self.chain[-1])
            self.chain[-1] = self.block_sort(self.chain[-1])
            #self.chain[-1] = block.insert(0, self.chain[-1][0])
            self.chain[-1].append([block_hash, b_time])
            self.chain[-1].append([trans_fees])
            self.chain[-1].append([False, b_time])

            new_block = [[block_hash], announcement]
            self.chain.append(new_block)


    def validate(self, block_index: int, time_of_validation: float = 0.0, validating: bool = True):
        trans_index = 0
        for trans in self.chain[block_index]:
            if isinstance(trans, dict):
                if "amount" in trans:
                    if self.wallet_value(trans["sender"], block_index=block_index) < float(trans["amount"]):
                        if validating:
                            message = f"TRANS_INVALID {block_index} {trans_index}"
                            node.send_to_dist(message)
                            self.invalid_trans(block_index, trans_index)

                        if not validating:
                            return False
                
                if "stake_amount" in trans:
                    if self.wallet_value(trans["pub_key"], block_index=block_index) < float(trans["stake_amount"]):
                        if validating:
                            message = f"TRANS_INVALID {block_index} {trans_index}"
                            node.send_to_dist(message)
                            self.invalid_trans(block_index, trans_index)

                        if not validating:
                            return False

                if "unstake_amount" in trans:
                    if self.get_stake_value(trans["pub_key"], block_index=block_index) < float(trans["unstake_amount"]):
                        if validating:
                            message = f"TRANS_INVALID {block_index} {trans_index}"
                            node.send_to_dist(message)
                            self.invalid_trans(block_index, trans_index)

                        if not validating:
                            return False

            trans_index += 1

        if validating:
            node.send_to_dist("VALID " + str(block_index) + " " + str(time_of_validation))

        if not validating:
            return True

    def invalid_trans(self, block_index: int, trans_index: int, ip: str):
        nodes = read_nodes()
        node_pub = None
        for nod in nodes:
            if nod["ip"] == ip:
                node_pub = nod["pub_key"]

        if not node_pub:
            return

        block_index = int(block_index)
        trans_index = int(trans_index)

        trans = self.chain[block_index][trans_index]
        trans_no_sig = copy.copy(trans)
        trans_no_sig.pop("sig")
        trans_no_sig = " ".join(trans_no_sig)
        public_key = VerifyingKey.from_string(bytes.formathex(trans["sender"]), curve=SECP112r2)

        try:
            assert public_key.verify(bytes.fromhex(trans["sig"]), trans_no_sig.encode())

            if self.wallet_value(trans["sender"], block_index=block_index) < float(trans["amount"]):
                raise ValueError("sender does not have ")

            invalid_trans = False

        except:
            invalid_trans = True

        if invalid_trans:
            del self.chain[block_index][trans_index]
            pre_hashed_blocks = copy.copy(self.chain)

            for i in range(len(self.chain) - block_index):  # update hashes
                pre_hashed_blocks[block_index + i].pop()
                pre_hashed_blocks[block_index + i].pop()
                pre_hashed_blocks[block_index + i].pop()
                block_hash = self.hash_block(pre_hashed_blocks[block_index + i])
                self.chain[block_index + i][-3][0].append(block_hash)
                self.chain[block_index + i + 1][0] = [block_hash]

        if not invalid_trans:
            stake_removal = f"LIAR {node_pub} {ip}"
            with open("./info/stake_trans.pickle") as file:
                stake_trans = pickle.load(file)
            stake_trans.append(stake_removal)
            with open("./info/stake_trans.pickle") as file:
                pickle.dump(file)

    def block_valid(self, block_index: int, public_key: str, time_of_validation: float):
        # check if is actual validator
        nodes = []
        for block_hash in self.chain[block_index][-3]:
            val_node = validator.rb(block_hash, time_of_validation)
            nodes.append(val_node)
        correct_validation = self.validate(block_index, validating=False)
        if correct_validation:
            for ran_node in nodes:
                if ran_node["pub_key"] == public_key:
                    if not self.chain[-1][0]:
                        self.chain[block_index][-1] = [True, time_of_validation, public_key]

    def send_blockchain(self):
        return str(self.chain).replace(" ", "")


class CustomUnpickler(pickle.Unpickler):

    def find_class(self, module, name):
        if name == 'Blockchain':
            return Blockchain
        return super().find_class(module, name)


def write_blockchain(blockchain):
    with open("./info/Blockchain.pickle", "wb") as file:
        pickle.dump(blockchain, file)


def read_blockchain():
    with open("./info/Blockchain.pickle", "rb") as file:
        return CustomUnpickler(file).load()


def read_nodes():
    with open("./info/Nodes.pickle", "rb") as file:
        return CustomUnpickler(file).load()


def validate_blockchain(block_index, ip, time):
    chain = read_blockchain()
    nodes = pickle.load("./info/Nodes.pickle")
    for node in nodes:
        if node[1] == ip:
            wallet = node[2]
            break
    chain.block_valid(block_index, wallet, time)
    write_blockchain(chain)


def invalid_blockchain(block_index, transaction_index, ip):
    chain = read_blockchain()
    chain.invalid_trans(block_index, transaction_index, ip)
    write_blockchain(chain)


def key_tester():
    priv, hex_priv = priv_key_gen()
    pub, hex_pub = pub_key_gen(priv)
    cur_time = 2
    sig1 = sign_trans(priv, str(cur_time))
    sig2 = sign_trans(priv, str(cur_time))
    print(sig1, sig2)
    print(hex_priv, hex_pub, sig1.hex(), cur_time)
    public_key = VerifyingKey.from_string(bytes.fromhex(hex_pub), curve=SECP112r2)
    try:
        assert public_key.verify(bytes.fromhex(sig1.hex()), str(cur_time).encode())
        assert public_key.verify(bytes.fromhex(sig2.hex()), str(cur_time).encode())
        print("complete")
    except:
        print("LLLLL")


def test_transaction(priv_key, reciever, amount):
    priv = SigningKey.from_string(bytes.fromhex(priv_key), curve=SECP112r2)
    pub, hex_pub = pub_key_gen(priv)
    trans = [str(time.time()), str(hex_pub), reciever, str(amount)]
    trans_str = " ".join(trans)
    sig = priv.sign(trans_str.encode()).hex()
    trans.append(sig)
    return trans


def tester(main_prv, main_pub):
    while True:
        time.sleep(1)
        path1 = bool(random.randint(0, 1))
        if path1:
            priv, hex_priv = priv_key_gen()
            pub, hex_pub = pub_key_gen(priv)
            amount = random.randint(100, 1000)
            with open("./testing_keys.txt", "a") as file:
                file.write(f"{hex_priv} {hex_pub} {amount}\n")
            trans = test_transaction(main_prv, hex_pub, amount)
            node.send_to_all(f"TRANS {trans[0]} {trans[1]} {trans[2]} {trans[3]} {trans[4]}")
        else:
            with open("./testing_keys.txt", "r") as file:
                test_keys = file.read().split("\n")
            wallet = random.choices(test_keys)
            wallet = wallet.split(" ")
            trans = test_transaction(wallet[0], main_pub, 25.0)
            node.send_to_all(f"TRANS {trans[0]} {trans[1]} {trans[2]} {trans[3]} {trans[4]}")


if __name__ == "__main__":
    # trans = test_transaction("", "da886ae3ec4c355170586317fed0102854f2b9705f58772415577265", 100)
    # print(trans)
    # key_tester()
    # CHAIN = Blockchain()
    # print("hash: ", CHAIN.hash_block(1))
    # write_blockchain(CHAIN)
    # print(read_blockchain().send_blockchain())
    pass
