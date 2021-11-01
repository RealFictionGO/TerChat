import threading
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
        break
    else:
        print('Nickname can\'t be empty')

client.connect((ip, port))

def recive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message.replace(' ', '') == "NICK":
                client.send(nickname.encode('ascii'))
            else:
                print(message)

        except:
            print("Error occurred")
            client.close()
            break

def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))    

recive_thred = threading.Thread(target=recive)
recive_thred.start()

write_thred = threading.Thread(target=write)
write_thred.start()
