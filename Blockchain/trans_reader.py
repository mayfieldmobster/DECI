import node
import time
from ecdsa import VerifyingKey, SECP112r2
import copy
import pickle
import blockchain
import ast
import requests

def AI_handler():
    pass

def trans_handler(line):
    #print(line)
    line = line.split(" ")
    trans = {"time": line[2], "sender": line[3], "receiver": line[4], "amount": line[5], "sig": line[6]}
    trans_no_sig = copy.copy(trans)
    trans_no_sig.pop("sig")  # left with trans without sig
    trans_no_sig = " ".join(list(trans_no_sig.values()))
    public_key = VerifyingKey.from_string(bytes.fromhex(trans["sender"]), curve=SECP112r2)
    if not public_key.verify(bytes.fromhex(trans["sig"]), trans_no_sig.encode()):
        return
    chain = blockchain.read_blockchain()
    if trans in chain[-1] or trans in chain[-2]:
        return

    if float(trans["time"]) > (time.time() - 20.0):  # was announced in the last 30 seconds
        if not float(trans["time"]) > time.time():  # not from the future
            chain.add_transaction(trans)
            blockchain.write_blockchain(chain)

def AI_job_handler(line):
    line = line.split(" ")
    nodes = ast.literal_eval(line[3])
    nodes_info = []
    for AI_node in nodes:
        nodes_info.append({"ip": AI_node["ip"], "wallet": AI_node["pub_key"], "work_done": 0.0})  #  announce work done to update later
    job_announce = {"time": float(line[2]), "script_identity": float(line[4]), "nodes": nodes_info}
    r = requests.get(f"https://decint.com/si/{line[4]}")
    if r.status_code == 404:
        return
    chain = blockchain.read_blockchain()
    if job_announce in chain[-1] or job_announce in chain[-2]:
        return
    if job_announce["time"] > (time.time() - 20.0):  # was announced in the last 30 seconds
        if not job_announce["time"] > time.time():  # not from the future
            chain.add_protocol(job_announce)
            blockchain.write_blockchain(chain)

def staking_handler(line):
    line = line.split(" ")
    if "STAKE" == line[1]:
        stake_trans = {"time": float(line[2]), "pub_key": line[2], "stake_amount": line[3], "sig": line[4]}
    elif "UNSTAKE" == line[1]:
        stake_trans = {"time": float(line[2]), "pub_key": line[2], "unstake_amount": line[3], "sig": line[4]}
    public_key = VerifyingKey.from_string(bytes.fromhex(line["sender"]), curve=SECP112r2)
    if not public_key.verify(bytes.fromhex(line[4]), line[2].encode()):
        return
    chain = blockchain.read_blockchain()
    if stake_trans in chain[-1] or stake_trans in chain[-2]:
        return
    if stake_trans["time"] > (time.time()-20.0):
        if not stake_trans["time"] > time.time():
            chain.add_protocol(stake_trans)
            blockchain.write_blockchain(chain)
            with open("./info/stake_trans.pickle", "rb") as f:
                stake_transactions = pickle.load(f)
            stake_transactions.append(stake_trans)
            with open("./info/stake_trans.pickle", "wb") as f:
                pickle.dump(stake_transactions,f)


def read():
    time.sleep(60)
    print("---TRANSACTION READER STARTED---")
    while True:
        trans_lines = node.dist_request_reader("TRANS")
        if trans_lines:
            for trans_line in trans_lines:
                if "TRANS" in trans_line:
                    trans_handler(trans_line)
                    #  TODO add trans error handler
                elif "AI_JOB" in trans_line:
                    AI_job_handler(trans_line)
                elif "STAKE" in trans_line or "UNSTAKE" in trans_line:
                    staking_handler(trans_line)
