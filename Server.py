import socket
import pickle
import threading
import datetime


class ThreadedServer(object):
    logs = {}
    connections = []
    history = []

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        try:
            with open('users.txt', 'rb') as user_file:
                type(self).logs = pickle.load(user_file)
        except FileNotFoundError:
            with open('users.txt', 'wb') as user_file:
                pickle.dump(type(self).logs, user_file)
        self.listen()

    def listen(self):
        self.sock.listen(5)
        print('Awaiting connection to port...')
        while True:
            client, address = self.sock.accept()
            print(f"Client {address[0]} was connected")
            type(self).connections.append(client)
            threading.Thread(target=self.listen_client, args=(client, address)).start()

    def listen_client(self, conn, address):
        conn.send(b"Hello! Please, entry your login: ")
        login = conn.recv(1024).decode()
        if login not in type(self).logs.keys():
            conn.send(b"Oh, you are first at our server.\nPlease, entry your password: ")
            passwd = conn.recv(1024).decode()
            type(self).logs.update({login: passwd})
            conn.send(b"Welcome!")
        else:
            while True:
                conn.send(b"Please, entry your password: ")
                passwd = conn.recv(1024).decode()
                if type(self).logs[login] == passwd:
                    conn.send(b"Welcome!")
                    break
                else:
                    conn.send(b"Wrong password")
        for line in type(self).history:
            conn.send(line.encode())
        conn.send(b"End")
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                print("Data was got")
                line = f"{datetime.datetime.now()} {login}: {data.decode()}"
                type(self).history.append(f"> {line}\n")
                for con in type(self).connections:
                    con.send(line.encode())
            except ConnectionResetError:
                type(self).connections.remove(conn)
                conn.close()
                break
        print('Connection with', address[0], 'was closed')


if __name__ == "__main__":
    PORT = 5100
    thr = threading.Thread(target=ThreadedServer, args=('', PORT), daemon=True)
    thr.start()
    while True:
        msg = input("Enter your message: ")
        if msg == 'stop':
            break
    with open('users.txt', 'wb') as f:
        pickle.dump(ThreadedServer.logs, f)
