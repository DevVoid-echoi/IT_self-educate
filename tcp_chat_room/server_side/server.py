import threading
import socket
import os
import sys

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PARENT_DIR not in sys.path:
    sys.path.append(PARENT_DIR)

from config import HOST, PORT, SCRIPT_DIR, BAN_FILE_PATH, ADMIN_PASSWORD
from client_management.lock import state_lock
from client_management.ban_handler import get_banned_users, add_ban
from client_management.actions import clients, nicknames, broadcast, kick_user, handle

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(4096).decode('utf-8', errors='replace').strip()

        if ("HTTP/" in nickname 
            or "HEAD" in nickname
            or "GET" in nickname
            or len(nickname) > 30
            or len(nickname) == 0):
            print(f"Denied connection from: {address}")
            client.close()
            continue

        with state_lock:
            if nickname in nicknames:
                client.send("NICK_TAKEN".encode("utf-8"))
                client.close()
                continue

        banned_users = get_banned_users()
        if nickname in banned_users:
            client.send("BAN".encode('utf-8'))
            client.close()
            continue
        
        if nickname == 'admin':
            client.send('PASS'.encode('utf-8'))
            password = client.recv(4096).decode('utf-8', errors='replace').strip()

            if password != ADMIN_PASSWORD:
                client.send('REFUSE'.encode('utf-8'))
                client.close()
                continue

        with state_lock:
            clients.append(client)
            nicknames.append(nickname)

        print(f"Nickname of the client is {nickname}!")
        broadcast(f"{nickname} joined the chat!".encode('utf-8'), sender=client)
        client.send("Connected to the server!\n".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

try:
    print(f"Server is running on {HOST}:{PORT}...")
    receive()
except KeyboardInterrupt:
    print("\nServer is shutting down...")
    for client in clients:
        client.close()
    server.close()
    sys.exit()
