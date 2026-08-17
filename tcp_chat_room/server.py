import threading
import socket

host = "127.0.0.1" #local_host
port = 9999

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))
server.listen()

clients=[]
nicknames=[]

def broadcast(message, sender=None):
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except:
                pass

def handle(client):
    while True:
        try:
            message = client.recv(4096)
            if not message:
                raise Exception("Client disconnected")
            broadcast(message, sender=client)
        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames.pop(index)
                print(f"Client '{nickname}' disconnected.")
                broadcast(f"{nickname} left the chat!\n".encode('utf-8'))
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
            or len(nickname)>30
            or len(nickname) == 0):
            print(f"Từ chối kết nối không hợp lệ từ {address}")
            client.close()
            continue

        clients.append(client)
        nicknames.append(nickname)

        print(f"Nickname of the client is {nickname}!")
        broadcast(f"{nickname} joined the chat! \n".encode('utf-8'))
        client.send("Connected to the server! \n".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()