import socket
import argparse
import threading
from json import loads, dumps
from json.decoder import JSONDecodeError


def receive_messages():
    while True:
        try:
            data = client.recv(1024)
            data = loads(data)
            username = data["username"]
            message = data["message"]
            print("\n"+username + ": " + message)
        except ConnectionAbortedError:
            client.close()
            break
        except OSError:
            client.close()
            break


def send_message(username):
    while True:
        try:
            message = input()
        except KeyboardInterrupt:
            client.close()
        if message[0] == "!":
            message = message[0:]
            if message == "exit":
                client.close()
                break
        else:
            data = {
                "message": message,
                "username": username
            }
            data = dumps(data).encode("utf-8")
            try:
                client.send(data)
            except OSError:
                client.close()
                break


def get_user_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--destination",
                        help="Destination server IP address.", dest="dest")
    parser.add_argument(
        "-p", "--port", help="Server port number.", dest="port")
    parser.add_argument("-u", "--username", help="Username.", dest="username")
    args = parser.parse_args()
    return args


args = get_user_input()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((str(args.dest), int(args.port)))

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_message(args.username)
