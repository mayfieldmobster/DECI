import objsize



class TestERROR(Exception):
    pass

num = input(">>>")
if int(num) < 5:
    raise TestERROR("num is less than 5")