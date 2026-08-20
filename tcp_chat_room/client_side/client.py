import threading
import socket
import sys
import os

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PARENT_DIR not in sys.path:
    sys.path.append(PARENT_DIR)

from config import HOST,PORT
from client_management.instructions import print_instructions
from client_management.connection import receive, write, read_line

def main():
    nickname = input("Choose a nickname: ")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    client.send(f"NICK {nickname}\n".encode("utf-8"))
    
    buffer = ""
    line, buffer = read_line(client, buffer)

    if line == "AUTH_REQUIRED":
        password = input("Enter admin password: ").strip()
        client.send(f"AUTH {password}\n".encode("utf-8"))
        line, buffer = read_line(client, buffer)

    if not line or line.startswith("ERR "):
        msg = line[4:]
        print(f"Connection refused: {msg}")
        client.close()
        sys.exit(1)

    print_instructions(nickname)

    receive_thread = threading.Thread(
        target=receive, 
        args=(client, nickname),
        daemon=True
    )
    receive_thread.start()

    write(client, nickname)

    sys.stdout.write("\r\033[K")
    sys.stdout.flush()
    sys.exit(0)

if __name__ == "__main__":
    main()
