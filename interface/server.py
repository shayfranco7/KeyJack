import socket
import threading
import tkinter as tk


class Server:
    connected_logger = None
    root = tk.Tk()
    root.title("Text Area Example")

    # Create the text area widget
    text_area = tk.Text(root, height=10, width=50)

    # Add scrollbars (optional)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=text_area.yview)
    text_area.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Pack the text area in the window
    text_area.pack()

    last_received_message = ""

    def __init__(self):
        self.server_socket = None
        worker_thread = threading.Thread(target=self.create_listening_server)
        worker_thread.start()
        print("Server thread started")
        self.root.mainloop()

    # listen for incoming connection
    def create_listening_server(self):

        self.server_socket = socket.socket(socket.AF_INET,
                                           socket.SOCK_STREAM)  # create a socket using TCP port and ipv4
        local_ip = '127.0.0.1'
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
        while True:
            incoming_buffer = so.recv(256)  # initialize the buffer
            if not incoming_buffer:
                break
            self.last_received_message = incoming_buffer.decode('utf-8')
            print(self.last_received_message)
            #self.broadcast_to_all_clients(so)  # send to all clients
        so.close()

    # broadcast the message to all clients
    def broadcast_to_all_clients(self, senders_socket):  # send output to logger
        for client in self.clients_list:
            socket, (ip, port) = client
            if socket is not senders_socket:
                socket.sendall(self.last_received_message.encode('utf-8'))

    def receive_messages_in_a_new_thread(self):
        while True:
            client = so, (ip, port) = self.server_socket.accept()
            self.connected_logger = client
            print('Connected to ', ip, ':', str(port))
            t = threading.Thread(target=self.receive_messages, args=(so,))
            t.start()

    # add a new client



if __name__ == "__main__":
    Server()
    # Run the main loop
