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


print("\nBy Using our product you except our Terms and Conditions")
input = input("To Accept type 'ACCEPT'  : ")
if input != "ACCEPT":
    exit()

print("This is the the key that will be rewarded")
pub_key = input("Public Key: ")
print("Bellow insert Port that will be forwarded for communication (Leave Blank to Default)")
norm_port = input("Port: ")
print("Bellow insert another port that you will have to forwarded (Leave Blank to Default)")
ai_port = input("Port: ")

with open("./info/Public_key.txt", "w") as file:
    file.write(pub_key)

with open("./info/ports.txt", "w") as file:
    file.write(norm_port + "\n" + ai_port)

print("Thats you,\n"
      "make sure you are port forwarding BOTH PORTS!!!,\n"
      "run DECI.exe to start,\n"
      "if you want to change anything run this again.\n")