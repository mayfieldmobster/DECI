def exchange_cost(amount):
    start_val = 0.0037*0
    new_val = start_val + amount*0.0037
    total_val = start_val + new_val
    avg_val = total_val/2.0
    cost = avg_val*amount
    return cost, start_val, new_val

#raise ValueError('A very specific bad thing happened.')
#print(exchange_cost(270270))


