#server.py
import socket
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT = 6045
ADDRESS = "172.20.10.12"
my_socket.bind((ADDRESS, PORT))
my_socket.listen()
client, client_address = my_socket.accept()
result = client.recv(1024)
print(result.decode())