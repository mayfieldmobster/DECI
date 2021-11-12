import pickle

with open("../info/Test_Trans.pickle", "rb") as file:
    Block = pickle.load(file)

    for transaction in Block:
        transaction[3] = str(transaction[3])

    with open("../info/Blockchain.pickle", "wb") as file:
        pickle.dump([[["0"]]], file)