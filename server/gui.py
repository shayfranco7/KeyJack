import tkinter as tk
from tkinter import filedialog, font, messagebox, ttk
import os
import shutil
from PIL import Image, ImageTk

class KeyJackGUI:
    def __init__(self, controller=None):
        self.controller = controller
        self.root = tk.Tk()
        self.file_list = []
        self.attacks_dir = "payloads"

        self.setup_gui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_gui(self):
        self.root.title("KeyJack Control Panel")
        self.root.geometry("1000x700")
        self.root.configure(bg='black')

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Sidebar.TFrame', background='#0078D7')
        self.style.configure('Content.TFrame', background='black')
        self.style.configure('TButton', background='#0078D7', foreground='white', font=('Arial', 12, 'bold'),
                             padding=10, relief='raised', borderwidth=2)
        self.style.map('TButton', background=[('active', '#005EA6')])
        self.style.configure('Save.TButton', background='#0078D7', foreground='white')
        self.style.map('Save.TButton', background=[('active', '#008C59')])
        self.style.configure('Clear.TButton', background='#FF6347', foreground='white')
        self.style.map('Clear.TButton', background=[('active', '#D84A32')])
        self.style.configure('TCombobox', fieldbackground='#2E2E2E', background='#0078D7', foreground='white')
        self.style.map('TCombobox', fieldbackground=[('readonly', '#2E2E2E')])

        self.cyber_font = font.Font(family="Consolas", size=16)
        self.title_font = font.Font(family="Consolas", size=24, weight="bold")

        self.create_widgets()

    def create_widgets(self):
        # Main container
        self.main_container = tk.Frame(self.root, bg='black')
        self.main_container.pack(fill=tk.BOTH, expand=True)
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ttk.Frame(self.main_container, style='Sidebar.TFrame', width=250)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)  # Prevent the sidebar from shrinking

        # Add logo to sidebar
        logo_image = Image.open("keyjacck_logo.png")  # Replace with your logo path
        logo_image = logo_image.resize((200, 150), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(self.sidebar, image=logo_photo, bg='#0078D7')
        logo_label.image = logo_photo  # Keep a reference
        logo_label.pack(pady=20)

        # Main content area
        self.main_frame = ttk.Frame(self.main_container, style='Content.TFrame')
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        # Sidebar buttons
        self.home_button = ttk.Button(self.sidebar, text="Home", command=self.show_home)
        self.home_button.pack(fill=tk.X, padx=10, pady=10)

        self.injection_button = ttk.Button(self.sidebar, text="Injection", command=self.show_injection)
        self.injection_button.pack(fill=tk.X, padx=10, pady=10)

        self.keystrokes_button = ttk.Button(self.sidebar, text="Keystrokes", command=self.show_keystrokes)
        self.keystrokes_button.pack(fill=tk.X, padx=10, pady=10)

        # Add status label to bottom of sidebar
        #self.status_label = tk.Label(self.sidebar, text="STATUS: DISCONNECTED", bg='#0078D7', fg='red2', font=self.cyber_font)
        #self.status_label.pack(side=tk.BOTTOM, pady=20)

        self.status_label = tk.Label(
            self.sidebar,
            text="STATUS: DISCONNECTED",
            bg='#0078D7',
            fg='red2',
            font=(self.cyber_font, 13, "bold")
        )
        self.status_label.pack(side=tk.BOTTOM, pady=20)

        # Content frames
        self.home_frame = ttk.Frame(self.main_frame, style='Content.TFrame')
        self.injection_frame = ttk.Frame(self.main_frame, style='Content.TFrame')
        self.keystrokes_frame = ttk.Frame(self.main_frame, style='Content.TFrame')

        # Setup content for each frame
        self.setup_home_frame()
        self.setup_injection_frame()
        self.setup_keystrokes_frame()

        # Show home frame by default
        self.show_home()

    def setup_home_frame(self):
        # Title
        title_label = tk.Label(self.home_frame, text="KeyJack Control Panel",
                               font=("Ariel", 40, "bold"), bg="black", fg="white")
        title_label.pack(pady=20)
        # Logo
        logo_image = Image.open("keyjacck_logo.png")  # Replace with your logo path
        logo_image = logo_image.resize((500, 400), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(self.home_frame, image=logo_photo, bg='black')
        logo_label.image = logo_photo  # Keep a reference
        logo_label.pack(pady=20)



    def setup_injection_frame(self):
        # Title
        title_label = tk.Label(self.injection_frame, text="Injection Control",
                               font=self.title_font, bg="black", fg="white")
        title_label.pack(pady=20)

        # Frame for comboboxes and buttons
        control_frame = ttk.Frame(self.injection_frame, style='Content.TFrame')
        control_frame.pack(pady=10, padx=10, fill=tk.X)

        # Subfolder selection
        subfolder_frame = ttk.Frame(control_frame, style='Content.TFrame')
        subfolder_frame.pack(fill=tk.X, pady=5)
        subfolder_label = tk.Label(subfolder_frame, text="Select Subfolder:", bg='black', fg='white', font=self.cyber_font)
        subfolder_label.pack(side=tk.LEFT, padx=(0, 10))
        self.second_combobox = ttk.Combobox(subfolder_frame, width=40, state="readonly")
        self.second_combobox.set("Select a subfolder")
        self.second_combobox.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # File selection
        file_frame = ttk.Frame(control_frame, style='Content.TFrame')
        file_frame.pack(fill=tk.X, pady=5)
        file_label = tk.Label(file_frame, text="Select File:", bg='black', fg='white', font=self.cyber_font)
        file_label.pack(side=tk.LEFT, padx=(0, 10))
        self.file_combobox = ttk.Combobox(file_frame, width=40, state="readonly")
        self.file_combobox.set("Select a file")
        self.file_combobox.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Buttons
        button_frame = ttk.Frame(control_frame, style='Content.TFrame')
        button_frame.pack(fill=tk.X, pady=10)
        self.refresh_button = ttk.Button(button_frame, text="Refresh")
        self.refresh_button.pack(side=tk.LEFT, padx=5)
        self.upload_button = ttk.Button(button_frame, text="Upload File")
        self.upload_button.pack(side=tk.LEFT, padx=5)

        # File description
        self.file_description = tk.Label(self.injection_frame, text="", bg='black', fg='#0078D7',
                                         font=self.cyber_font, wraplength=700)
        self.file_description.pack(pady=10)

        # Command center
        command_label = tk.Label(self.injection_frame, text="Command Center:", bg='black', fg='white', font=self.cyber_font)
        command_label.pack(anchor='w', padx=10, pady=(20, 5))
        self.command_center_area = tk.Text(self.injection_frame, height=10, bg='#000000', fg='#0078D7',
                                           font=self.cyber_font)
        self.command_center_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Execute button
        self.execute_button = ttk.Button(self.injection_frame, text="EXECUTE INJECTION")
        self.execute_button.pack(pady=20)

    def setup_keystrokes_frame(self):
        title_label = tk.Label(self.keystrokes_frame, text="Keystrokes Capture",
                               font=self.title_font, bg="black", fg="white")
        title_label.pack(pady=20)

        self.intercepted_keystrokes_area = tk.Text(self.keystrokes_frame, height=20, bg='#000000', fg='#0078D7',
                                                   font=self.cyber_font)
        self.intercepted_keystrokes_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        button_frame = ttk.Frame(self.keystrokes_frame, style='Content.TFrame')
        button_frame.pack(pady=10)

        self.save_button = ttk.Button(button_frame, text="Save", style='Save.TButton')
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(button_frame, text="Clear", style='Clear.TButton', command=self.clear_keystrokes)
        self.clear_button.pack(side=tk.LEFT, padx=5)

    def show_home(self):
        self.hide_all_frames()
        self.home_frame.pack(fill=tk.BOTH, expand=True)

    def show_injection(self):
        self.hide_all_frames()
        self.injection_frame.pack(fill=tk.BOTH, expand=True)

    def show_keystrokes(self):
        self.hide_all_frames()
        self.keystrokes_frame.pack(fill=tk.BOTH, expand=True)

    def hide_all_frames(self):
        for frame in (self.home_frame, self.injection_frame, self.keystrokes_frame):
            frame.pack_forget()

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

    def clear_keystrokes(self):
        self.intercepted_keystrokes_area.delete('1.0', tk.END)

    def on_closing(self):
        if self.controller:
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
        if self.controller:
            self.controller.on_second_select(None)

# Usage example:
if __name__ == "__main__":
    gui = KeyJackGUI()
    gui.start()