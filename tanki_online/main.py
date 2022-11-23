import threading
import socket
import time
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


def game_thread():
    global running
    global POS
    global DRAW_QUEUE
    pygame.init()
    screen = pygame.display.set_mode([500, 500])
    pygame.display.set_icon(pygame.Surface([0, 0]))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((5, 5, 5))

        POS = pygame.mouse.get_pos()
        for pos in DRAW_QUEUE:
            pygame.draw.circle(screen, (255, 255, 255), pos, 3)
            
        pygame.display.flip()

    pygame.quit()

def accept_loop():
    while True:
        try:
            host_sock.listen()
            client, addr = host_sock.accept()
            print(f"client {client.fileno()} has been connected")
            broadcast_list.append(client)
            client.send(str(client.fileno()).encode())
        except:
            break

def swap_thread_server():
    global POS
    global DRAW_QUEUE
    while True:
        local_broadcast = broadcast_list
        new_queue = [POS]
        #time.sleep(1)
        for client in local_broadcast:
            try:
                messange = ' '.join([f"{i[0]} {i[1]}" for i in DRAW_QUEUE])
                client.send(messange.encode())
                messange = client.recv(1024).decode()
                new_queue.append([int(i) for i in messange.split(" ")])
            except:
                for i in range(len(broadcast_list)):
                    if broadcast_list[i].fileno() == client.fileno():
                        broadcast_list.pop(i)
                        print(f"client {client.fileno()} has been disconnected")
                        break
        DRAW_QUEUE = new_queue

def swap_thread_client():
    global POS
    global DRAW_QUEUE
    global running
    while True:
        try:
            messange = client_sock.recv(1024).decode()
            int_messange = [int(i) for i in messange.split(" ")]
            DRAW_QUEUE = [int_messange[j*2:j*2+2] for j in range(int(len(int_messange)/2))]
            client_sock.send(f"{POS[0]} {POS[1]}".encode())
        except:
            print("DISCONNECTED")
            running = False
            break


HOST = socket.gethostbyname(socket.gethostname())
PORT = 12768
POS = [0, 0]
DRAW_QUEUE = [POS]
running = True

if HOST.startswith("127"):
    print(f"localhost")
print(f"\nHOST: {HOST}\nPORT: {PORT}\n")
while True:
    try:
        SERVER = bool(int(input("server? (0/1): ")))
        break
    except:
        print("incorrect input, type 0 or 1")

if SERVER:
    host_sock = socket.socket()
    broadcast_list = []
    try:
        host_sock.bind((HOST, PORT))
    except:
        print("PORT IS ALREADY BUSY")
        exit()
    print("SERVER\n")
    pygame.display.set_caption('server')

    thread_game = threading.Thread(target=game_thread, daemon=True)
    thread_swap = threading.Thread(target=swap_thread_server, daemon=True)
    thread_accept = threading.Thread(target=accept_loop, daemon=True)
    thread_game.start()
    thread_accept.start()
    thread_swap.start()

    thread_game.join()
    host_sock.close()
    print("\nDISCONNECTED")
else:
    client_sock = socket.socket()
    try:
        client_sock.connect((HOST, PORT))
        index = client_sock.recv(1024).decode()
        print(f"CONNECTED\nCLIENT INDEX: {index}\n")
        pygame.display.set_caption(f'client {index}')
        thread_swap = threading.Thread(target=swap_thread_client, daemon=True)
        thread_game = threading.Thread(target=game_thread, daemon=True)

        thread_game.start()
        thread_swap.start()

        thread_game.join()

    except:
        print("\n!server not found")

    client_sock.close()

