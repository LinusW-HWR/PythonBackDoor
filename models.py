class Client:
    pwd = None
    addr = None
    socket = None
    output = []
    files = []

    def __init__(self, pwd, addr, socket):
        self.pwd = pwd
        self.addr = addr
        self.socket = socket

    def append_output(self, cmd):
        cmd = str(cmd)
        for l in cmd.splitlines():
            self.output.append(l)

    def add_file(self, file):
        self.files.append(file)

    def get_file_by_name(self, filename):
        for f in self.files:
            if f.name == filename:
                return f
        return None


class MemFile:
    name = None
    data = None

    def __init__(self, name, data):
        self.name = name
        self.data = data

