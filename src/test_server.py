import time
import socket
from threading import Thread


class BotServer():
    def __init__(self):
        self.bot_list = []
        Thread(target = self.register_bot).start()
        self.foo()

    def register_bot(self):
        self.print_separator()
        print("Launched a thread to listen for incoming bot subscriptions. . .")
        self.print_separator()
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock_recv:
                    sock_recv.bind(("0.0.0.0", 50003))
                    data, addr = sock_recv.recvfrom(1024)
                    data = data.decode("utf-8")
                    
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock_send:
                    sock_send.sendto(b"200", (addr[0], int(data)))
                    self.bot_list.append(f"{addr[0]}:{data}")
                    self.print_separator()
                    print(f"Added new bot to active bot list: {addr[0]}:{data}")
                    self.print_separator()
            except:
                continue

    def send_command(self, command):
            print(f"Sending command: {command}")
            self.print_separator()

            with (socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
                for bot in self.bot_list:
                    bot = bot.split(":")
                    sock.sendto(command.encode("utf-8"), (bot[0], int(bot[1])))
    
    def print_separator(self):
        print("\n---------------------\n")

    def foo(self):
        while not self.bot_list:
            time.sleep(0.05)
        
        while True:
            self.send_command("nullpointer33|1423287122681729032")
            time.sleep(2)

if __name__ == '__main__':
    BotServer()
