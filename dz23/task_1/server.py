import socket
import time
from datetime import datetime

HOST = 'localhost'
PORT = 9966

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print("The server is waiting for a connection...")

while True:
    conn, addr = server_socket.accept()
    print(f"Connected to {addr}")

    while True:
        data = conn.recv(1024)
        if not data:
            break

        message = data.decode("utf-8")
        print(f"Received: {message} in {datetime.now()}")

        if message.lower() == 'exit':
            print("Received 'exit' command. I close the connection.")
            break

        time.sleep(5)
        sent_size = conn.send(data)

        if sent_size == len(data):
            print("All data has been successfully sent back to the client.")
        else:
            print("Error: Not all data was sent.")

    conn.close()
    if message.lower() == 'exit':
        break

server_socket.close()
print("The server has terminated.")
