import sys

stop_threads = False

def read_line(sock, buffer):
    """Read full-line messages"""
    while "\n" not in buffer:
        try:
            chunk = sock.recv(4096).decode("utf-8", errors="replace")
            if not chunk:
                return None, buffer
            buffer += chunk
        except(ConnectionResetError, BrokenPipeError, OSError):
            return None, buffer

    line, buffer = buffer.split("\n", 1)
    return line.strip(), buffer

def receive(client, nickname):
    """Handle different types of received messages"""
    global stop_threads
    buffer = ""
    while not stop_threads:
        line, buffer = read_line(client, buffer)
        """Close connection if not receive any message"""
        if line is None:
            sys.stdout.write("\r\033[KServer closed connection.\n")
            sys.stdout.flush()
            stop_threads = True
            client.close()
            break

        """Print the message if received normal message"""    
        if line.startswith("MSG "):
            msg = line[4:]
            sys.stdout.write(f"\r\033[K{msg}\n")
            sys.stdout.write(f"{nickname}: ")
            sys.stdout.flush()
            continue
        
        """Disconnect if reveived error messages"""
        elif message == "ERR ":
            err = line[4:]
            sys.stdout.write(f"\r\033[K[Error] {err}\n")
            sys.stdout.flush()
            stop_threads = True
            break
            

def write(client, nickname):
    """Handle different types of user input"""
    global stop_threads
    while not stop_threads:
        try:
            user_input = input(f"{nickname}: ")

            if not user_input:
                continue
            
            cmd = user_input.strip()

            """Disconnect when receive quit/exit command"""
            if cmd.lower() in ["/quit", "/exit"]:
                stop_threads = True
                sys.stdout.write("\r\033[KDisconnecting from server...\n")
                sys.stdout.flush()
                client.close()
                break
            
            """Only allow admin to kick and remove the user"""
            elif cmd.lower().startswith("/kick"):
                if nickname == "admin":
                    target_user = cmd[6:].strip()
                    if not target_user:
                        print("Usage: /kick <username>")
                        continue
                    client.send(f"KICK {target_user}\n".encode('utf-8'))
                else:
                    print("Command can only be executed by the admin!")
                continue

            """Only allow admin to ban, remove the user and add the banned user to a list to avoid future register/login"""
            elif cmd.lower().startswith("/ban"):
                if nickname == "admin":
                    target_user = cmd[5:].strip()
                    if not target_user:
                        print("Usage: /ban <username>")
                        continue
                    client.send(f"BAN {target_user}\n".encode('utf-8'))
                else:
                    print("Command can only be executed by the admin!")
                continue

            elif cmd:
                client.send(f"MSG {user_input}\n".encode('utf-8'))

        except (KeyboardInterrupt, EOFError):
            """Allow quit from keyboard and disconnect when receive an error"""
            stop_threads = True
            sys.stdout.write("\r\033[K[!] Exiting via keyboard shortcut...\n")
            sys.stdout.flush()
            client.close()
            break

        except Exception as e:
            """Handle all exceptions"""
            sys.stdout.write(f"\r\033[KError: {e}\n")
            sys.stdout.flush()
            break