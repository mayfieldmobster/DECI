import pickle
import blockchain

def updator():
    print("---STAKE UPDATOR STARTED---")
    STAKE_WALLET = "4aa5f462171c2c71129d6064b5c986a9a0610ff4afb1f90b13f4e29e"
    while True:
        chain = blockchain.read_blockchain()

        with open("../info/stake_trans.pickle", "rb") as file:
            stake_trans = pickle.load(file)

        for block in chain:
            if block[-1][0]:
                for trans in block[1:-3]:
                    if trans["sender"] == STAKE_WALLET or trans["receiver"] == STAKE_WALLET:
                        if trans not in stake_trans:
                            stake_trans.append(trans)

        with open("../info/stake_trans.pickle", "wb") as file:
            pickle.dump(stake_trans, file)



