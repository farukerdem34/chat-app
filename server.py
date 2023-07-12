import threading
import socket
from json import loads, dumps
import argparse


clients = []


def get_user_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--user-size",
                        help="Maximum user size.", dest="usersize", default=3)
    args = parser.parse_args
    return args


def broadcast_data(clients, data):
    for client in clients:
        client.send(data)


def add_new_client(client):
    if not (client in clients):
        clients.append(client)


def handle_client(client):
    while True:
        data = client.recv(1024)
        broadcast_data(clients, data)
        data = loads(data)
        message = data["message"]
        username = data["username"]
        print(username + ": " + message)


def start_server(ip, port, usersize):
    try:

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((ip, port))
        server.listen(usersize)
        print(f"Server started, listening on port {port}")

        while True:
            client, client_address = server.accept()
            print(f"Accepted connection from: {client_address}")
            add_new_client(client)
            client_thread = threading.Thread(
                target=handle_client, args=(client,))
            client_thread.start()
    except KeyboardInterrupt:
        server.close()


args = get_user_input()

start_server("localhost", 8000, args.usersize)
