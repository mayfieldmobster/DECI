import node
import time
from ecdsa import VerifyingKey, SECP112r2
import copy
import pickle
import blockchain


def read():
    time.sleep(60)
    print("---TRANSACTION READER STARTED---")
    while True:
        Trans_lines = node.request_reader("TRANS")
        if Trans_lines:
            for line in Trans_lines:
                print(line)
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
                chain = blockchain.read_blockchain()
                if trans in chain[-1] or trans in chain[-2]:
                    continue

                if float(trans["time"]) > (time.time() - 30.0):  # was announced in the last 30 seconds
                    if not float(trans["time"]) > time.time():  # not from the future
                        chain.add_transaction(trans)
