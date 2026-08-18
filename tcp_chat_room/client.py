import threading
import socket
import sys

nickname = input("Choose a nickname: ")
password=""

if nickname == "admin":
    password = input("Enter password for admin: ").strip()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 9999))

print("-" * 50)
print(" HƯỚNG DẪN CHAT:")
print(" - Nhập tin nhắn và bấm Enter để gửi.")
print(" - Gõ '/quit' hoặc '/exit' để rời phòng chat.")
if nickname == "admin":
    print(" - Gõ /kick <user_name> để đuổi người dùng khỏi phòng chat")
    print(" - Gõ /ban <user_name> để cấm người dùng vào phòng chat")
print("-" * 50)

stop_threads = False

def receive():
    global stop_threads
    while not stop_threads:
        try:
            message = client.recv(4096).decode('utf-8', errors='replace')
            if not message:
                sys.stdout.write("\r\033[KServer closed connection.\n")
                sys.stdout.flush()
                stop_threads = True
                client.close()
                break
            
            if message == "NICK":
                client.send(nickname.encode('utf-8'))
                continue

            elif message == "PASS":
                client.send(password.encode('utf-8'))
                continue

            elif message == "BAN":
                sys.stdout.write("\r\033[KYou are banned from this server!\n")
                sys.stdout.flush()
                stop_threads = True
                client.close()
                break
            
            elif message == "REFUSE":
                sys.stdout.write("\r\033[KWrong password! Connection refused.\n")
                sys.stdout.flush()
                stop_threads = True
                client.close()
                break
            
            else:
                sys.stdout.write(f"\r\033[K{message}\n")
                sys.stdout.write(f"{nickname}: ")
                sys.stdout.flush()

        except Exception as e:
            if not stop_threads:
                sys.stdout.write(f"\r\033[KConnection error: {e}\n")
                sys.stdout.flush()
                stop_threads = True
                client.close()
            break

def write():
    global stop_threads
    while not stop_threads:
        try:
            user_input = input(f"{nickname}: ")
            cmd = user_input.strip()

            if cmd.lower() in ["/quit", "/exit"]:
                stop_threads = True
                sys.stdout.write("\r\033[KDisconnecting from server...\n")
                sys.stdout.flush()
                client.close()
                break

            if cmd.lower().startswith("/kick"):
                if nickname == "admin":
                    target_user = cmd[6:].strip()
                    if not target_user:
                        print("Usage: /kick <username>")
                        continue
                    client.send(f"KICK {target_user}".encode('utf-8'))
                else:
                    print("Command can only be executed by the admin!")
                continue

            if cmd.lower().startswith("/ban"):
                if nickname == "admin":
                    target_user = cmd[6:].strip()
                    if not target_user:
                        print("Usage: /ban <username>")
                        continue
                    client.send(f"BAN {target_user}".encode('utf-8'))
                else:
                    print("Command can only be executed by the admin!")
                continue

            if cmd:
                message = f"{nickname}: {user_input}\n"
                client.send(message.encode('utf-8'))

        except (KeyboardInterrupt, EOFError):
            stop_threads = True
            sys.stdout.write("\r\033[K[!] Exiting via keyboard shortcut...\n")
            sys.stdout.flush()
            client.close()
            break

        except Exception as e:
            sys.stdout.write(f"\r\033[KError: {e}\n")
            sys.stdout.flush()
            break

receive_thread = threading.Thread(target=receive, daemon=True)
receive_thread.start()

write()

sys.stdout.write("\r\033[K")
sys.stdout.flush()
sys.exit(0)