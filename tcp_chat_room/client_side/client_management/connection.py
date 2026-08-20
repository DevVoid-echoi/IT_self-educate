import sys

stop_threads = False

def receive(client, nickname, password):
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

def write(client, nickname):
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