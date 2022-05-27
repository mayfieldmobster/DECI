import objsize#
import ast
import random
import time

arr1 = [1,2,3]
arr2 = [4,5,6]
arr3 = arr1 + arr2
for i in arr3:
    if i%2 == 0:
        del i

print(arr3)