import pygame
import threading
import socket

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

def swap_thread():
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
       
DRAW_QUEUE = []
POS = [0, 0]
HOST = socket.gethostbyname(socket.gethostname())
PORT = 12768
running = True

if HOST.startswith("127"):
    print(f"localhost")
print(f"HOST: {HOST}\nPORT: {PORT}")

  
client_sock = socket.socket()
try:
    client_sock.connect((HOST, PORT))
    index = client_sock.recv(1024).decode()
    print(f"CONNECTED\nCLIENT INDEX: {index}\n")
    pygame.display.set_caption(f'client {index}')
    thread_swap = threading.Thread(target=swap_thread, daemon=True)
    thread_game = threading.Thread(target=game_thread, daemon=True)

    thread_game.start()
    thread_swap.start()

    thread_game.join()

except:
    print("\n!server not found")

client_sock.close()
