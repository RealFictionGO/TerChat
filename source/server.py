import threading
import socket

host = '127.0.0.1'
port = int(input("Enter socket for chatroom: "))
server_name = input("Name the server ")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f'{client} has left the chat.'.encode('ascii'))
            break

def recive():
    while True:
        client, adress = server.accept()
        print(f'Connected with {str(adress)}')

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        print(f'New client connected {nickname}')
        broadcast(f'{nickname} joined chat'.encode('ascii'))
        client.send(f'Connected to {server_name}'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is active")
print(f'Welcome to {server_name}')
recive()