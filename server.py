import threading
import socket
from json import loads, dumps
import argparse


clients = []

def generate_json_data():
    with open("config.json","w") as data:
        server_ip = str(input("Enter server IP: "))
        try:
            server_port = int(input("Enter server port: "))
        except ValueError:
            print("Enter integer!")
            server_port = int(input("Enter server port: "))
        config = {
            "server-ip":server_ip,
            "server-port":server_port
        }
        config = dumps(config)
        data.write(config)

def get_json_data():
    try:
        with open("config.json","r") as data:
            data = data.read()
            data = loads(data)
            return data
    except FileNotFoundError:
        generate_json_data()
        get_json_data()
    

def get_user_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--user-size",
                        help="Maximum user size.", dest="usersize", default=3)
    args = parser.parse_args()
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

data = get_json_data()
start_server(data["server-ip"], data["server-port"], args.usersize)
