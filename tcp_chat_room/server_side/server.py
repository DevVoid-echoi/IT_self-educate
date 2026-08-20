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
from client_management.actions import clients, nicknames, read_line, broadcast, kick_user, handle_messages, clean_up_client

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        buffer = ""
        line, buffer = read_line(client, buffer)
        if not line or not line.startswith("NICK "):
            client.close()
            continue

        nickname = line[5:].strip()

        if (len(nickname) > 30 or len(nickname) == 0):
            client.send("ERR INVALID_NICK\n".encode("utf-8"))
            print(f"Denied connection from: {address}")
            client.close()
            continue

        with state_lock:
            if nickname in nicknames:
                client.send("ERR NICKNAME_TAKEN\n".encode("utf-8"))
                client.close()
                continue

        banned_users = get_banned_users()
        if nickname in banned_users:
            client.send("ERR BANNED\n".encode('utf-8'))
            client.close()
            continue
        
        if nickname == 'admin':
            client.send('AUTH_REQUIRED\n'.encode('utf-8'))
            line, buffer = read_line(client, buffer)
            if not line or not line.startswith("AUTH "):
                client.close()
                continue

            password = line[5:].strip()

            if password != ADMIN_PASSWORD:
                client.send('ERR WRONG_PASSWORD\n'.encode('utf-8'))
                client.close()
                continue

        with state_lock:
            clients.append(client)
            nicknames.append(nickname)

        print(f"Nickname of the client is {nickname}!")
        broadcast(f"MSG {nickname} joined the chat!\n".encode('utf-8'), sender=client)
        client.send("OK Connected to the server!\n".encode('utf-8'))

        thread = threading.Thread(target=handle_messages, args=(client,), daemon=True)
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
