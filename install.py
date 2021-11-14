import os
import node

"""
install dependencies
create folders
request nodes and blockchain with
ask for wallet to use and how much to stake
annonounce self and time of creation
"""

os.system("pip3 install tensorflow")
os.system("pip3 install ecdsa")
os.system("pip install art")
from art import *
tprint("D  E  C  E  N  T")

print("\nBy Using our product you except our Terms and Conditions")
input = input("To Accept type 'ACCEPT'  : ")
if input != "ACCEPT":
    exit()





pub_key = input("public_key: ")
with open("Public_key.txt", "w") as file:
    file.write(pub_key)