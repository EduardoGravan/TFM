import socket


class BotClient():
    def __init__(self):
        self.bot_ip = "0.0.0.0"
        self.bot_port = 5005

        self.c2_ip = "127.0.0.1"
        self.c2_port = 50003

        self.connect_to_c2()
        self.receive_command()

    def connect_to_c2(self):
        self.print_separator()
        print("Attempting to connect to C2 server. . .")
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock_send:
                sock_send.sendto(str(self.bot_port).encode("utf-8"), (self.c2_ip, self.c2_port))

            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock_recv:
                    sock_recv.settimeout(5)
                    try:
                        sock_recv.bind((self.bot_ip, self.bot_port))
                        msg, _ = sock_recv.recvfrom(1024)

                        if msg.decode("utf-8") == "200":
                            print("Succesfully connected to C2 server. . .")
                            break

                    except:
                        continue 

    def receive_command(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.bot_ip, self.bot_port))
        
        self.print_separator()
        print("Listening for incoming commands from C2 server. . .")
        self.print_separator()

        while True:
            data, addr = sock.recvfrom(1024)
            data = data.decode("utf-8")
            print("Command received: ")
            print(f"rcv: {data} from {addr}")
            self.print_separator()

    def print_separator(self):
        print("\n---------------------\n")

if __name__ == '__main__':
    BotClient()
