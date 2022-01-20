from AI import Blockchain
from blockchain import node
import time
from ecdsa import VerifyingKey, SECP112r2
import copy
import pickle


def read():
    transactions = []
    time.sleep(5)
    while True:
        Trans_lines = node.request_reader("TRANS")
        if Trans_lines:
            for line in Trans_lines:
                line = line.split(" ")
                trans = {"time": line[2], "sender": line[3], "receiver": line[4], "amount": line[5], "sig": line[6]}
                trans_no_sig = copy.copy(trans)
                trans_no_sig.pop("sig")  # left with trans without sig

                trans_no_sig = " ".join(trans_no_sig)
                public_key = VerifyingKey.from_string(bytes.formathex(trans["sender"]), curve=SECP112r2)
                try:
                    sig_cor = public_key.verify(bytes.fromhex(trans["sig"]), trans_no_sig.encode())
                except:
                    continue
                with open("../info/Blockchain.pickle", "rb") as file:
                    blockchain = pickle.load(file)
                    blockchain = blockchain
                if trans in blockchain[-1] or trans in blockchain[-2]:
                    continue

                if float(trans["time"]) > (time.time() - 30.0):  # was announced in the last 30 seconds
                    if not float(trans["time"]) > time.time():  # not from the future
                        Blockchain.add_transaction(trans)
