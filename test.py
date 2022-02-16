import objsize#
import ast

arr = '[{"home":1, "people": 5},{"home":3, "people": 4},eval(print("hello"))]'

print(ast.literal_eval(arr))