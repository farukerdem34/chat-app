import socket
import argparse


def send_message():
    while True:
        message = input("Enter a message: ")
        client.send(message.encode())
        if message == "exit":
            break

    client.close()

def get_user_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--destination",help="Destination server IP address.",dest="dest")
    parser.add_argument("-p","--port",help="Server port number.",dest="port")
    args = parser.parse_args()
    return args

args = get_user_input()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((args.dest, args.port))

send_message()
