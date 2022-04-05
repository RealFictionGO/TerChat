import threading
import socket
import os
import json

from source.client import config, login  

host = socket.gethostname()  
path = os.getcwd()

#search server directory
def server_dir():
    if os.path.exists(path + "\\rooms"):
        os.chdir(path + "\\rooms")
    else:
        os.mkdir('rooms')
        os.chdir(path + "\\rooms")
    return path + "\\rooms"

# mode choosing [1] loading already saved server from \rooms dir
#               [2] creating new server save

def print_servers(print:bool):
    server_dir()
    if print == True:
        print('________________________________________')
        for server in os.listdir():
            print(server.replace('.json', ''))
        print('________________________________________')

    server_names = os.listdir()
    for name in server_names:
        raw_name = name.replace('.json','')
        index = server_names.index(name)
        server_names.pop(index)
        server_names.insert(index, raw_name)

    return server_names

def load_server():
    all_servers = print_servers()

    while True:
        l_server = input('\n Which server to load? \nserver name: ').strip()

        if l_server in all_servers:
            with open(l_server + '.json', 'r') as f:
                server_data = json.loads(f)
                f.close()
            
            return server_data

        elif l_server == 'exit':
            return None

        else:
            print('Choose server from a list')

def create_server():
    server_dir()
    print_servers(False)
    new_server_data = {}
    while True:
        name = input('New server name: ')
        if name not in os.listdir():
            break
        else:
            print('Server name already exist')

    new_server_data.update({'name' : name})
    while True:
        try:
            server_port = int(input('Server\'s port ( recomended 30000 > ): ').strip())
            break
        except:
            print('You have to type a number')
    new_server_data.update({'port' : server_port})

    with open(name + '.json', 'w') as f:
        f.write(json.dumps(new_server_data))
        f.close()

    while True:
        accept = input('Do you want to load this server? [y/n]\n ').strip()
        if accept == 'y':
            return new_server_data
        elif accept == 'n':
            return
        else:
            print('You have to type \'y\' or \'n\'')

def start():
    while True:
        print("""
_____           ____ _           _   
|_   _|__ _ __ / ___| |__   __ _| |_ 
  | |/ _ \ '__| |   | '_ \ / _` | __|
  | |  __/ |  | |___| | | | (_| | |_ 
  |_|\___|_|   \____|_| |_|\__,_|\__|
        """)
        print('Made by RealFiction')
        print('https://github.com/RealFictionGO')
        print('https://twitter.com/RealfictionS')

        option = input('>_').strip()

        if option == 'load':
            l_data = load_server()
            return l_data
        elif option == 'create':
            c_data = create_server()
            return c_data
        elif option == 'help' or option == 'ls':
            print("""
            
            | load     - connect to a server 
            | create   - settings for display
            | help     - as its name says

            """)
        else:
            print('Type \'help\' for command list')

server_data = start()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, server_data.get('port')))
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
        client.send(f'Connected to {server_data.get("name")}'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is active")
print(f'Welcome to {server_data.get("name")}')
recive()