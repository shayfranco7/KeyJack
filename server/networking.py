import socket
import threading

class KeyJackNetwork:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server_socket = None
        self.connected_client = None

    def setup_network(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(1)
        threading.Thread(target=self.accept_connections, daemon=True).start()

    def accept_connections(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            self.connected_client = client_socket
            self.on_connect()
            threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                self.on_receive(data)
            except:
                break
        self.connected_client = None
        self.on_disconnect()

    def send_message_to_client(self, message):
        if self.connected_client:
            try:
                self.connected_client.send(message.encode('utf-8'))
                self.on_send(message)
            except:
                self.on_send_fail()

    # Callbacks to be connected by the controller
    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_receive(self, data):
        pass

    def on_send(self, message):
        pass

    def on_send_fail(self):
        pass

    def close(self):
        if self.server_socket:
            self.server_socket.close()
