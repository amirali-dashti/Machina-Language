import tkinter as tk
from tkinter import simpledialog, messagebox

class DFABuilderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DFA Builder")
        self.root.geometry("800x600")

        # Create a canvas with a blue background (bluesheet)
        self.canvas = tk.Canvas(self.root, bg="#87CEEB", width=800, height=500)  # Light blue color
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Buttons for control with better layout
        self.add_button_frame()

        # State variables
        self.states = []  # [(x, y, name)]
        self.transitions = []  # [(start_state, end_state, label)]
        self.start_state = None
        self.final_states = set()
        self.drawing_line = False
        self.current_line = None

        # Bind mouse events for state and line drawing
        self.canvas.bind("<Button-1>", self.create_state)
        self.canvas.bind("<Button-3>", self.start_transition)
        self.canvas.bind("<ButtonRelease-3>", self.end_transition)

    def add_button_frame(self):
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=5)

        tk.Button(frame, text="Set Start/Final States", command=self.set_start_final_states, bg="orange", font=("Arial", 10), width=20).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Clear", command=self.clear_canvas, bg="red", fg="white", font=("Arial", 10), width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Export DFA", command=self.export_dfa, bg="green", fg="white", font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)

    def create_state(self, event):
        state_num = len(self.states) + 1
        x, y = event.x, event.y
        r = 30  # Radius of the circle

        # Draw the state
        state_id = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="white", outline="black", width=2)
        self.canvas.create_text(x, y, text=f"q{state_num}", font=("Arial", 12, "bold"))

        # Store state information
        self.states.append((x, y, f"q{state_num}", state_id))

    def start_transition(self, event):
        self.start_state = self.get_state_at(event.x, event.y)
        if self.start_state:
            self.current_line = self.canvas.create_line(event.x, event.y, event.x, event.y, arrow=tk.LAST, width=2)
            self.drawing_line = True

    def end_transition(self, event):
        if self.drawing_line and self.start_state:
            end_state = self.get_state_at(event.x, event.y)
            if end_state:
                if end_state == self.start_state:
                    # Draw self-loop
                    self.draw_self_loop(self.start_state)
                else:
                    # Offset lines to handle multiple transitions
                    self.offset_line(event.x, event.y, end_state)

                label = self.ask_for_transition_label()
                self.transitions.append((self.start_state[2], end_state[2], label))
                self.display_transition_label(self.start_state, end_state, label)
            else:
                self.canvas.delete(self.current_line)
            self.drawing_line = False

    def draw_self_loop(self, state):
        x, y, name, _ = state
        r = 40
        self.canvas.create_arc(x - r, y - r, x + r, y + r, start=0, extent=300, style=tk.ARC, width=2, outline="black")

    def offset_line(self, x, y, end_state):
        coords = self.canvas.coords(self.current_line)
        # Offset by 10 pixels for visibility in case of multiple transitions
        self.canvas.coords(self.current_line, coords[0], coords[1], x + 10, y + 10)

    def display_transition_label(self, start_state, end_state, label):
        x1, y1, _, _ = start_state
        x2, y2, _, _ = end_state
        mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2

        # Adjust label's position based on the distance between start and end state
        offset_y = -20 if x1 != x2 or y1 != y2 else -40

        # Prevent overlap of multiple labels on top of each other
        label_offset = 0
        for existing_label in self.canvas.find_withtag("transition_label"):
            existing_coords = self.canvas.coords(existing_label)
            if abs(existing_coords[0] - mid_x) < 50 and abs(existing_coords[1] - mid_y) < 50:
                label_offset += 20

        # Place the label with an appropriate offset
        self.canvas.create_text(mid_x, mid_y + offset_y + label_offset, text=label, font=("Arial", 10, "bold"), tags="transition_label")

    def ask_for_transition_label(self):
        label = simpledialog.askstring("Transition Label", "Enter Transition Label:")
        return label if label else "λ"

    def get_state_at(self, x, y):
        for state in self.states:
            sx, sy, name, state_id = state
            if (x - sx) ** 2 + (y - sy) ** 2 <= 30 ** 2:  # Check if inside circle
                return state
        return None

    def set_start_final_states(self):
        state_names = [name for _, _, name, _ in self.states]
        self.start_state = simpledialog.askstring("Select Start State", f"Choose a Start State:\n{state_names}")
        if self.start_state not in state_names:
            messagebox.showerror("Error", "Invalid Start State. Please try again.")
            return
        
        final_states_input = simpledialog.askstring("Select Final States", f"Choose Final States (comma separated):\n{state_names}")
        try:
            final_states_list = [state.strip() for state in final_states_input.split(",")]
            for state in final_states_list:
                if state not in state_names:
                    raise ValueError
            self.final_states = set(final_states_list)
            self.highlight_start_final_states()
        except:
            messagebox.showerror("Error", "Invalid Final States. Please try again.")

    def highlight_start_final_states(self):
        # Highlight start state with green and final states with yellow
        for _, _, name, state_id in self.states:
            if name == self.start_state:
                self.canvas.itemconfig(state_id, fill="lightgreen", width=3)
            elif name in self.final_states:
                self.canvas.itemconfig(state_id, fill="yellow", width=3)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.states.clear()
        self.transitions.clear()
        self.start_state = None
        self.final_states.clear()

    def export_dfa(self):
        print("States:", [name for _, _, name, _ in self.states])
        print("Start State:", self.start_state)
        print("Final States:", self.final_states)
        print("Transitions:", self.transitions)
        messagebox.showinfo("DFA Exported", "DFA exported successfully!\nCheck the console for details.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DFABuilderApp(root)
    root.mainloop()
