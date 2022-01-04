import Blockchain
import node
import time
import ast
from ecdsa import SigningKey, VerifyingKey, SECP112r2



def read():
    transactions = []
    time.sleep(5)
    while True:
        time.sleep(0.01)
        Trans_lines = node.request_reader("TRANS")
        if Trans_lines:
            for line in Trans_lines:
                line = line.split(" ")
                trans = ast.literal_eval(line[2])
                trans_no_sig = []
                for value in trans:
                    trans_no_sig.append(value)
                del trans_no_sig[4]  # left with trans without sig
                trans_no_sig = " ".join(trans_no_sig)
                public_key = VerifyingKey.from_string(bytes.formathex(trans[1]), curve=SECP112r2)
                try:
                    sig_cor = public_key.verify(bytes.fromhex(trans[4]), trans_no_sig.encode())
                except ValueError:
                    sig_cor = False
                if sig_cor:
                    if float(trans[0]) < (time.time()-30.0):
                        if not float(trans[0]) > time.time():
                            transactions.append(trans)

        if len(transactions) >= 50:
            transactions = sorted(transactions, key=lambda transactions: float(transactions[0]))
            for trans in transactions:
                Blockchain.add_transaction(trans)
                time.sleep(3)
