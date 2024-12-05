import pandas as pd

def ripper(table, i, rip, j):
    print(f"LOG: covering {i}, {rip}, and {j}")
    R1 = table.iloc[i, rip]
    R2 = table.iloc[rip, rip]
    R3 = table.iloc[rip, j]
    R4 = table.iloc[i, j]
    outcome = f"{R1}({R2})*{R3}U{R4}"
    print(outcome)
    
    table.iloc[i, j] = outcome
    
    table.drop(index=rip, columns=rip, inplace=True)
    print(table)

def gtor(table):
    state_len = table.shape[0]
    for k in range(1, state_len - 1):
        rip = state_len - k - 1
        i = rip - 1
        j = rip + 1
        ripper(table, i, rip, j)