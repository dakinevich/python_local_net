import pygame
import threading
import socket
import time

def game_thread():
    global POS
    global DRAW_QUEUE
    pygame.init()
    screen = pygame.display.set_mode([500, 500])
    pygame.display.set_caption('server')
    pygame.display.set_icon(pygame.Surface([0, 0]))

    running = True  

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
       
        

def swap_thread():
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

HOST = socket.gethostbyname(socket.gethostname())
PORT = 12768
POS = [0, 0]
DRAW_QUEUE = [POS]


if HOST.startswith("127"):
    print(f"localhost")
print(f"HOST: {HOST}\nPORT: {PORT}\nSERVER\n")

host_sock = socket.socket()
broadcast_list = []
host_sock.bind((HOST, PORT))

thread_game = threading.Thread(target=game_thread, daemon=True)
thread_swap = threading.Thread(target=swap_thread, daemon=True)
thread_accept = threading.Thread(target=accept_loop, daemon=True)
thread_game.start()
thread_accept.start()
thread_swap.start()

thread_game.join()
host_sock.close()
print("DISCONNECTED")
exit()
