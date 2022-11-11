#client.py
import socket
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "172.20.10.12"
port = 6045
my_socket.connect((host, port))
my_socket.send("hello".encode())