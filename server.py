import socket, select
 
basename = "image_got.png"

HOST = "192.168.1.3"
PORT = 6045

connected_clients_sockets = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(10)

connected_clients_sockets.append(server_socket)

while True:

    read_sockets, write_sockets, error_sockets = select.select(connected_clients_sockets, [], [])

    for sock in read_sockets:

        if sock == server_socket:
            
            sockfd, client_address = server_socket.accept()
            connected_clients_sockets.append(sockfd)
            print("client apended")

        else:
            sock.settimeout(0.1)
            data = sock.recv(4096)
            txt = data.decode()
            tmp = txt.split()
            size = int(tmp[1])
            print(f"sock sended size: {size}")
            sock.sendall(b"GOT SIZE")
            myfile = open(basename, "wb")
            sock.settimeout(0)
            data = sock.recv(size)
            myfile.write(data)
            myfile.close()
            sock.close()
            connected_clients_sockets.remove(sock)
server_socket.close()