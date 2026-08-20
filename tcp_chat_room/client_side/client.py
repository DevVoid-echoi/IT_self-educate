import threading
import socket
import sys
import os

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PARENT_DIR not in sys.path:
    sys.path.append(PARENT_DIR)

from config import HOST,PORT
from client_management.instructions import print_instructions
from client_management.connection import receive, write

def main():
    nickname = input("Choose a nickname: ")
    password=""

    if nickname == "admin":
        password = input("Enter password for admin: ").strip()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    print_instructions(nickname)

    receive_thread = threading.Thread(
        target=receive, 
        args=(client, nickname, password),
        daemon=True
    )
    receive_thread.start()

    write(client, nickname)

    sys.stdout.write("\r\033[K")
    sys.stdout.flush()
    sys.exit(0)

if __name__ == "__main__":
    main()
