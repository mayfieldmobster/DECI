def exchange_cost(amount):
    start_val = 0.0037*10000
    new_val = start_val - amount*0.0037
    total_val = start_val + new_val
    avg_val = total_val/2.0
    cost = avg_val*amount
    return cost, start_val, new_val

print(exchange_cost(100.0))