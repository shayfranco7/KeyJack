import tkinter as tk
from tkinter import ttk
import os

def create_menu(window):
    # Create a StringVar to hold the selected value
    selected_file = tk.StringVar()

    # Create the Combobox
    combo = ttk.Combobox(window, textvariable=selected_file, state="readonly", width=50)

    # Populate the Combobox
    options = []
    base_dir = "payloads"
    for dir_path, dirs, files in os.walk(base_dir):
        level = dir_path.replace(base_dir, '').count(os.sep)
        indent = ' ' * 4 * level
        subdir = os.path.basename(dir_path)
        if subdir:
            options.append(f"{indent}{subdir}/")
        for f in files:
            options.append(f"{indent}    {f}")

    combo['values'] = options

    # Function to handle selection
    def on_select(event):
        print(f"Selected: {selected_file.get()}")

    combo.bind('<<ComboboxSelected>>', on_select)
    combo.pack(pady=20)

    window.mainloop()

if __name__ == "__main__":
    create_menu()