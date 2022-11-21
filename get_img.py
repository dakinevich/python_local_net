#client.py
import socket
import numpy as np
from PIL import Image

def from_16(a):
    s = 0
    alph = "0123456789abcdef"
    while a:
        s*=16
        s+=alph.index(a[0])
        a = a[1:]
    return s

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "192.168.1.3"
port = 6045
my_socket.connect((host, port))
        
message = my_socket.recv(2048).decode()
w, h, d, banch = [int(i) for i in message.split(" ")]
np_img = np.zeros((w, h, d), dtype=np.uint8)
get_banch = ""
for ix in range(w):
    if ix%100 == 0:
            print(str(int(100*ix/w)/100)+"%")
    for iy in range(h):
        print(ix, iy)
        if len(get_banch) == 0:
            print("before")
            get_banch += my_socket.recv(1024).decode()
            print("after")
        np_img[ix][iy] = np.array([from_16(get_banch[i*2: i*2 +2]) for i in range(3)])
        get_banch = get_banch[6:]
img = Image.fromarray(np_img)
img.save("result.png")