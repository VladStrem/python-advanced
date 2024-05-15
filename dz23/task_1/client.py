import socket

HOST = 'localhost'
PORT = 9966

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

while True:
    message = input("Enter a message to send to the server (or 'exit' to exit): ")
    client_socket.send(message.encode("utf-8"))
    if message.lower() == 'exit':
        break

    data = client_socket.recv(1024)
    print(f"Response from the server: {data.decode("utf-8")}")

client_socket.close()
