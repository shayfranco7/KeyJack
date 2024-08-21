import tkinter as tk
from tkinter import filedialog, font, messagebox, ttk
import os
import shutil
class KeyJackGUI:
    def __init__(self, controller=None):
        self.controller = controller
        self.root = tk.Tk()
        self.file_list = []
        self.attacks_dir = "payloads"

        self.setup_gui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_gui(self):
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
        self.second_combobox.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.file_combobox = ttk.Combobox(repo_frame, width=50, state="readonly")
        self.file_combobox.set("Select a file")
        self.file_combobox.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.refresh_button = ttk.Button(repo_frame, text="Refresh")
        self.refresh_button.pack(side=tk.RIGHT, padx=5)

        self.upload_button = ttk.Button(repo_frame, text="Upload File")
        self.upload_button.pack(side=tk.RIGHT, padx=5)

        self.file_description = tk.Label(self.injection_frame, text="", bg='#2E2E2E', fg='#00FF00',
                                         font=self.cyber_font, wraplength=850)
        self.file_description.pack(pady=5)

        self.command_center_area = tk.Text(self.injection_frame, height=15, bg='#000000', fg='#00FF00',
                                           font=self.cyber_font)
        self.command_center_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.execute_button = ttk.Button(self.injection_frame, text="EXECUTE INJECTION")
        self.execute_button.pack(pady=10)


    def setup_keystrokes_tab(self):
        self.intercepted_keystrokes_area = tk.Text(self.keystrokes_frame, height=20, bg='#000000', fg='#00FF00',
                                                   font=self.cyber_font)
        self.intercepted_keystrokes_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.save_button = ttk.Button(self.keystrokes_frame, text="SAVE KEYSTROKES")
        self.save_button.pack(pady=10)


    def bind_controller_events(self):
        """Bind controller methods to GUI events."""
        self.second_combobox.bind("<<ComboboxSelected>>", self.controller.on_second_select)
        self.file_combobox.bind("<<ComboboxSelected>>", self.controller.on_file_select)
        self.refresh_button.config(command=self.controller.load_subfolder_list)
        self.upload_button.config(command=self.controller.upload_file)
        self.execute_button.config(command=self.controller.handle_sending)
        self.save_button.config(command=self.controller.save_keystrokes)
        self.controller.load_subfolder_list()

    def start(self):
        self.root.mainloop()

    def update_status(self, status, color):
        self.status_label.config(text=f"STATUS: {status}", fg=color)

    def update_file_description(self, description):
        self.file_description.config(text=description)

    def update_command_center(self, message):
        self.command_center_area.insert(tk.END, message + "\n")
        self.command_center_area.see(tk.END)

    def update_intercepted_keystrokes(self, message):
        self.intercepted_keystrokes_area.insert(tk.END, message)
        self.intercepted_keystrokes_area.see(tk.END)

    def on_closing(self):
        self.controller.on_closing()
        self.root.destroy()

    def load_file_list(self, options):
        self.file_combobox['values'] = options
        if options:
            self.file_combobox.set(options[0])
            self.update_file_description(options[0])
        else:
            self.file_combobox.set('')
            self.file_description.config(text="No files found in the selected directory.")

    def load_subfolder_list(self, subfolders):
        self.second_combobox['values'] = subfolders
        self.second_combobox.set('All Files')
        self.controller.on_second_select(None)
