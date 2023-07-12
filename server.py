import threading
import socket
import json

def handle_client(client):
    while True:
        message = client.recv(1024).decode()
        print("Received message:", message)
        if message == "exit":
            break

    client.close()

def start_server(ip,port):
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(ip,port)
    server.listen(10)
    print(f"Server started, listening on port {port}")

    while True:
        client, client_address = server.accept()
        print(f"Accepted connection from: {client_address}")

        client_thread = threading.Thread(target=handle_client,args=(client,))
        client_thread.start()
