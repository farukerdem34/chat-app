import threading
import socket
import json

clients = []


def broadcast_message(clients, message):
    for client in clients:
        client.send(message.encode())


def add_new_client(client):
    if not (client in clients):
        clients.append(client)


def handle_client(client):
    while True:
        message = client.recv(1024).decode()
        print(f"{message}\n")
        broadcast_message(clients, message)


def start_server(ip, port):
    try:

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((ip, port))
        server.listen(10)
        print(f"Server started, listening on port {port}")

        while True:
            client, client_address = server.accept()
            print(f"Accepted connection from: {client_address}\n")
            add_new_client(client)
            client_thread = threading.Thread(
                target=handle_client, args=(client,))
            client_thread.start()
    except KeyboardInterrupt:
        server.close()


start_server("localhost", 8000)
