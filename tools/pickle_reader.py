import pickle
import numpy as np
from ecdsa import SigningKey, VerifyingKey, SECP112r2
import itertools

"""
with open("../info/Test_Trans.pickle", "rb") as file:
    Transactions = pickle.load(file)
    print(str(Transactions).replace(" ",""))
    print(type(Transactions))
    print(type(str(Transactions)))

    for transaction in Transactions:
        trans_no_sig = []
        trans_no_sig.append(transaction)
        trans_no_sig = list(itertools.chain.from_iterable(trans_no_sig))
        del trans_no_sig[4]
        print(transaction)
        trans_no_sig = " ".join(trans_no_sig)
        public_key = VerifyingKey.from_string(bytes.fromhex(transaction[1]), curve=SECP112r2)
        #print(bytes.fromhex(transaction[4]), trans_no_sig.encode())
        try:

            assert public_key.verify(bytes.fromhex(transaction[4]), trans_no_sig.encode())
            print("yh")
        except:
            print("WTF")
"""


with open("../DIST_NODE/info/Nodes.pickle", "rb") as file:
    Nodes = pickle.load(file)
    print(Nodes)

