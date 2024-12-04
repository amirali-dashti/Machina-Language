from dfa_data import DFA
import ast


def commandCall(entry, command):
    if command in entry:
        return True
    else:
        return False
    
def moveRight(entry, command):
    if not isinstance(entry, str) or not isinstance(command, str):
        raise ValueError("Both entry and command must be strings.")

    if command == "":
        return entry  # Returning entry unchanged if command is empty

    return entry.replace(command, "")

def readEqual(entry):
    for i in entry:
        if i == " " or i == "=":
            entry = moveRight(entry, i)
        else:
            return entry
        
def qPrint(entry):
    if ".states" in entry:
        print(dfa.states)

def changeState(entry):
    result = entry.split("/")
    stateName, start, final = result
    dfa.add_state(stateName, start, final)

def que(entry):
    if ".len" in entry:
        end_of_range = int(readEqual(moveRight(entry, ".len")))
        for i in range(1, end_of_range + 1):
            if i == 1:
                dfa.add_state(f"q{i}", True, False)
            elif i == end_of_range:
                dfa.add_state(f"q{i}", False, True)
            else:
                dfa.add_state(f"q{i}", False, False)
    if ".print" in entry:
            qPrint(moveRight(entry, ".len"))
    if ".changestate." in entry:
            changeState(moveRight(entry, ".changestate."))

def navigator(entry):
    if commandCall(entry, "Q"):
        que(moveRight(entry, "Q"))
        
dfa = DFA()

def compiler(code):
    lineCount = 0
    for line in code.splitlines():
        navigator(line)
        lineCount += 1
        
        
example = """
Q.len = 5
Q.print.states
Q.changestate.q1/False/False
Q.print.states
"""
compiler(example)