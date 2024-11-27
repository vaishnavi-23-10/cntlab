import socket
import os

PORT = 8000
BUFFER_SIZE = 4096

def send_file(server_ip, port, file_path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))

    # Send a hello message to the server
    hello_message = "Hello from client"
    client_socket.sendall(hello_message.encode('utf-8'))

    # Receive the server's hello message
    server_response = client_socket.recv(BUFFER_SIZE).decode('utf-8')
    print(f"Message from server: {server_response}")

    # Prepare to send the file
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    client_socket.send(f"{file_name},{file_size}".encode('utf-8'))

    with open(file_path, 'rb') as f:
        bytes_read = f.read(BUFFER_SIZE)
        while bytes_read:
            client_socket.send(bytes_read)
            bytes_read = f.read(BUFFER_SIZE)

    print(f"Sent file: {file_name}")
    client_socket.close()

# Example usage
if __name__ == "__main__":
    send_file("127.0.0.1", PORT, "tcp.txt")  # Replace with the actual file path
