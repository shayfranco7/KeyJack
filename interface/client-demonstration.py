import socket
import threading

# Server IP address and port (replace with your server's details)
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 10319  # Port to listen on (non-privileged ports are > 1023)


def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"Received from server: {data}")
        except:
            break
    print("Disconnected from server.")
    client_socket.close()


# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("connecting to server...")
# Connect to the server
client_socket.connect((HOST, PORT))

# Start a thread to receive messages from the server
threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

# Continuously get user input and send messages
while True:
    message = input("Enter message to send (or 'quit' to exit): ")

    # Send the message
    client_socket.sendall(message.encode())

    # Check for quit message
    if message == "quit":
        break

# Close the socket
client_socket.close()
print("Connection closed.")
