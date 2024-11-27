import socket
import threading

PORT = 8000
BUFFER_SIZE = 4096

def handle_client(client_socket):
    try:
        # Receive and print the initial hello message from the client
        hello_message = client_socket.recv(BUFFER_SIZE).decode('utf-8')
        print(f"Message from client: {hello_message}")

        # Send a hello message back to the client
        response = "Hello from server"
        client_socket.sendall(response.encode('utf-8'))
        print("Hello message sent to client")

        # Receive the file name and size
        file_info = client_socket.recv(BUFFER_SIZE).decode('utf-8').split(',')
        file_name, file_size = file_info[0], int(file_info[1])
        
        # Open a file to write the incoming data
        with open(file_name, 'wb') as f:
            bytes_received = 0
            while bytes_received < file_size:
                data = client_socket.recv(BUFFER_SIZE)
                if not data:
                    break
                f.write(data)
                bytes_received += len(data)

        print(f"Received file: {file_name}")
    finally:
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', PORT))
    server_socket.listen(5)
    print(f"Server started on port {PORT}. Waiting for connections...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection accepted from {client_address}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
