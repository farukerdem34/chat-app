import socket
import argparse
import threading


def receive_messages():
    while True:
        message = client.recv(1024).decode()
        print(f"{message}\n")
        if message == "exit":
            break

    client.close()

# @TODO Send messages with base64
def send_message():
    while True:
        message = input("Enter a message: ")
        client.send(message.encode())
        if message == "exit":
            break

    client.close()


def get_user_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--destination",
                        help="Destination server IP address.", dest="dest")
    parser.add_argument(
        "-p", "--port", help="Server port number.", dest="port")
    args = parser.parse_args()
    return args


args = get_user_input()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((str(args.dest), int(args.port)))

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_message()
