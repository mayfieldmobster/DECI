import AI
import node
import pickle

def distributor(epochs, data_size, num_params):
    total_size = data_size*epochs
    with open("./info/Nodes.pickle", "rb") as file:
        nodes = pickle.load(file)
    
    pass
