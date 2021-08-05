import socket
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions



class BotClient():
    def __init__(self):
        self.bot_ip = "0.0.0.0"
        self.bot_port = random.randint(5000, 9999)

        self.c2_ip = "127.0.0.1"
        self.c2_port = 50003

        self.sleep_time = 3

        self.init_chrome_driver()
        self.twitter_login()

        self.connect_to_c2()
        self.wait_for_commands()

    def init_chrome_driver(self):
        options = Options()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.browser = webdriver.Chrome("./chromedriver.exe", options=options)

    def twitter_login(self):
        email = "egstfm1@gmail.com"
        username = "egs_tfm_1"
        password = "2021egstfm1"

        self.print_separator()
        print("Bot attempting to log in to Twitter. . .")
        self.print_separator()

        self.browser.get("https://www.twitter.com/login")
        time.sleep(self.sleep_time)

        username_input = self.browser.find_element_by_name("session[username_or_email]")
        password_input = self.browser.find_element_by_name("session[password]")

        username_input.send_keys(email)
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)
        time.sleep(self.sleep_time)
        
        if self.browser.current_url != "https://www.twitter.com/home":
            username_input = self.browser.find_element_by_name("session[username_or_email]")
            password_input = self.browser.find_element_by_name("session[password]")

            username_input.send_keys(username)
            password_input.send_keys(password)
            password_input.send_keys(Keys.ENTER)
            time.sleep(self.sleep_time)


        print(f"Bot succesfully logged in to Twitter with account: {email}")
        self.print_separator()

    def connect_to_c2(self):
        print("Attempting to connect to C2 server. . .")
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock_send:
                sock_send.sendto(str(self.bot_port).encode("utf-8"), (self.c2_ip, self.c2_port))

            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock_recv:
                    sock_recv.settimeout(self.sleep_time)
                    try:
                        sock_recv.bind((self.bot_ip, self.bot_port))
                        msg, _ = sock_recv.recvfrom(1024)

                        if msg.decode("utf-8") == "200":
                            print("Succesfully connected to C2 server. . .")
                            break

                    except:
                        continue 

    def wait_for_commands(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.bot_ip, self.bot_port))
        
        self.print_separator()
        print("Listening for incoming commands from C2 server. . .")
        self.print_separator()

        #while True:
        data, addr = sock.recvfrom(1024)
        data = data.decode("utf-8")
        print("Command received: ")
        print(f"rcv: {data} from {addr}")
        self.print_separator()
        self.execute_command(data)

    def execute_command(self, command):
        command = command.split("|")
        tweet_url = f"https://twitter.com/{command[0]}/status/{command[1]}"
        self.browser.get(tweet_url)
        print(f"Bot opening status: \"{tweet_url}\"")
        self.print_separator()
        time.sleep(self.sleep_time)

        like_button = WebDriverWait(self.browser, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, "//div[@aria-label='Like']")))
        like_button.click()
        print("Bot is liking the status. . .")
        
        time.sleep(self.sleep_time)

        retweet_button = WebDriverWait(self.browser, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, "//div[@aria-label='Retweet']")))
        retweet_button.click()
        print("Bot is retweeting the status. . .")
        confirm_retweet_button = WebDriverWait(self.browser, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, "//div[@data-testid='retweetConfirm']")))
        confirm_retweet_button.click()
        self.print_separator()
        
        time.sleep(self.sleep_time)

        
    def print_separator(self):
        print("\n---------------------\n")

if __name__ == '__main__':
    BotClient()
