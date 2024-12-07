from dfa_data import DFA


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
    if ".tra" in entry:
        print(dfa.transitions)

def changeState(entry):
    result = entry.split(" ")
    stateName, start, final = result[0], result[1] == "True", result[2] == "True"

    state_index = dfa.states.index[dfa.states["Name"] == stateName].tolist()
    
    if state_index:
        state_index = state_index[0]
        dfa.states.at[state_index, "Is_Start"] = start
        dfa.states.at[state_index, "Is_Final"] = final
        if start:
            dfa.start_state = stateName  # Ensure the start state is correctly tracked
        # print(f"State '{stateName}' updated.")
    else:
        # Add new state if it doesn't exist
        dfa.add_state(stateName, start, final)
        print(f"State '{stateName}' added.")


def labelRemove(entry):
    lrlist = entry.split(" ")
    dfa.remove_transition(lrlist[0], lrlist[1], lrlist[2])

def labelChange(entry):
    lclist = entry.split(" ")
    old_start, old_end, old_label, new_label = lclist[:4]
    # Remove the old transition
    dfa.remove_transition(old_start, old_end, old_label)
    # Add the new transition with the new label
    dfa.add_transition(old_start, old_end, new_label)

def labelConfigs(entry):
    if ".remove." in entry:
        labelRemove(moveRight(entry, ".remove."))
    elif ".change." in entry:
        labelChange(moveRight(entry, ".change."))
    elif ".add." in entry:
        eei(moveRight(entry, ".add."))

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
    if ".label" in entry:
            labelConfigs(moveRight(entry, ".label"))
            
def eei(entry):
    eei_list = entry.split(" ")
    
    dfa.add_transition(eei_list[0], eei_list[1], eei_list[2])
    

def translate(entry):
    if ".dfa.gnfa" in entry:
        dfa.dfatable()
    if ".dfa.re" in entry:
        dfa.gtor()
        
        
def generalDos(entry):
    if ".translate" in entry:
        translate(moveRight(entry, "do"))
        
def navigator(entry):
    if commandCall(entry, "Q"):
        que(moveRight(entry, "Q"))
    if commandCall(entry, "do"):
        generalDos(moveRight(entry, "do"))
        
        
        
dfa = DFA()

def compiler(code):
    lines = code.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if "E.{" in line:  # Start of an E block
            i += 1  # Skip to the next line to start processing inside the block
            while i < len(lines) and lines[i] != "}":  # Continue until you find the closing brace
                eei(lines[i])  # Process the line (eei function should be implemented accordingly)
                i += 1  # Move to the next line
        else:
            navigator(line)  # Process non-E block lines
            i += 1  # Move to the next line

        
        
example = """
Q.len = 3
E.{
q1 q2 a
q2 q1 a
q2 q2 b
q1 q3 b
q3 q1 b
q3 q2 a
}
Q.changestate.q2 False True
Q.changestate.q1 True False
Q.changestate.q3 False True
Q.print.states
Q.print.tra
do.translate.dfa.re
"""
compiler(example)