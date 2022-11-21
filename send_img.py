import socket, select

image = "test.png"

HOST = "192.168.1.3"
PORT = 6045

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)

sock.connect(server_address)


myfile = open(image, "rb")
bytes = myfile.read()
size = len(bytes)

sock.sendall((f"SIZE {size}").encode())
answer = sock.recv(4096)


if answer.decode() == "GOT SIZE":
    sock.sendall(bytes)

myfile.close()
sock.close()