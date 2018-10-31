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
        with open('log.txt', 'rb') as f:
            ThreadedServer.logs = pickle.load(f)
        self.listen()

    def listen(self):
        self.sock.listen(5)
        print('Awaiting connection to port...')
        while True:
            client, addr = self.sock.accept()
            print(f"Client {addr[0]} was connected")
            ThreadedServer.connections.append(client)
            threading.Thread(target=self.listenToClient, args=(client, addr)).start()

    def listenToClient(self, conn, addr):
        conn.send(b"Hello! Please, entry your login: ")
        login = conn.recv(1024).decode()
        if not login in ThreadedServer.logs.keys():
            conn.send(b"Oh, you are first at our server.\nPlease, entry your password: ")
            passwd = conn.recv(1024).decode()
            ThreadedServer.logs.update({login: passwd})
            conn.send(b"Welcome!")
        else:
            while True:
                conn.send(b"Please, entry your password: ")
                passwd = conn.recv(1024).decode()
                if ThreadedServer.logs[login] == passwd:
                    conn.send(b"Welcome!")
                    break
                else:
                    conn.send(b"Wrong password")
        for line in ThreadedServer.history:
            conn.send(line.encode())
        conn.send(b"End")
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                print("Data was got")
                line = f"{datetime.datetime.now()} {login}: {data.decode()}"
                ThreadedServer.history.append(f"> {line}\n")
                for con in ThreadedServer.connections:
                    con.send(line.encode())
            except ConnectionResetError:
                ThreadedServer.connections.remove(conn)
                conn.close()
                break
        print('Connection with', addr[0], 'was closed')




if __name__ == "__main__":
    PORT = 5100
    thr = threading.Thread(target=ThreadedServer, args=('',PORT), daemon=True)
    thr.start()
    while True:
        str = input("Enter your message: ")
        if str == 'stop':
            break
    with open('log.txt', 'wb') as f:
        pickle.dump(ThreadedServer.logs, f)
