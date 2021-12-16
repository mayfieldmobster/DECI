import Blockchain
import node
import time
import ast



def read():
    transactions = []
    _ = []
    while True:
        time.sleep(0.01)
        Trans_lines = node.request_reader("TRANS")
        if Trans_lines != _ :
            for line in Trans_lines:
                line = line.split(" ")
                trans = ast.literal_eval(line[2])
                if trans[0] < (time.time()-20-0):
                    transactions.append(trans)

        if len(transactions) >= 50:
            transactions = sorted(transactions, key=lambda transactions: transactions[0])
            for trans in transactions:
                Blockchain.add_transaction(trans)
                time.sleep(3)
