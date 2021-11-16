import pickle

with open("../info/Test_Trans.pickle", "rb") as file:
    Block = pickle.load(file)

    for transaction in Block:
        transaction[3] = str(transaction[3])

    with open("../info/Nodes.pickle", "wb") as file:
        pickle.dump([[0,"192.168.68.112","7fd8a5ba6916444357da92a5648e757af6ace943c05894ea53f7967f"]], file)