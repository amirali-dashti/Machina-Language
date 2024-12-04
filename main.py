import customtkinter as ctk
from tkinter import filedialog, messagebox
from dfa_data import DFA
from Compiler import compiler
import sys
import io

class DFAGUIApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.title("DFA to Regular Expression Convertor")
        self.geometry("800x600")

        # UI Theme Configuration
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("dark-blue")

        # Initialize widgets
        self.create_widgets()

    def create_widgets(self):
        # Code Entry Section
        self.code_label = ctk.CTkLabel(self, text="Write or Paste Your DFA Code Here:", font=("Arial", 14))
        self.code_label.pack(pady=10)

        self.code_text = ctk.CTkTextbox(self, width=700, height=200, font=("Courier", 12))
        self.code_text.pack(pady=10)

        self.run_button = ctk.CTkButton(self, text="Run Code", command=self.run_code)
        self.run_button.pack(pady=10)

        # Output Text Box for displaying results or errors
        self.output_text = ctk.CTkTextbox(self, width=700, height=200, font=("Courier", 12))
        self.output_text.pack(pady=10)

        # File selection section
        self.file_label = ctk.CTkLabel(self, text="Select DFA Input File:", font=("Arial", 14))
        self.file_label.pack(pady=10)

        self.file_entry = ctk.CTkEntry(self, width=400)
        self.file_entry.pack(pady=5)

        self.browse_button = ctk.CTkButton(self, text="Browse", command=self.browse_file)
        self.browse_button.pack(pady=5)

        # Buttons for loading and validating DFA
        self.load_button = ctk.CTkButton(self, text="Load and Display DFA", command=self.load_dfa)
        self.load_button.pack(pady=10)

        self.validate_button = ctk.CTkButton(self, text="Validate DFA", command=self.validate_dfa)
        self.validate_button.pack(pady=5)

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            self.file_entry.delete(0, ctk.END)
            self.file_entry.insert(0, file_path)

    def load_dfa(self):
        file_path = self.file_entry.get().strip()
        if not file_path:
            messagebox.showerror("Error", "Please select a valid file.")
            return

        self.dfa = self.parse_input_file(file_path)
        if self.dfa:
            self.display_dfa()
        else:
            messagebox.showerror("Error", "Failed to load DFA from input file.")

    def validate_dfa(self):
        if hasattr(self, 'dfa') and self.dfa:
            result = self.dfa.validate_dfa()
            self.output_text.insert(ctk.END, f"\n\nValidation Result: {result}\n")
            if "successful" in result:
                messagebox.showinfo("Validation Result", result)
            else:
                messagebox.showwarning("Validation Result", result)
        else:
            messagebox.showerror("Error", "Please load a DFA first.")

    def display_dfa(self):
        if hasattr(self, 'dfa'):
            self.output_text.insert(ctk.END, self.dfa.display_dfa())

    def run_code(self):
        code = self.code_text.get("1.0", ctk.END).strip()

        if not code:
            messagebox.showerror("Error", "Please enter some code to run.")
            return

        # Redirect stdout to capture the code output
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        try:
            # Convert the input into valid Python code
            self.process_dfa_input(code)
            output = sys.stdout.getvalue()
            self.output_text.insert(ctk.END, f"\n{output}\n")

        except Exception as e:
            error_message = f"Error: {e}\n"
            self.output_text.insert(ctk.END, error_message)

        # Reset stdout to its original state
        sys.stdout = old_stdout

    def process_dfa_input(self, code):
        compiler(self, code)

if __name__ == "__main__":
    app = DFAGUIApp()
    app.mainloop()
