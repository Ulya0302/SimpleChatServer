import socket
import threading
import os
from time import sleep

class Scanner(object):
    available_ports = []
    host = ''
    n1 = 0 #Число завершивших работу потоков
    start: int = 0
    end = 5200
    step = 20
    PORTS = end - start

    def __init__(self, host_or_ip):
        Scanner.host = host_or_ip

    def start_scan(self):
        thr = threading.Thread(target=self.threading, args=(), daemon=True)
        Scanner.show_bar()
        thr.start()
        while (thr.is_alive()):
            sleep(5)
            Scanner.reload_bar()
        Scanner.show()

    def threading(self):
        threads = []
        for i in range(Scanner.start, Scanner.end, Scanner.step):
            threads.append(threading.Thread(target=self.to_scan, args=(i, i + Scanner.step)))
        for thr in threads:
            thr.start()
        for thr in threads:
            thr.join()

    def to_scan(self, min, max):
        for port in range(min, max):
            try:
                sock = socket.socket()
                sock.connect((Scanner.host, port))
            except (ConnectionRefusedError, OSError) as err:
                 pass
            else:
                Scanner.available_ports.append(port)
                sock.close()
            finally:
                Scanner.n1 += 1


    @classmethod
    def reload_bar(cls):
        cls.clear()
        k = int(cls.n1/cls.PORTS*20)
        lst = ['#']*k + ['.']*(20-k)
        print(f"Entry host or IP: {cls.host}\nProgress:[{''.join(lst)}] {int(cls.n1/cls.PORTS*100)}% done")

    @classmethod
    def show_bar(cls):
        cls.clear()
        print(f"Entry host or IP: {cls.host}\nProgress:[{'.'*20}] 0% done")

    @classmethod
    def show(self):
        for el in sorted(Scanner.available_ports):
            print(f"Port {el} is available")

    @classmethod
    def clear(cls):
        os.system('cls')

if __name__ == "__main__":
    host_ip = input("Entry host or IP: ")
    scn = Scanner(host_ip)
    scn.start_scan()
    input("Press Enter to exit")
