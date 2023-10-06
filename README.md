# PythonBackDoor
 
## Description
A simple BackDoor written in python and served to the user via a flask frontend.


## Features
- Listen for incoming clients to connect to the server on a specific port and IP
- Browse the clients file system
- Download files from the client system 
- Send files to the client system


## Installation
The easiest way to set up the server and client is via Docker.\
Both server and client are deployed to the 
[xlinus41](https://hub.docker.com/u/xlinus41) 
repository on Docker Hub\
*Keep in mind that the image for the server with a flask frontend is called **python_backdoor_server_flask***\
This docker-compose.yml creates a server and client.
1. Create docker-compose.yml
```
services:
    server:
        image: "xlinus41/python_backdoor_server_flask"
        container_name: bd_sv
        environment:
            - BD_HOST=bd_sv
            - BD_PORT=8086
        ports:
          - "5000:5000"
        stdin_open: true
        tty: true
    client:
        image: "xlinus41/python_backdoor_client_flask"
        environment:
            - BD_HOST=bd_sv
            - BD_PORT=8086
```
2. Run this command 
```
docker compose up -d
```

The 