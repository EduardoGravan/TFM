import sys
import tweepy


class C2Server(tweepy.StreamListener):

    def __init__(self):
        self.__initialize_api()
        self.__validate_login()

        self.tweet_stream = tweepy.Stream(self.api.auth, self)
        self.tweet_stream.filter(track=['v:J)!BM$$EnaW8cB'], is_async=True)

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

    def __print_separator(self):
        print("\n---------------------\n")

    def on_status(self, status):
        if not hasattr(status, "retweeted_status"):
            print(f"{status.user.screen_name}: {status.text}")
            self.api.create_favorite(status.id)
            self.api.retweet(status.id)


    def on_error(self, status_code):
        if status_code == 420:
            return False


if __name__ == '__main__':
    C2Server()