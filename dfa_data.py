# dfa_data.py

import pandas as pd
import numpy as np

class DFA:
    def __init__(self):
        # Initialize state and transition management with Pandas DataFrames
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
        else:
            self.transitions = pd.concat([self.transitions, pd.DataFrame({
                "Start_State": [start_state],
                "End_State": [end_state],
                "Label": [label]
            })], ignore_index=True)
            return f"Transition from '{start_state}' to '{end_state}' with label '{label}' added."

    def display_dfa(self):
        output = f"\nDFA States:\n{self.states}\nDFA Transitions:\n{self.transitions}\nGNFA Table:\n{self.dfatable()}"
        return output
        
    def dfatable(self):
        n = len(self.states)
        
        # Re-index the states, so the state numbering starts from 1
        state_to_index = {state: index + 1 for index, state in enumerate(self.states["Name"].values)}
        
        # Add a new start state (state 0) and a new final state (state n+1)
        self.table = pd.DataFrame(np.full((n + 2, n + 2), "n"))  # Create table of size (n+2) x (n+2)

        # Add epsilon transitions (e) to the new start state and final state
        for i in range(n):
            # epsilon transition from the new start state (0) to the original start state
            if self.states.iloc[i]["Is_Start"]:
                self.table.iloc[0, state_to_index[self.states.iloc[i]["Name"]]] = "e"
            # epsilon transition from each final state to the new final state (n+1)
            if self.states.iloc[i]["Is_Final"]:
                self.table.iloc[state_to_index[self.states.iloc[i]["Name"]], n+1] = "e"
        
        # Now, fill in the transitions based on the original DFA
        for _, row in self.transitions.iterrows():
            start_state = row["Start_State"]
            end_state = row["End_State"]
            label = row["Label"]
            
            # Make sure that the state-to-index mapping is correct
            if start_state in state_to_index and end_state in state_to_index:
                i = state_to_index[start_state]  # Get the index for the start state
                j = state_to_index[end_state]    # Get the index for the end state
                
                # Set the table cell to the label of the transition
                self.table.iloc[i, j] = label
        
        print(self.table)  # To check the updated table
        return self.table



    def export_dfa(self, file_path="dfa_export.xlsx"):
        with pd.ExcelWriter(file_path) as writer:
            self.states.to_excel(writer, sheet_name="States", index=False)
            self.transitions.to_excel(writer, sheet_name="Transitions", index=False)
        return f"DFA exported to '{file_path}'."

    def validate_dfa(self):
        # Check if a start state exists
        if not self.start_state:
            return "DFA validation failed: No start state defined."
        # Check if at least one final state exists
        if not self.states[self.states["Is_Final"]].empty:
            return "DFA validation successful."
        else:
            return "DFA validation failed: No final states defined."