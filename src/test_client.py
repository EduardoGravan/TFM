import sys
import time
import socket
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


class BotClient():
    def __init__(self, config_file):
        self.config_file = config_file[1]
        self.bot_ip = "0.0.0.0"
        self.bot_port = random.randint(5000, 9999)

        self.c2_ip = "127.0.0.1"
        self.c2_port = 50003

        self.sleep_time = 1
        self.reduced_sleep_time = 0.2
        self.twitter_reply = "Muy buen tweet, estoy de acuerdo!"

        self.init_chrome_driver()
        self.twitter_login()

        self.connect_to_c2()
        self.wait_for_commands()

    def init_chrome_driver(self):
        options = Options()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.browser = webdriver.Chrome("./chromedriver.exe", options=options)

    def twitter_login(self):
        email, username, password = self.read_config_file()

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
                    sock_recv.settimeout(5)
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

        while True:
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
        
        time.sleep(self.reduced_sleep_time)

        retweet_button = WebDriverWait(self.browser, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, "//div[@aria-label='Retweet']")))
        retweet_button.click()
        print("Bot is retweeting the status. . .")
        confirm_retweet_button = WebDriverWait(self.browser, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, "//div[@data-testid='retweetConfirm']")))
        confirm_retweet_button.click()

        time.sleep(self.reduced_sleep_time)

        comment_button = WebDriverWait(self.browser, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, "//div[@aria-label='Reply']")))
        comment_button.click()
        print("Bot is replying to the status. . .")
        time.sleep(self.reduced_sleep_time)
        tweet_text = self.browser.find_elements_by_css_selector("br[data-text='true']")
        tweet_text[0].send_keys(self.twitter_reply)
        tweet_button = WebDriverWait(self.browser, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, "//div[@data-testid='tweetButton']")))
        tweet_button.click()

        print("Democracy successfully destroyed!")
        
        self.print_separator()

        time.sleep(5)
        
    def read_config_file(self):
        with open(self.config_file, "r") as config:
            try:
                self.print_separator()
                print("Attempting to read config file. . .")

                file_content = config.readlines()
                email = file_content[0].replace("\n", "")
                password = file_content[1].replace("\n", "")
                username = file_content[2].replace("\n", "")

                return email, password, username

            except:
                print("Error while reading config from file, program will terminate")
                sys.exit(-1)

    def print_separator(self):
        print("\n---------------------\n")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Error, you need to pass a proper configuration file as an argument.")
        print("Usage: python test_client.py bot1.cfg")
    else:
        BotClient(sys.argv)
