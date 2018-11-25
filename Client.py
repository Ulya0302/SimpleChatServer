import socket
import threading


class Client(object):

    def __init__(self, host='127.0.0.1'):
        self.HOST = host
        self.sock = socket.socket()
        self.login = ''
        self.passwd = ''

    def connect(self):
        print("Connecting...")
        self.sock.connect((self.HOST, 5100))
        print('Connected to ', self.HOST)
        self.authentication()

    def authentication(self):
        data = self.sock.recv(1024)  # Please entry your login
        self.login = input(data.decode())
        self.sock.send(self.login.encode())
        data = self.sock.recv(1024)
        while True:
            self.passwd = input(data.decode())
            self.sock.send(self.passwd.encode())
            data = self.sock.recv(1024)
            if data.decode() == "Welcome!":
                print(data.decode())
                break
        flag = True
        while flag:
            data = self.sock.recv(1024)
            if "End" in data.decode():
                flag = False
            print(data.decode())
        self.chating()

    def chating(self):
        Client.send = threading.Thread(target=self.sending, daemon=True)
        Client.get = threading.Thread(target=self.getting, daemon=True)
        Client.send.start()
        Client.get.start()
        Client.send.join()
        self.sock.close()

    def sending(self):
        while True:
            try:
                data = input("> ")
                if data == "exit":
                    break
                self.sock.send(data.encode())
            except ConnectionResetError:
                print("\nServer forcibly disconnected!!")
                break

    def getting(self):
        while True:
            try:
                data = self.sock.recv(1024).decode()
                if not data.split()[2][:-1] == self.login:
                    print(data + "\n>")
            except ConnectionResetError:
                print("You are disconnected from server")
                break


if __name__ == "__main__":
    cl = Client()
    cl.connect()
    input("Press Enter to exit")
