import itertools
import hashlib
import ast
from ecdsa import SigningKey, VerifyingKey, SECP112r2
import node
from ecdsa.util import randrange_from_seed__trytryagain
import os
import validator
import copy
#from numba import jit
import pickle
import time


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


def hash_block(block):
    for val in block:
        if isinstance(val, dict):
            val = list(val.values())
    block = list(itertools.chain.from_iterable(block))
    print(block)
    str_data = " ".join(block)
    hashed = hashlib.sha256(str_data.encode())
    hex_hashed = hashed.hexdigest()
    return hex_hashed


class Blockchain:

    def __init__(self):
        self.chain = [[["0"], {"time": "0", "sender": "0",
                               "receiver": "8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033",
                               "amount": str(2**23), "sig": "0"}]]

    def __repr__(self):
        return str(self.chain)  # .replace("]", "]\n")

    def print_block(self, block_index):
        return str(self.chain[block_index]).replace("]", "]\n")

    def __len__(self):
        return len(self.chain)

    def __ge__(self, other: int):
        return len(self.chain) >= other

    def __le__(self, other: int):
        return len(self.chain) <= other

    def __gt__(self, other: int):
        return len(self.chain) > other

    def __lt__(self, other: int):
        return len(self.chain) < other

    def __bool__(self):
        print("The Blockchain never lies")
        return True

    def __call__(self):
        return self.chain

    def get_block(self, block_index: int):
        try:
            return self.chain[block_index]
        except Exception as e:
            print(e)

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
        for val in block:
            if isinstance(val, dict):
                val = list(val.values())
        block = list(itertools.chain.from_iterable(block))
        print(block)
        str_data = " ".join(block)
        hashed = hashlib.sha256(str_data.encode())
        hex_hashed = hashed.hexdigest()
        return hex_hashed

    def update(self, prev_chain):
        self.chain = ast.literal_eval(str(prev_chain))

    #@jit(nopython=True)
    def wallet_value(self, wallet_address):
        value = 0.0
        for block in self.chain:
            for trans in block:
                if isinstance(trans, dict):
                    if trans["sender"] == wallet_address:
                        value -= float(trans["amount"])
                    if trans["receiver"] == wallet_address:
                        if block[-1][0]:
                            value += (float(trans["amount"]) * 0.99)

            if block[-1][0]:
                if block[-1][2] == wallet_address:
                    value += block[-2][0] * 0.5

        if wallet_address == "3f41f86b3a3ac977bf03f026273fa353f1f83c0643d805c51d853f61":
            for block in self.chain:
                value += block[-2][0] * 0.5
        return value

    def add_transaction(self, trans: dict):
        relative_time = int(float(trans["time"]) - float(self.chain[-1][1]["time"]))
        # prev_relative_time = int(float(trans["time"]) - float(self.chain[-2][1]["time"]))
        prev_relative_time = 10000

        if relative_time < 900:
            if relative_time < 0:
                if prev_relative_time < 900:
                    if not self.chain[-2][-1][0]:
                        self.chain[-2].append(trans)

                        temp_block = []
                        for val in self.chain:
                            temp_block.append(val)

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
                    trans_fees += b_trans["amount"] * 0.01

            block = copy.copy(self.chain[-1])
            block = sorted(block[1:], key=lambda block: float(block["time"]))
            self.chain[-1] = block.insert(0, self.chain[-1][0])
            self.chain[-1].append([block_hash, b_time])
            self.chain[-1].append([trans_fees])
            self.chain[-1].append([False, b_time])

            new_block = [[block_hash], trans]
            self.chain.append(new_block)

    def validate(self, block_index: int, time_of_validation: float = 0.0, validating: bool = True):
        trans_index = 0
        for trans in self.chain[block_index]:
            if isinstance(trans, dict):
                trans_no_sig = copy.copy(trans)
                trans_no_sig.pop("sig")
                trans_no_sig = " ".join(trans_no_sig)
                public_key = VerifyingKey.from_string(bytes.fromhex(trans["sender"]), curve=SECP112r2)

            try:
                assert public_key.verify(bytes.fromhex(trans["sig"]), trans_no_sig.encode())

                if self.wallet_value(trans["sender"]) < float(trans["amount"]):
                    raise ValueError("sender does not have ")

            except Exception as e:
                if isinstance(e, AssertionError) or isinstance(e, ValueError):
                    if validating:
                        message = f"TRANS_INVALID {block_index} {trans_index}"
                        node.send_to_all(message)
                        self.invalid_trans(block_index, trans_index)

                    if not validating:
                        return False

            trans_index += 1

        if validating:
            node.send_to_all("VALID " + str(block_index) + " " + str(time_of_validation))

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

            if self.wallet_value(trans["sender"]) < float(trans["amount"]):
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
            stake_removal = f"LIAR {node_pub}"
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


def write_blockchain(blockchain):
    with open("info/Blockchain.pickle", "wb") as file:
        pickle.dump(blockchain, file)


def read_blockchain():
    with open("info/Blockchain.pickle", "rb") as file:
        return pickle.load(file)


def read_nodes():
    with open("info/Nodes.pickle", "rb") as file:
        return pickle.load(file)


def validate_blockchain(block_index, ip, time):
    chain = read_blockchain()
    nodes = pickle.load()
    for node in nodes:
        if node[1] == ip:
            wallet = node[2]
            break
    chain.block_valid(block_index, wallet, time)
    write_blockchain(chain)


def invalid_blockchain(block_index, transaction_index):
    chain = read_blockchain()
    chain.invalid_trans(block_index, transaction_index)
    write_blockchain(chain)



def key_tester():
    priv, hex_priv = priv_key_gen()
    pub, hex_pub = pub_key_gen(priv)
    cur_time = time.time()
    sig = sign_trans(priv, str(cur_time))
    print(hex_priv, hex_pub, sig.hex(), cur_time)
    public_key = VerifyingKey.from_string(bytes.fromhex(hex_pub), curve=SECP112r2)
    assert public_key.verify(bytes.fromhex(sig.hex()), str(cur_time).encode())

CHAIN = Blockchain()
write_blockchain(CHAIN)
