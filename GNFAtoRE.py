import pandas as pd

def ripper(table, i, rip, j):
    R1 = table.iloc[i, rip]
    R2 = table.iloc[rip, rip]
    R3 = table.iloc[rip, j]
    R4 = table.iloc[i, j]
    outcome = f"{R1}({R2})*{R3}U{R4}"
    
    table.iloc[i, j] = outcome
    
    # Drop the row and column for the 'rip' state.
    table.drop(index=table.index[rip], columns=table.columns[rip], inplace=True)
    print(table)

def gtorOLD(table):
    while table.shape[0] > 2:
        # Get the current valid states list
        states = list(table.index)
        rip = states[-2]  # Rip the second-last state to avoid start or final states
        
        incoming = [i for i in range(len(states)) if table.iloc[i, rip] != 'n']
        outgoing = [j for j in range(len(states)) if table.iloc[rip, j] != 'n']
        
        for i in incoming:
            for j in outgoing:
                if i != rip and j != rip:
                    ripper(table, i, rip, j)

    # Print the final regular expression result from the start to the final state.
    for _, row in table.iterrows():
        for col in table.columns:
            value = row[col]
            if value != "n":
                print("The translation result from GNFA to Regular Expression:")
                print(f"{value}")


def gtor(table):
    while table.shape[0] > 2:
        states = list(table.index)
        rip = states[-2]  # Choose second last state
        incoming = [i for i in range(len(states)) if table.iloc[i, rip] != 'n']
        outgoing = [j for j in range(len(states)) if table.iloc[rip, j] != 'n']

        for i in incoming:
            for j in outgoing:
                if i != rip and j != rip:
                    R1 = table.iloc[i, rip]
                    R2 = table.iloc[rip, rip]
                    R3 = table.iloc[rip, j]
                    R4 = table.iloc[i, j]
                    result = f"{R1}({R2})*{R3}U{R4}" if R2 != "n" else f"{R1}{R3}U{R4}"
                    table.iloc[i, j] = result if table.iloc[i, j] == "n" else f"{table.iloc[i, j]}U{result}"

            # Drop the row and column for the 'rip' state
        table.drop(index=rip, columns=rip, inplace=True)

        # Output final result
    for _, row in table.iterrows():
        for col in table.columns:
            value = row[col]
            if value != "n":
                print("The final Regular Expression is:")
                print(value)