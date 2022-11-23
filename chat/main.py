import threading
import time
def read():
    while True:
        print(c)

def modify():
    while True:
        c[1] = int(time.time())%10 # but if new link it brokes
c = [1,2,4]
t1 = threading.Thread(target=read)
t2 = threading.Thread(target=modify)
t1.start()
t2.start()




