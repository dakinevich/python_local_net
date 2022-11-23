#server.py
import socket
import threading
host_sock = socket.socket()

HOST = socket.gethostbyname(socket.gethostname())
PORT = 12768

if HOST.startswith("127"):
    print(f"localhost")
print(f"HOST: {HOST}\nPORT: {PORT}\nSERVER\n")

broadcast_list = []
host_sock.bind((HOST, PORT))
def accept_loop():
    while True:
        host_sock.listen()
        client, addr = host_sock.accept()
        broadcast_list.append(client)
        client.send(str(client.fileno()).encode())
        broadcast(f"client {client.fileno()} added", "server")
        start_listenning_thread(client)
        
def start_listenning_thread(client):
    client_thread = threading.Thread(
            target=listen_thread,
            args=(client,)
        )
    client_thread.start()
    
def listen_thread(client):
    while True:
        try:
            message = client.recv(1024).decode()
            broadcast(message, client.fileno())
        except:
            for i in range(len(broadcast_list)):
                if broadcast_list[i].fileno() == client.fileno():
                    broadcast(f"client {client.fileno()} has been disconnected", "server")
                    broadcast_list.pop(i)
                    break
        
def broadcast(content, sender):
    message = f"{sender}: {content}"
    print(message)
    for client in broadcast_list:
        try:
            client.send(message.encode())
        except:
            pass #wtf

def thread_sending():
    while True:
        message_to_send = input()
        if message_to_send:
            broadcast(message_to_send, "server")

thread_accept = threading.Thread(target=accept_loop)
thread_send = threading.Thread(target=thread_sending)
thread_accept.start()
thread_send.start()
