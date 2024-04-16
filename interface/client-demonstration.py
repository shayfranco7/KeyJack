import socket

# Server IP address and port (replace with your server's details)
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 10319  # Port to listen on (non-privileged ports are > 1023)

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("connecting to server...")
# Connect to the server
client_socket.connect((HOST, PORT))

# Continuously get user input and send messages
while True:
    message = input("Enter message to send (or 'quit' to exit): ")

    # Send the message
    client_socket.sendall(message.encode())

    # Check for quit message
    if message == "quit":
        break

    # Receive server response (optional)
    # Uncomment the following lines to receive and display server responses
    # data = client_socket.recv(1024)
    # print(f"Received from server: {data.decode()}")

# Close the socket
client_socket.close()

print("Connection closed.")