# dfa_data.py

import pandas as pd
import numpy as np
from GNFAtoRE import gtor

class DFA:
    def __init__(self):
        self.states = pd.DataFrame(columns=["Name", "Is_Start", "Is_Final"])
        self.transitions = pd.DataFrame(columns=["Start_State", "End_State", "Label"])
        self.start_state = None

    def add_state(self, name, is_start, is_final):
        if name in self.states["Name"].values:
            return f"State '{name}' already exists."
        else:
            self.states = pd.concat([self.states, pd.DataFrame({
                "Name": [name],
                "Is_Start": [is_start],
                "Is_Final": [is_final]
            })], ignore_index=True)
            if is_start:
                self.start_state = name
            return f"State '{name}' added."

    def add_transition(self, start_state, end_state, label):
        if start_state not in self.states["Name"].values or end_state not in self.states["Name"].values:
            return "Both start and end states must exist before adding a transition."
        self.transitions = pd.concat([self.transitions, pd.DataFrame({
            "Start_State": [start_state],
            "End_State": [end_state],
            "Label": [label]
        })], ignore_index=True)
        return f"Transition from '{start_state}' to '{end_state}' with label '{label}' added."

    def change_transition(self, start_state, end_state, label, new_start_state=None, new_end_state=None, new_label=None):
        mask = (
            (self.transitions["Start_State"] == start_state) & 
            (self.transitions["End_State"] == end_state) & 
            (self.transitions["Label"] == label)
        )
        if not mask.any():
            return f"No transition from '{start_state}' to '{end_state}' with label '{label}' found."

        if new_start_state:
            if new_start_state not in self.states["Name"].values:
                return f"New start state '{new_start_state}' does not exist."
            self.transitions.loc[mask, "Start_State"] = new_start_state

        if new_end_state:
            if new_end_state not in self.states["Name"].values:
                return f"New end state '{new_end_state}' does not exist."
            self.transitions.loc[mask, "End_State"] = new_end_state

        if new_label:
            self.transitions.loc[mask, "Label"] = new_label

        return "Transition updated successfully."

    def remove_transition(self, start_state, end_state, label):
        mask = (
            (self.transitions["Start_State"] == start_state) & 
            (self.transitions["End_State"] == end_state) & 
            (self.transitions["Label"] == label)
        )
        if not mask.any():
            return f"No transition from '{start_state}' to '{end_state}' with label '{label}' found."
        
        self.transitions = self.transitions[~mask].reset_index(drop=True)
        return f"Transition from '{start_state}' to '{end_state}' with label '{label}' removed."

    def display_dfa(self):
        output = f"\nDFA States:\n{self.states}\nDFA Transitions:\n{self.transitions}\nGNFA Table:\n{self.dfatable()}"
        return output
        
    def dfatable(self):
        n = len(self.states)
        state_to_index = {state: index + 1 for index, state in enumerate(self.states["Name"].values)}
        self.table = pd.DataFrame(np.full((n + 2, n + 2), "n"))

        # Mark initial and final states
        for i in range(n):
            if self.states.iloc[i]["Is_Start"]:
                self.table.iloc[0, state_to_index[self.states.iloc[i]["Name"]]] = "e"
            if self.states.iloc[i]["Is_Final"]:
                self.table.iloc[state_to_index[self.states.iloc[i]["Name"]], n + 1] = "e"
        
        # Insert transitions
        for _, row in self.transitions.iterrows():
            i, j = state_to_index[row["Start_State"]], state_to_index[row["End_State"]]
            if self.table.iloc[i, j] == "n":
                self.table.iloc[i, j] = row["Label"]
            else:
                self.table.iloc[i, j] += f"U{row['Label']}"  # Union if already exists
        
        print("The translation result from DFA to GNFA:")
        print(self.table)
        return self.table

    def gtor(self):
        self.dfatable()
        
        table = self.table.copy()
        
        gtor(table)
    
    
    def export_dfa(self, file_path="dfa_export.xlsx"):
        with pd.ExcelWriter(file_path) as writer:
            self.states.to_excel(writer, sheet_name="States", index=False)
            self.transitions.to_excel(writer, sheet_name="Transitions", index=False)
        return f"DFA exported to '{file_path}'."

    def validate_dfa(self):
        if not self.start_state:
            return "DFA validation failed: No start state defined."
        if not self.states[self.states["Is_Final"]].empty:
            return "DFA validation successful."
        else:
            return "DFA validation failed: No final states defined."
