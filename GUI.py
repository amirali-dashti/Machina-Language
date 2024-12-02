import customtkinter as ctk

# Initialize CustomTkinter theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class GridApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Grid Size Input")
        self.geometry("400x200")
        
        self.label = ctk.CTkLabel(self, text="Enter grid size (n):")
        self.label.pack(pady=10)
        
        self.grid_size_entry = ctk.CTkEntry(self)
        self.grid_size_entry.pack(pady=10)
        
        self.submit_button = ctk.CTkButton(self, text="Create Grid", command=self.create_grid_window)
        self.submit_button.pack(pady=10)
        
    def create_grid_window(self):
        try:
            n = int(self.grid_size_entry.get())
            if n <= 0:
                raise ValueError("Grid size must be positive.")
        except ValueError:
            ctk.CTkMessageBox.show_error("Error", "Please enter a valid positive integer.")
            return

        grid_window = ctk.CTkToplevel(self)
        grid_window.title(f"{n} x {n} Grid")
        grid_window.geometry(f"{n*100+100}x{n*100+100}")

        self.entries = []  # Store entries in a list of lists
        
        # Create column headers
        for col in range(n):
            header = ctk.CTkLabel(grid_window, text=f"{col+1}", width=40, fg_color="lightgrey")
            header.grid(row=0, column=col+1, padx=2, pady=2, sticky="nsew")

        # Create row headers and entries grid
        for i in range(n):
            # Row header
            row_header = ctk.CTkLabel(grid_window, text=f"{i+1}", width=40, fg_color="lightgrey")
            row_header.grid(row=i+1, column=0, padx=2, pady=2, sticky="nsew")
            
            row_entries = []
            for j in range(n):
                entry = ctk.CTkEntry(grid_window, width=60)
                entry.grid(row=i+1, column=j+1, padx=5, pady=5, sticky="nsew")
                row_entries.append(entry)
            self.entries.append(row_entries)

        # Add a submit button to collect the grid data
        collect_button = ctk.CTkButton(grid_window, text="Collect Data", command=self.collect_grid_data)
        collect_button.grid(row=n+1, column=0, columnspan=n+1, pady=10)

        # Make grid responsive
        for i in range(n+1):
            grid_window.grid_columnconfigure(i, weight=1)
            grid_window.grid_rowconfigure(i, weight=1)
        
    def collect_grid_data(self):
        grid_data = []
        for row in self.entries:
            row_data = [entry.get() for entry in row]
            grid_data.append(row_data)
        
        # Print grid data to console (or handle it as needed)
        print("Grid Data:")
        for row in grid_data:
            print(row)
        ctk.CTkMessageBox.show_info("Grid Data Collected", "Grid data has been collected and printed in the console.")

if __name__ == "__main__":
    app = GridApp()
    app.mainloop()
