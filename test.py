import pickle
from timeit import default_timer as timer

def scan_block(pub_adrress):
    with open("info/Test_Trans.pickle", "rb") as file:
        block = pickle.load(file)
        blockchain = [block]

    amount_in_wallet = 0.0

    for block in blockchain:
        for transaction in block:
            if transaction[2] == pub_adrress:
                amount_in_wallet += float(transaction[3])
            if transaction[1] == pub_adrress:
                amount_in_wallet -= float(transaction[3])

    return amount_in_wallet

start = timer()
adr_amount = scan_block('c18ba0025f7fa9b31ff83a203e7b14dd8ec3a6cb023864f7a70fd94e')
end = timer()
total_time = end - start
possible_time = total_time*100000

print(adr_amount)
print(total_time)
print(possible_time)










