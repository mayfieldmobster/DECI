import pickle

with open("../info/Blockchain.pickle", "rb") as file:
    Blockchain = pickle.load(file)
    del Blockchain[-1]
    del Blockchain[0][-1]
    del Blockchain[0][-1]
with open("../info/Blockchain.pickle", "wb") as file:
    pickle.dump(Blockchain,file)