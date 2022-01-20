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

#with open("./text.zip", "wb") as file:
    #file.write(bytes.fromhex("00" + binar))

"""
import glob
import os

os.chdir(".")
names={}
for fn in glob.glob('*.py'):
    with open(fn) as f:
        names[fn]=sum(1 for line in f if line.strip() and not line.startswith('#'))

print(sum(names.values()))
"""
import objsize
import ast

data = ast.literal_eval("[[['0'], {'time': '0', 'sender': '0', 'receiver': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'amount': '26', 'sig': '0'}, {'time': '10', 'sender': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'receiver': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'amount': '27', 'sig': 'asfsdfgshdfhfsffs2'}, {'time': '11', 'sender': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'receiver': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'amount': '27', 'sig': 'asfsdfgshdfhfsffs2'}, {'time': '12', 'sender': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'receiver': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'amount': '27', 'sig': 'asfsdfgshdfhfsffs2'}, {'time': '13', 'sender': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'receiver': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'amount': '27', 'sig': 'asfsdfgshdfhfsffs2'}, {'time': '14', 'sender': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'receiver': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'amount': '27', 'sig': 'asfsdfgshdfhfsffs2'}, {'time': '14', 'sender': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'receiver': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'amount': '27', 'sig': 'asfsdfgshdfhfsffs2'}, {'time': '14', 'sender': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'receiver': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'amount': '27', 'sig': 'asfsdfgshdfhfsffs2'}, {'time': '14', 'sender': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'receiver': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'amount': '27', 'sig': 'asfsdfgshdfhfsffs2'}, {'time': '14', 'sender': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'receiver': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'amount': '27', 'sig': 'asfsdfgshdfhfsffs2'}, {'time': '14', 'sender': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'receiver': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'amount': '27', 'sig': 'asfsdfgshdfhfsffs2'}, {'time': '14', 'sender': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'receiver': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'amount': '27', 'sig': 'asfsdfgshdfhfsffs2'}, {'time': '14', 'sender': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'receiver': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'amount': '27', 'sig': 'asfsdfgshdfhfsffs2'}, {'time': '14', 'sender': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'receiver': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'amount': '27', 'sig': 'asfsdfgshdfhfsffs2'}, {'time': '14', 'sender': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'receiver': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'amount': '27', 'sig': 'asfsdfgshdfhfsffs2'}, {'time': '14', 'sender': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'receiver': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'amount': '27', 'sig': 'asfsdfgshdfhfsffs2'}, {'time': '14', 'sender': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'receiver': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'amount': '27', 'sig': 'asfsdfgshdfhfsffs2'}, {'time': '14', 'sender': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'receiver': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'amount': '27', 'sig': 'asfsdfgshdfhfsffs2'}, {'time': '14', 'sender': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'receiver': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'amount': '27', 'sig': 'asfsdfgshdfhfsffs2'}, {'time': '14', 'sender': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'receiver': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'amount': '27', 'sig': 'asfsdfgshdfhfsffs2'}, {'time': '14', 'sender': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'receiver': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'amount': '27', 'sig': 'asfsdfgshdfhfsffs2'}, {'time': '14', 'sender': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'receiver': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'amount': '27', 'sig': 'asfsdfgshdfhfsffs2'}, {'time': '14', 'sender': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'receiver': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'amount': '27', 'sig': 'asfsdfgshdfhfsffs2'}, {'time': '14', 'sender': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'receiver': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'amount': '27', 'sig': 'asfsdfgshdfhfsffs2'}, {'time': '14', 'sender': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'receiver': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'amount': '27', 'sig': 'asfsdfgshdfhfsffs2'}, {'time': '14', 'sender': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'receiver': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'amount': '27', 'sig': 'asfsdfgshdfhfsffs2'}, {'time': '14', 'sender': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'receiver': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'amount': '27', 'sig': 'asfsdfgshdfhfsffs2'}, {'time': '14', 'sender': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'receiver': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'amount': '27', 'sig': 'asfsdfgshdfhfsffs2'}, {'time': '14', 'sender': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'receiver': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'amount': '27', 'sig': 'asfsdfgshdfhfsffs2'}, {'time': '14', 'sender': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'receiver': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'amount': '27', 'sig': 'asfsdfgshdfhfsffs2'}, {'time': '14', 'sender': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'receiver': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'amount': '27', 'sig': 'asfsdfgshdfhfsffs2'}, {'time': '14', 'sender': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'receiver': '8668373f064764cf4e917756903e606874b0d94bb1e6ea1ab7e75033', 'amount': '27', 'sig': 'asfsdfgshdfhfsffs2'}]]".replace(" ",""))

print(data[0][1]["receiver"])