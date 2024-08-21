import tkinter as tk
from tkinter import filedialog


def select_file():
    # Open a file dialog and return the selected file path
    file_path = filedialog.askopenfilename()
    if file_path:
        print(f"Selected file: {file_path}")
        label.config(text=f"Selected file: {file_path}")


# Create the main window
root = tk.Tk()
root.title("File Selector")

# Create and place a button that triggers the file selection dialog
select_button = tk.Button(root, text="Select File", command=select_file)
select_button.pack(pady=20)

# Create and place a label to show the selected file path
label = tk.Label(root, text="No file selected")
label.pack(pady=20)

# Run the application
root.mainloop()
