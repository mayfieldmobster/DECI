import node
import socket
import codecs
def send(host, message):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, 1379))
        client.send(message.encode("utf-8"))
    except:
        return "node offline"

#send("127.0.0.1", "TRANS "+str(['1635081552.1908393','b82afe0396e554f32fb8dedbb41f8e294a44184a1b709daf4b9224b9','c18ba0025f7fa9b31ff83a203e7b14dd8ec3a6cb023864f7a70fd94e','321','206df1c0ea8983c82352287f0bb62295d5b66101cf1b02237a3bb84e']).replace(" ",""))


#open("recent_messages.txt", "w").close()

#lines = node.request_reader("DEP")

#print("L:",lines[0])

"""
with open("./DECI/text.zip", "rb") as file:
    binar = file.read().hex()
    print(binar)
    print(type(binar))
    print(bytes.fromhex(binar))
    print(type(bytes.fromhex(binar)))
    
"""
#with open("./text.zip", "wb") as file:
    #file.write(bytes.fromhex("00" + binar))

"""
num = "054365"

if str(type(len(num) / 2)) == "<class 'float'>":
    print("odd")

else:
    print("even")

print(len(num)/2)
print(str(type(len(num) / 2)))
"""



def hello():
    print("hello")

hello(3)
