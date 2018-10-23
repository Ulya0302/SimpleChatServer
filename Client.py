import socket

HOST = '127.0.0.1'

sock = socket.socket()
print("Connecting...")
sock.connect((HOST, 6074))
print('Connected to ', HOST)


data = sock.recv(1024)
if data.decode() == "Hello! Please, entry your name: ":
    name = input(data.decode())
    sock.send(name.encode())
    data = sock.recv(1024)
    print(data.decode())
else:
    print(data.decode())


while True:
    try:
        data = input("Enter your message to server: ")
        if data == 'exit':
            break
        sock.send(data.encode())
        print("Message was sended")
        data = sock.recv(1024)
        print('This was recieved from server:')
        print(data.decode())
    except (ConnectionResetError):
        print("\nServer forcibly disconnected!!")
        break
sock.close()
print('Connection with', HOST, 'was closed')

input("Press Enter to exit")