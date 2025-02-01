from dfa_data import DFA

def commandCall(entry, command):
    return command in entry

def moveRight(entry, command):
    if not isinstance(entry, str) or not isinstance(command, str):
        raise ValueError("Both entry and command must be strings.")
    return entry.replace(command, "") if command else entry

def readEqual(entry):
    for i in entry:
        if i == " " or i == "=":
            entry = moveRight(entry, i)
        else:
            return entry

def qPrint(entry, dfa):
    if ".all" in entry:
        dfa.display_dfa()
    if ".states" in entry:
        print(dfa.states)
    if ".tra" in entry:
        print(dfa.transitions)

def changeState(entry, dfa):
    result = entry.split(" ")
    stateName, start, final = result[0], result[1] == "True", result[2] == "True"

    state_index = dfa.states.index[dfa.states["Name"] == stateName].tolist()
    if state_index:
        state_index = state_index[0]
        dfa.states.at[state_index, "Is_Start"] = start
        dfa.states.at[state_index, "Is_Final"] = final
        if start:
            dfa.start_state = stateName  # Ensure the start state is correctly tracked
    else:
        dfa.add_state(stateName, start, final)
        print(f"State '{stateName}' added.")

def labelRemove(entry, dfa):
    lrlist = entry.split(" ")
    dfa.remove_transition(lrlist[0], lrlist[1], lrlist[2])

def labelChange(entry, dfa):
    lclist = entry.split(" ")
    old_start, old_end, old_label, new_label = lclist[:4]
    dfa.remove_transition(old_start, old_end, old_label)
    dfa.add_transition(old_start, old_end, new_label)

def labelConfigs(entry, dfa):
    if ".remove." in entry:
        labelRemove(moveRight(entry, ".remove."), dfa)
    elif ".change." in entry:
        labelChange(moveRight(entry, ".change."), dfa)
    elif ".add." in entry:
        eei(moveRight(entry, ".add."), dfa)

def que(entry, dfa):
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
        qPrint(moveRight(entry, ".print"), dfa)
    if ".changestate." in entry:
        changeState(moveRight(entry, ".changestate."), dfa)
    if ".label" in entry:
        labelConfigs(moveRight(entry, ".label"), dfa)

def eei(entry, dfa):
    eei_list = entry.split(" ")
    dfa.add_transition(eei_list[0], eei_list[1], eei_list[2])

def translate(entry, dfa):
    if ".dfa.gnfa" in entry:
        dfa.dfatable()
    if ".dfa.re" in entry:
        dfa.gtor()

def generalDos(entry, dfa):
    if ".translate" in entry:
        translate(moveRight(entry, "do"), dfa)

def navigator(entry, dfa):
    if commandCall(entry, "Q"):
        que(moveRight(entry, "Q"), dfa)
    if commandCall(entry, "do"):
        generalDos(moveRight(entry, "do"), dfa)

def compiler(code):
    dfa = DFA()
    lines = code.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if "E.{" in line:  # Start of an E block
            i += 1
            while i < len(lines) and lines[i] != "}":
                eei(lines[i], dfa)  # Pass the dfa instance
                i += 1
        else:
            navigator(line, dfa)  # Pass the dfa instance
            i += 1