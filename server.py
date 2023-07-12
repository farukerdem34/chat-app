import threading
import socket
from json import loads, dumps
import argparse


clients = []


def generate_json_data():
    with open("config.json", "w") as data:
        server_ip = str(input("Enter server IP: "))
        try:
            server_port = int(input("Enter server port: "))
            server_size = int(input("Enter server size:"))
        except ValueError:
            print("Enter integer!")
            server_port = int(input("Enter server port: "))
        config = {
            "server-ip": server_ip,
            "server-port": server_port,
            "server-size": server_size
        }
        config = dumps(config)
        data.write(config)


def get_json_data():
    try:
        with open("config.json", "r") as data:
            data = data.read()
            data = loads(data)
            return data
    except FileNotFoundError:
        generate_json_data()


def broadcast_data(clients, data, sender):
    for client in clients:
        if client != sender:
            client.send(data)


def add_new_client(client):
    if not (client in clients):
        clients.append(client)


def handle_client(client):
    while True:
        data = client.recv(1024)
        broadcast_data(clients, data, client)
        data = loads(data)
        message = data["message"]
        if message[0] == "!":
            message = message[0:]
            if message == "exit":
                clients.remove(client)
                client.close()
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


data = get_json_data()

try:
    start_server(data["server-ip"], data["server-port"], data["server-size"])
except TypeError:
    data = get_json_data()
    start_server(data["server-ip"], data["server-port"], data["server-size"])
except KeyError:
    default_arguments = ["server-ip", "server-port", "server-size"]
    missin_arguments = list(default_arguments-data.keys())
    for i in missin_arguments:
        print(f"Missing Argument: {i}")
