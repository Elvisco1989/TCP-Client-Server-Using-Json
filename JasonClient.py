import socket
import json
import sys

Header = 1024
ServerPort = 9090
ServerName = socket.gethostbyname(socket.gethostname())
Address = (ServerName, ServerPort)

Clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Clientsocket.connect(Address)

def send_command(cmd):
    json_cmd = json.dump(cmd)
    Clientsocket.sendall(json_cmd.encode())
    server_response = Clientsocket.recv(1024).decode('utf-8')
    decoded_response = json.load(server_response) 
                  


