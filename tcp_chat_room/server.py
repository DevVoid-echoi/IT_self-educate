import threading
import socket
import os
import sys

host = "127.0.0.1"  # local_host
port = 9999

state_lock = threading.Lock()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BAN_FILE_PATH = os.path.join(SCRIPT_DIR, "ban.txt")

def get_banned_users():
    if not os.path.exists(BAN_FILE_PATH):
        return []
    with open(BAN_FILE_PATH, 'r', encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]

def add_ban(nickname):
    with open(BAN_FILE_PATH, 'a', encoding="utf-8") as f:
        f.write(f"{nickname}\n")

def broadcast(message, sender=None):
    if isinstance(message, str):
        message = message.encode("utf-8")

    with state_lock:
        targets = list(clients)

    disconnected_clients = []

    for client in targets:
        if client != sender:
            try:
                client.sendall(message)
            except (BrokenPipeError, ConnectionResetError, OSError) as e:
                print(f"Error sending message: {e}")
                disconnected_clients.append(client)
    for client in disconnected_clients:
        with state_lock:
            if client in clients:
                index = clients.index(client)
                nickname = nicknames.pop(index)
                clients.pop(index)
            else:
                nickname = None

        try:
            client.close()
        except OSError:
            pass

        if nickname:
            print(f"Removed disconnected client '{nickname}'.")

def kick_user(name):
    client_to_kick = None
    with state_lock:
        if name in nicknames:
            index = nicknames.index(name)
            client_to_kick = clients.pop(index)
            nicknames.pop(index)

    if client_to_kick:
        try:
            client_to_kick.send("You were kicked by an admin!".encode("utf-8"))
            client_to_kick.close()
        except Exception:
            pass
        broadcast(f"{name} was kicked by an admin!".encode('utf-8'))

def handle(client):
    while True:
        try:
            data = client.recv(4096)

            if not data:
                with state_lock:
                    if client in clients:
                        index = clients.index(client)
                        nickname = nicknames.pop(index)
                        clients.pop(index)
                    else:
                        nickname = None

                try:
                    client.close()
                except OSError:
                    pass

                if nickname:
                    print(f"Client '{nickname}' disconnected.")
                    broadcast(
                        f"{nickname} left the chat!\n",
                        sender=client
                    )

                break


            message = data.decode('utf-8', errors="ignore").strip()

            with state_lock:
                current_nick = (
                    nicknames[clients.index(client)] if client in clients
                    else None
                )

            if not current_nick:
                break

            if message.startswith('KICK '):
                if current_nick == "admin":
                    name_to_kick = message[5:].strip()
                    if name_to_kick:
                        kick_user(name_to_kick)
                else:
                    client.send("Command was refused!".encode('utf-8'))
                continue

            if message.startswith('BAN '):
                if current_nick == "admin":
                    name_to_ban = message[4:].strip()
                    if name_to_ban:
                        add_ban(name_to_ban)
                        kick_user(name_to_ban)
                        print(f'{name_to_ban} was banned!')
                else:
                    client.send("Command was refused!".encode('utf-8'))
                continue

            if message:
                broadcast(message, sender=client)

        except (ConnectionResetError, BrokenPipeError, OSError) as e:

            with state_lock:
                if client in clients:
                    index = clients.index(client)
                    nickname = nicknames.pop(index)
                    clients.pop(index)
                else:
                    nickname = None

            try:
                client.close()
            except OSError:
                pass

            if nickname:
                print(f"Client '{nickname}' disconnected unexpectedly.")

                broadcast(
                    f"{nickname} left the chat!\n",
                    sender=client
                )

            break

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

            if password != "admin123":
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
    receive()
except KeyboardInterrupt:
    print("\nServer is shutting down...")
    for client in clients:
        client.close()
    server.close()
    sys.exit()
