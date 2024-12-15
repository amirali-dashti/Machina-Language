import pandas as pd
import re


# STABLE ____________________________________________________________________________________________________________________
# List of regex patterns to clean
regexes = [
    r"\(\)",  # Matches empty parentheses "()"
    r"()",    # Matches empty parentheses "()"
    r"n"      # Matches the character 'n'
]

def gP(entry):
    if len(entry) > 1:
        entry = f"({entry})"
    return entry

def dataCleaning(entry):
    # Apply all regexes to remove unwanted parts
    cleared_text = entry
    for regex in regexes:
        cleared_text = re.sub(regex, '', cleared_text)  # Apply regex replacement
    
    cleared_text = cleared_text.replace("UU", "U")
    cleared_text = cleared_text.replace("**", "*")
    
    # Remove the first character if it starts with 'e', 'U', or 'e*'
    if cleared_text.startswith(("e", "U")):
        cleared_text = cleared_text[1:]
    
    if cleared_text.startswith("e*"):
        cleared_text = cleared_text[2:]

    # Remove the last character if it ends with 'e', 'U', or '*e'
    if cleared_text.endswith(("e", "U")):
        cleared_text = cleared_text[:-1]
        
    if cleared_text.endswith("*e"):
        cleared_text = cleared_text[:-1]

    
    
    return cleared_text

def gtor(table):
    counter = 1
    while table.shape[0] > 2:
        states = list(table.index)
        rip = states[-2]
        print("-------NEW qrip-------")
        print(f"qrip = q{rip}")
        incoming = [i for i in range(len(states)) if table.iloc[i, rip] != 'n']
        print(f"q{incoming} -----> q{rip}")
        outgoing = [j for j in range(len(states)) if table.iloc[rip, j] != 'n']
        print(f"q{rip} -----> q{outgoing}")

        for i in incoming:
            for j in outgoing:
                if i != rip and j != rip and table.iloc[i, rip] != 'n' and table.iloc[rip, j] != 'n':
                    # Only process if transitions exist
                    R1 = gP(table.iloc[i, rip].replace("n", ""))
                    R2 = gP(table.iloc[rip, rip].replace("n", ""))
                    R3 = gP(table.iloc[rip, j].replace("n", ""))
                    R4 = gP(table.iloc[i, j].replace("n", ""))
                    print(f"-----------Step {counter}-----------")
                    counter += 1
                    if R1 != "":
                        print(f"COLLECTING: q{i} ----{R1}----> q{rip}")
                    if R2 != "":
                        print(f"COLLECTING: q{rip} <----{R2}----> q{rip}")
                    if R3 != "":
                        print(f"COLLECTING: q{rip} ----{R3}----> q{j}")
                    if R4 != "":
                        print(f"COLLECTING: q{i} ----{R4}----> q{j}")

                    result = dataCleaning(f"{R1}{R2}*{R3}U{R4}" if R2 != "n" else f"{R1}{R3}U{R4}")
                    table.iloc[i, j] = result if table.iloc[i, j] == "n" else f"{table.iloc[i, j]}U{result}"
                    print(f"AFTER RIPPING: q{i} ----{table.iloc[i, j]}----> q{j}")

        # Drop the row and column for the 'rip' state
        table.drop(index=rip, columns=rip, inplace=True)
        print(f"q{rip} got removed. Here's the new table:")
        print(table)
        
    # Output final result
    for _, row in table.iterrows():
        for col in table.columns:
            value = row[col]
            if value != "n":
                print("The final Regular Expression is:")
                print(value)
                
                
                
# ------------------BETA------------------------
def navigator(nav_dict, table, i, j):
    if table.iloc[i, j] != "n":
        nav_dict[(i, j)] = [[[[[i, j], table.iloc[i, j]]]]]
    for rip in range(i, j):
        if table.iloc[rip, rip] != "n":
            nav_dict[(i, j)] = [[[[[i, j], table.iloc[rip, rip]]]]]
test = '''        if (i, rip) in nav_dict:
            second_way.append([[i, j], nav_dict[(i, rip)]])
            if (rip, rip) in nav_dict:
                second_way.append([[i, j], nav_dict[(rip, rip)]])
            if (rip, j) in nav_dict:
                second_way.append([[i, j], nav_dict[(rip, j)]])
                
        if second_way != []:
            if (i, j) in nav_dict:
                nav_dict[(i, j)].append(second_way)
            else:
                nav_dict[(i, j)] = [second_way]'''

def gtorBETA(table):
    nav_dict = dict()
    counter = 1
    states = list(table.index)
    for i in states:
        for j in states:
            navigator(nav_dict, table, i, j)

    for points, addresses in nav_dict.items():
        print(f"for {points}, we have this/these way/s:")
        for ways in addresses:
            for way in ways:
                for step in way:
                    street_points = step[0]
                    street = step[1]
                    print(f"We pass throught {street_points[0]} to {street_points[1]} with {street}")
                print("then")