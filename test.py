import objsize


import torch
print(torch.cuda.is_available())
class TestERROR(Exception):
    pass

num = input(">>>")
if int(num) < 5:
    raise TestERROR("num is less than 5")