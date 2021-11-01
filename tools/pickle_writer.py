import pickle

with open("../info/Test_Trans.pickle", "rb") as file:
    Block = pickle.load(file)

    for transaction in Block:
        transaction[3] = str(transaction[3])

    with open("../info/Test_Trans.pickle", "wb") as file:
        block = pickle.dump(Block, file)