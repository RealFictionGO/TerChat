import threading
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def login():
    while True:
        try:
            ip = input('Input server ip: ')
            port = int(input('Enter server port: '))
            break
        except:
            print('Invalid input\n Tip: Server port has to be a number')

    while True:
        nickname = input('Enter nickname: ')
        if nickname != '':
            return ip, port, nickname
        else:
            print('Nickname can\'t be empty')

def config():
    pass

def start():
        while True:
            print("""
   _____          ____ _           _   
  |_   _|__ _ __ / ___| |__   __ _| |_ 
    | |/ _ \ '__| |   | '_ \ / _` | __|
    | |  __/ |  | |___| | | | (_| | |_ 
    |_|\___|_|   \____|_| |_|\__,_|\__|
            """)
            print('Made by RealFiction')
            print('https://github.com/RealFictionGO')
            print('https://twitter.com/RealfictionS')

            option = input('>_').strip()

            if option == 'login':
                l_data = login()
                return l_data
            elif option == 'config':
                config()
            elif option == 'help' or option == 'ls':
                print("""
                
                | login    - connect to a server 
                | config   - settings for display
                | help     - as its name says

                """)
            else:
                print('Type \'help\' for command list')

login_data = start()
client.connect((login_data[0], login_data[1]))

def recive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message.replace(' ', '') == "NICK":
                client.send(login_data[2].encode('ascii'))
            else:
                print(message)

        except:
            print("Error occurred")
            client.close()
            break

def write():
    while True:
        message = f'{login_data[2]}: {input("")}'
        client.send(message.encode('ascii'))

recive_thred = threading.Thread(target=recive)
recive_thred.start()

write_thred = threading.Thread(target=write)
write_thred.start()
