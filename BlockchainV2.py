import pickle
import itertools
import hashlib
from ecdsa import SigningKey, VerifyingKey, SECP112r2
import node
import time
from ecdsa.util import randrange_from_seed__trytryagain
import os
import validator
import copy

class Blockchain:

    def __init__(self):
        self.chain = [[["0"], {"time":"0", "sender":"0", "receiver":"8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033", "amount":str(2^25), "sig": "0"}]]

    def update(self, prev_chain):
        self.chain = prev_chain

    def hash_block(self,block):
        for val in block:
            if isinstance(val, dict):
                val = list(val.values())
        block = list(itertools.chain.from_iterable(block))
        print(block)
        str_data = " ".join(block)
        hashed = hashlib.sha256(str_data.encode())
        hex_hashed = hashed.hexdigest()
        return hex_hashed


    def wallet_value(self, wallet_address):
        value = 0.0
        for block in self.chain:
            for trans in block:
                if isinstance(trans,dict):
                    if trans["sender"] == wallet_address:
                        value -= float(trans["amount"])
                    if trans["receiver"] == wallet_address:
                        value += float(trans["amount"])
                        value -= (float(trans["amount"]) * 0.01)

            if block[-1][0]:
                if block[-1][2] == wallet_address:
                    value += block[-2][0]
        return value



    def add_transaction(self,trans):

        relative_time = int(float(self.chain[-1][1]["time"]) - float(trans["time"]))
        prev_relative_time = int(float(self.chain[-2][1]["time"]) - float(trans["time"]))

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
                        
                        self.chain[-2][-3] = [self.hash_block(temp_block),trans["time"]]
                        self.chain[-2][-2][0] +=  (trans["amount"] * 0.01)
                        self.chain[-2][-1][1] = trans["time"]

        elif relative_time > 900:
            b_time = self.chain[-1][-1]["time"]
            block_hash = self.hash(self.chain[-1])
            trans_fees = 0
            for b_trans in self.chain[-1]:
                if isinstance(b_trans,dict):
                    trans_fees += b_trans["amount"] * 0.01

            block = copy.copy(self.chain[-1])
            block = sorted(block[1:], key=lambda block:float(block["time"]))
            self.chain[-1] = block.insert(0,self.chain[-1][0])

            self.chain[-1].append([block_hash,b_time])
            self.chain[-1].append([trans_fees])
            self.chain[-1].append([False, b_time])

            new_block = [[block_hash], trans]
            self.chain.append(new_block)


    def validate(self, block_index, time_of_validation, validator=True):
        transindex= 0
        for trans in self.chain[block_index]:
            if isinstance(trans, dict):
                trans_no_sig = copy.copy(trans)
                trans_no_sig.pop()
                trans_no_sig = " ".join(trans_no_sig)
                public_key = VerifyingKey.from_string(bytes.formathex(trans["sender"]), curve=SECP112r2)

            try:
                assert public_key.verify(bytes.fromhex(trans["sig"]), trans_no_sig.encode())

                if self.wallet_value(trans["sender"]) < float(trans["amount"]):
                    raise ValueError("sender does not have ")

            except:
                if validator:
                    message = ["TRANS_INVALID", str(block_index), str(transindex)]
                    message = " ".join(message)
                    node.send_to_all(message)

            transindex += 1

        if validator:
            node.send_to_all("VALID " + str(block_index) + " " + str(time_of_validation))

        if not validator:
            return True

    def invalid_trans(self, block_index, trans_index):
        block_index = int(block_index)
        trans_index = int(trans_index)

        trans = self.chain[block_index][trans_index]
        trans_no_sig = copy.copy(trans)
        trans_no_sig.pop()
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
            pre_hashed_blocks = copy.copy(self.chain[block_index:])
            block_hashes = []

            for block in pre_hashed_blocks:
                block.pop()
                block.pop()
                block.pop()
                block_hashes.append(self.hash_block(block))#calculates hash from wrong previous hash

            for i in range(len(self.chain) - block_index):  # update hashes
                self.chain[block_index + i][-3][0] = block_hashes[i]
                self.chain[block_index + i + 1][0] = [block_hashes][i]
















