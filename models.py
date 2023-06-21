class Client:
    files = []

    def __init__(self, pwd, addr, socket):
        self.pwd = pwd
        self.addr = addr
        self.socket = socket
        self.output = ["Enter help for help"]
        self.files = []

    def append_output(self, cmd, out):
        out = str(out)
        self.output.append(">> " + cmd)
        for l in out.splitlines():
            self.output.append(l)

    def add_file(self, file):
        self.files.append(file)

    def get_file_by_name(self, filename):
        for f in self.files:
            if f.name == filename:
                return f
        return None


class MemFile:
    def __init__(self, name, data):
        self.name = name
        self.data = data
