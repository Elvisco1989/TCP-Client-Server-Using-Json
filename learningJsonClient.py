    
import socket
import json

Header = 1024
ServerPort = 4545
ServerName = socket.gethostbyname(socket.gethostname())
Address = (ServerName, ServerPort)

Clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Clientsocket.connect(Address)


def send_command(cmd):
    json_object = json.dumps(cmd)
    Clientsocket.sendall(json_object.encode())
    server_response = Clientsocket.recv(Header).decode('utf-8')
    if not server_response:
        return {}
    decoded_response = json.loads(server_response)
    return decoded_response

while True:
    user_input = input("Enter Either Random, Add, Subtract in JSON format: ")
    try:
        json_object = json.loads(user_input) 
    except json.JSONDecodeError:
        print("Invalid JSON format. Please try again.")
        continue
    
    response = send_command(json_object)
    print(response)  

    if response.get("prompt") == "Input numbers":
    
        print("Enter two numbers separated by space in JSON format:")
        numbers_input = input()
        try:
            numbers = json.loads(numbers_input) 
            if isinstance(numbers, list) and len(numbers) == 2:
                
                response = send_command(numbers)
                print(response)  
            else:
                print("Invalid input. Please enter a list containing two numbers.")
        except json.JSONDecodeError:
            print("Invalid JSON format. Please try again.")