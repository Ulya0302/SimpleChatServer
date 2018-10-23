import socket
import pickle
import threading


class ThreadedServer(object):
    logs = {}

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
            threading.Thread(target=self.listenToClient, args=(client, addr)).start()

    def listenToClient(self, conn, addr):
        if not addr[0] in ThreadedServer.logs.keys():
            conn.send(b"Hello! Please, entry your name: ")
            print("Waiting for a name...")
            data = conn.recv(1024).decode()
            ThreadedServer.logs.update({addr[0]:data})

        conn.send(f"Hello {ThreadedServer.logs[addr[0]]}".encode())
        while True:
            print("Waiting for a data...")
            data = conn.recv(1024)
            if not data:
                break
            print("Data was got")
            conn.send(data.upper())
        conn.close()
        print('Connection with', addr[0], 'was closed')
        #return False


if __name__ == "__main__":
    PORT = 5100
    thr = threading.Thread(target=ThreadedServer, args=('',PORT), daemon=True)
    thr.start()
    input("Press Enter to off Server!\n")
    with open('log.txt', 'wb') as f:
        pickle.dump(ThreadedServer.logs, f)
