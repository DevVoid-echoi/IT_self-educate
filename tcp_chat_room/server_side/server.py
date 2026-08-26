import threading
import socket
import os
import sys

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PARENT_DIR not in sys.path:
    sys.path.append(PARENT_DIR)

from config import HOST, PORT, SCRIPT_DIR, BAN_FILE_PATH
from client_management.lock import state_lock
from client_management.ban_handler import get_banned_users, add_ban
from client_management.actions import clients, nicknames, read_line, broadcast, kick_user, handle_messages, clean_up_client, user_sessions
from auth.authentication import login, register, set_user_role

"""Connect using IPv4 and TCP"""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

def receive():
    """Receive message from clients"""
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}") # Kết nối với client ở địa chỉ "address"

        buffer = ""
        session = None

        # --- AUTHENTICATION ---
        while not session:
            line, buffer = read_line(client, buffer)
            if not line:
                break
            
            """Check for valid login information"""
            if line.startswith("LOGIN "):
                parts = line.split(" ", 2)
                if len(parts) == 3:
                    _, username, password = parts
                    success, user_session = login(username, password)
                    if success:
                        session = user_session
                    else:
                        client.send("ERR WRONG_AUTH\n".encode("utf-8")) # Decline due to wrong information
                        continue
                else:
                    client.send("ERR INVALID_FORMAT\n".encode("utf-8"))
                    continue

            """Register new users"""
            if line.startswith("REGISTER "):
                parts = line.split(" ", 2)
                if len(parts) == 3:
                    _, username, password = parts
                    success, msg = register(username, password)
                    if success:
                        client.send(f"OK {msg}\n".encode("utf-8")) # Send OK message if succeess
                    else:
                        client.send(f"ERR {msg}\n".encode("utf-8")) # Show error message
                else:
                    client.send("ERR INVALID_FORMAT\n".encode("utf-8"))
                continue
        
        # Nếu không có session (Client chủ động ngắt kết nối)
        if not session:
            client.close()
            continue
                
        nickname = session["username"]

        # --- Check connect conditions ---
        # Check whether the username has been used
        with state_lock:
            if nickname in nicknames:
                client.send("ERR ALREADY_LOGGED_IN\n".encode("utf-8"))
                client.close()
                continue

        # Check if the user is banned
        banned_users = get_banned_users()
        if nickname in banned_users:
            client.send("ERR BANNED\n".encode('utf-8'))
            client.close()
            continue

        with state_lock:
            clients.append(client)
            nicknames.append(nickname)
            user_sessions[client] = session

        # --- Succeed and start threads ---
        print(f"User '{nickname}' ({session['role']}) connected successfully!")
        client.send(f"OK Connected as {nickname}\n".encode("utf-8"))
        broadcast(f"MSG {nickname} joined the chat!\n".encode("utf-8"), sender=client)

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
