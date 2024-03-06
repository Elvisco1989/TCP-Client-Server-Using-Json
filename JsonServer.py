import socket
import random
import threading
import json

Header = 1024
ServerPort = 9090
ServerName = socket.gethostbyname(socket.gethostname())
Address = (ServerName, ServerPort)

Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Server.bind(Address)

Server.listen()
print(f"[LISTENING] Server is listening on {ServerName}")

def handle_input_numbers(ClientConn):
    numbers_json = ClientConn.recv(Header).decode()
    try:
        numbers = json.loads(numbers_json)
        if len(numbers) == 2:
            return map(int, numbers)
        else:
            raise ValueError("Invalid number of inputs")
    except ValueError as e:
        print("Error:", e)
        return None, None


def handle_client(ClientConn):
    while True:
        try:
            command_json = ClientConn.recv(Header).decode()
            command_data = json.loads(command_json)
            if not command_data:
                break
            method = command_data.get('method', '')
            if method == "Random":
                ClientConn.send("Input numbers".encode())
                numbers_json = ClientConn.recv(Header).decode()
                numbers = json.loads(numbers_json)
                if len(numbers) == 2:
                    num1, num2 = map(int, numbers)
                    result = random.randint(num1, num2)
                    ClientConn.send(json.dumps({"result": result}).encode())
            elif method in ["Add", "Subtract"]:
                ClientConn.send("Input numbers".encode())
                numbers_json = ClientConn.recv(Header).decode()
                numbers = json.loads(numbers_json)
                if len(numbers) == 2:
                    num1, num2 = map(int, numbers)
                    if method == "Add":
                        result = num1 + num2
                    else:
                        result = num1 - num2
                    ClientConn.send(json.dumps({"result": result}).encode())
            else:
                ClientConn.send(json.dumps({"error": "Invalid method"}).encode())
        except json.JSONDecodeError:
            ClientConn.send(json.dumps({"error": "Invalid JSON format"}).encode())
        except Exception as e:
            print("Error:", e)
            break

# Accept incoming connections and handle clients
while True:
    ClientConn, Address = Server.accept()
    print(f"Connected by {Address}")
    client_handler = threading.Thread(target=handle_client, args=(ClientConn,))
    client_handler.start()







