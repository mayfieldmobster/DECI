def exchange_cost(amount):
    start_val = 0.0037*0
    new_val = start_val + amount*0.0037
    total_val = start_val + new_val
    avg_val = total_val/2.0
    cost = avg_val*amount
    return cost, start_val, new_val

#raise ValueError('A very specific bad thing happened.')
#print(exchange_cost(270270))



with open("recent_messages.txt", "r") as file:
    lines = file.read().splitlines()
    del lines[0]
    print(lines)

with open("recent_messages.txt", "w") as file:
    for line in lines:
        if '127.0.0.1 OPT_REQ fuck you' != line:
            file.write("\n"+ line)