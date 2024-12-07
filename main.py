import customtkinter as ctk
import sys
import io
from Compiler import compiler
from tkinter import messagebox

class DFAGUIApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.title("Machina IDLE")
        self.geometry("800x600")

        # UI Theme Configuration
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("dark-blue")

        # Initialize widgets
        self.create_widgets()

    def create_widgets(self):
        # Code Entry Section
        self.code_text = ctk.CTkTextbox(self, width=700, height=200, font=("Courier", 12))
        self.code_text.pack(pady=10)

        # Run Button at top right
        self.run_button = ctk.CTkButton(self, text="▶", command=self.run_code)
        self.run_button.place(relx=0.98, rely=0.02, anchor='ne')  # Adjusted placement for better positioning

        # Output Text Box for displaying results
        self.output_text = ctk.CTkTextbox(self, width=700, height=200, font=("Courier", 12))
        self.output_text.pack(pady=10)

    def run_code(self):
        code = self.code_text.get("1.0", ctk.END).strip()

        if not code:
            messagebox.showerror("Error", "Please enter some code to run.")
            return

        # Redirect stdout to capture the code output
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        try:
            # Process the DFA code
            self.process_dfa_input(code)
            output = sys.stdout.getvalue()
            self.output_text.insert(ctk.END, f"\n{output}\n")

        except Exception as e:
            error_message = f"Error: {e}\n"
            self.output_text.insert(ctk.END, error_message)

        # Reset stdout to its original state
        sys.stdout = old_stdout

    def process_dfa_input(self, code):
        compiler(code)

if __name__ == "__main__":
    app = DFAGUIApp()
    app.mainloop()
