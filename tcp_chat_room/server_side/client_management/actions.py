from client_management.lock import state_lock
from client_management.ban_handler import add_ban

clients = []
nicknames = []

def read_line(sock, buffer):
    """Read full-line messages"""
    while not "\n" in buffer:
        try:
            chunk = sock.recv(4096).decode("utf-8", errors="replace")
            if not chunk:
                return None, buffer
            buffer += chunk
        except(ConnectionResetError, BrokenPipeError, OSError):
            return None, buffer

    line, buffer = buffer.split("\n", 1)
    return line.strip(), buffer

def clean_up_client(client, disconect_msg):
    """Clean up disconnected users"""
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

    if nickname: # Print annoucement that the disconnected user left the chat
        print(f"Client {nickname} {disconect_msg}!")
        broadcast(f"MSG {nickname} left the chat!\n",sender=client)


def broadcast(message, sender=None):
    """Broadcast the message to all other users"""
    if isinstance(message, str):
        message = message.encode("utf-8") # Encode the message

    with state_lock:
        targets = list(clients) # Get the list of user

    disconnected_clients = []

    for client in targets:
        if client != sender:
            try:
                client.sendall(message) # Send the message to all users except for the sender
            except (BrokenPipeError, ConnectionResetError, OSError) as e:
                print(f"Error sending message: {e}")
                disconnected_clients.append(client) # Disconnect the user if get an error while sending the message
    for client in disconnected_clients:
        clean_up_client(client, "disconnected") "Clean up the disconnected client"

def kick_user(name):
    """Remove the user in kick command"""
    client_to_kick = None
    with state_lock:
        if name in nicknames:
            index = nicknames.index(name)
            client_to_kick = clients.pop(index)
            nicknames.pop(index)

    if client_to_kick:
        try:
            # Print the kick announcement and close the connection of the kicked user
            client_to_kick.send("MSG You were kicked by an admin!\n".encode("utf-8"))
            client_to_kick.close()
        except Exception:
            pass
        broadcast(f"MSG {name} was kicked by an admin!\n".encode('utf-8')) # Send the announcement to all users

def handle_messages(client):
    """Handle received messages from users"""
    buffer = ""
    while True:
        line, buffer = read_line(client, buffer)
        """Clean up disconnected user if not receive any message"""
        if line is None:
            clean_up_client(client, "disconnected")
            break

        with state_lock:
            current_nick = (
                nicknames[clients.index(client)] if client in clients
                else None
            )

        if not current_nick:
            break

        """Check if the user is admin and remove the target user"""
        if line.startswith('KICK '):
            if current_nick == "admin":
                name_to_kick = line[5:].strip()
                if name_to_kick:
                    kick_user(name_to_kick)
            else:
                client.send("MSG Command was refused!\n".encode('utf-8')) # Refused command if not admin
            continue

        """Check if the user is admin and ban the target user"""
        if line.startswith('BAN '):
            if current_nick == "admin":
                name_to_ban = line[4:].strip()
                if name_to_ban:
                    add_ban(name_to_ban)
                    kick_user(name_to_ban)
                    print(f'{name_to_ban} was banned!')
            else:
                client.send("MSG Command was refused\n!".encode('utf-8')) # Refused command if not admin
            continue

        """Broadcast the normal message"""
        if line.startswith("MSG" ):
            content = line[4:]
            broadcast(f"MSG {current_nick}: {content}\n".encode("utf-8"), sender=client)
