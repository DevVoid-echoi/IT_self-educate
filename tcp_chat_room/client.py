import threading
import socket
import sys

nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 9999))

first_msg = client.recv(4096).decode("utf-8", errors="replace")
if first_msg == "NICK":
    client.send(nickname.encode('utf-8'))

print("-" * 50)
print(" HƯỚNG DẪN CHAT:")
print(" - Nhập tin nhắn và bấm Enter để gửi.")
print(" - Gõ '/quit' hoặc '/exit' để rời phòng chat.")
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

            sys.stdout.write(f"\r\033[K{message}")
            sys.stdout.write(f"{nickname}: ")
            sys.stdout.flush()

        except:
            if not stop_threads:
                sys.stdout.write("\r\033[KConnection error.\n")
                sys.stdout.flush()
                stop_threads = True
                client.close()
            break

def write():
    global stop_threads
    while not stop_threads:
        try:
            user_input = input(f"{nickname}: ")

            if user_input.strip().lower() in ["/quit", "/exit"]:
                stop_threads = True
                sys.stdout.write("\r\033[KDisconnecting from server...\n")
                sys.stdout.flush()
                client.close()
                break

            if user_input.strip():
                message = f"{nickname}: {user_input}\n"
                client.send(message.encode('utf-8'))

        except (KeyboardInterrupt, EOFError):
            stop_threads = True
            sys.stdout.write("\r\033[K[!] Exiting via keyboard shortcut...\n")
            sys.stdout.flush()
            client.close()
            break

        except:
            break

receive_thread = threading.Thread(target=receive, daemon=True)
receive_thread.start()

write()

sys.stdout.write("\r\033[K")
sys.stdout.flush()
sys.exit(0)