def exchange_cost(amount):
    start_val = 0.0037*0
    new_val = start_val + amount*0.0037
    total_val = start_val + new_val
    avg_val = total_val/2.0
    cost = avg_val*amount
    return cost, start_val, new_val

#raise ValueError('A very specific bad thing happened.')
#print(exchange_cost(270270))


import time
def test():
    for i in range(100):
        print(i)
        time.sleep(1)

#test()

import socket
def send(host, message):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, 1379))
        client.send(message.encode("utf-8"))
    except:
        return "node offline"

#send("127.0.0.1", "TRANS "+str(['1635081552.1908393','b82afe0396e554f32fb8dedbb41f8e294a44184a1b709daf4b9224b9','c18ba0025f7fa9b31ff83a203e7b14dd8ec3a6cb023864f7a70fd94e','321','206df1c0ea8983c82352287f0bb62295d5b66101cf1b02237a3bb84e']).replace(" ",""))


import DECI.run

DECI.run.tes()







