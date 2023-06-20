class Client:
    pwd = None
    addr = None
    socket = None
    output = []

    def __init__(self, pwd, addr, socket):
        self.pwd = pwd
        self.addr = addr
        self.socket = socket

    def append_output(self, cmd):
        cmd = str(cmd)
        for l in cmd.splitlines():
            self.output.append(l)

class MemFile:
    name = None
    data = None

    def __init__(self, name, data):
        self.name = name
        self.data = data

