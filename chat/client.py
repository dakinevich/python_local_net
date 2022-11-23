import socket
import threading

def thread_sending():
    while True:
        message_to_send = input()
        if message_to_send:
            try:
                client_sock.send(message_to_send.encode())
            except:
                print("so sad")
                break
        
def thread_receiving():
    while True:
        try:
            message = client_sock.recv(1024).decode()
            print(f"{message}")
        except:
            print("!server disconected")
            break


HOST = socket.gethostbyname(socket.gethostname())
PORT = 12768

if HOST.startswith("127"):
    print(f"localhost")
print(f"HOST: {HOST}\nPORT: {PORT}")

  
client_sock = socket.socket()
try:
    client_sock.connect((HOST, PORT))
    print(f"CLIENT INDEX: {client_sock.recv(1024).decode()}\n")
    client_sock.recv(1024).decode() # skip connection messange
    thread_send = threading.Thread(target=thread_sending)
    thread_receive = threading.Thread(target=thread_receiving)
    thread_send.start()
    thread_receive.start()
    thread_receive.join()

except:
    print("\n!server not found")

client_sock.close()