import customtkinter as ctk
import sys
import io
from Compiler import compiler
from tkinter import messagebox, filedialog, Menu


class DFAGUIApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.title("Machina IDLE")
        self.geometry("800x600")
        self.minsize(600, 400)  # Minimum window size

        # UI Theme Configuration
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("dark-blue")

        # Initialize widgets
        self.create_widgets()

    def create_widgets(self):
        # Configure grid layout for automatic resizing
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Menu Bar
        self.menu_bar = Menu(self)
        self.config(menu=self.menu_bar)

        # File menu
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Open File", command=self.open_file)
        file_menu.add_command(label="Save File", command=self.save_file)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Output menu
        output_menu = Menu(self.menu_bar, tearoff=0)
        output_menu.add_command(label="Save Output", command=self.save_output)
        output_menu.add_command(label="Clear Output", command=self.clear_output)
        self.menu_bar.add_cascade(label="Output", menu=output_menu)

        # Run Button
        self.menu_bar.add_command(label="▶ Run Code", command=self.run_code)

        # Code Entry Section
        self.code_frame = ctk.CTkFrame(self)
        self.code_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.code_frame.grid_propagate(False)
        self.code_text = ctk.CTkTextbox(self.code_frame, font=("Courier", 12))
        self.code_text.pack(fill="both", expand=True)

        # Output Section
        self.output_frame = ctk.CTkFrame(self)
        self.output_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.output_frame.grid_propagate(False)
        self.output_text = ctk.CTkTextbox(self.output_frame, font=("Courier", 12))
        self.output_text.pack(fill="both", expand=True)
        self.output_text.configure(state=ctk.DISABLED)  # Make the output read-only

    def open_file(self):
        """Open a .txt file and load its content into the code editor."""
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                    self.code_text.delete("1.0", ctk.END)
                    self.code_text.insert(ctk.END, content)
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {e}")

    def save_file(self):
        """Save the content of the code editor to a .txt file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(self.code_text.get("1.0", ctk.END).strip())
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")

    def save_output(self):
        """Save the output content to a file."""
        output = self.output_text.get("1.0", ctk.END).strip()
        if not output:
            messagebox.showerror("Error", "No output to save.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(output)
            except Exception as e:
                messagebox.showerror("Error", f"Could not save output: {e}")

    def clear_output(self):
        """Clear the output text area."""
        self.output_text.configure(state=ctk.NORMAL)  # Make output writable
        self.output_text.delete("1.0", ctk.END)  # Clear output text
        self.output_text.configure(state=ctk.DISABLED)  # Make output read-only again

    def run_code(self):
        """Execute the code entered in the editor."""
        code = self.code_text.get("1.0", ctk.END).strip()

        if not code:
            messagebox.showerror("Error", "Please enter some code to run.")
            return

        # Redirect stdout to capture the code output
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        try:
            # Clear previous output and insert a separator
            self.output_text.configure(state=ctk.NORMAL)  # Make output writable
            self.output_text.insert(ctk.END, "\n" + "=" * 50 + "\n")  # Separator

            # Process the DFA code
            self.process_dfa_input(code)
            output = sys.stdout.getvalue()
            self.output_text.insert(ctk.END, output + "\n")  # Add output

        except Exception as e:
            # Show the error in the output box
            self.output_text.insert(ctk.END, f"Error: {e}\n")

        finally:
            # Reset stdout to its original state
            sys.stdout = old_stdout
            self.output_text.configure(state=ctk.DISABLED)  # Make output read-only

    def process_dfa_input(self, code):
        """Process and execute the DFA code using the compiler."""
        compiler(code)  # Assuming compiler processes and executes the code


if __name__ == "__main__":
    app = DFAGUIApp()
    app.mainloop()
