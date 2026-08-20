from client_management.lock import state_lock
from client_management.ban_handler import add_ban

clients = []
nicknames = []

def clean_up_client(client, disconect_msg):
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
        print(f"Client {nickname} {disconect_msg}!")
        broadcast(f"{nickname} left the chat!\n",sender=client)


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
                clean_up_client(client, "disconnected")

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
            clean_up_client(client, "disconnected")
            break
