import random
import pickle
import Blockchain


with open("./info/Test_Trans.pickle", "rb") as file:
    Block = pickle.load(file)

hash = int(Blockchain.hash_block(Block), 16)
print(hash)

random.seed(hash)

print(random.randint(0,12345))


