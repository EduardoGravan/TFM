import tweepy
import sys

class TwitterHandler:
    def __init__(self):
        self.__initialize_api()

    def __initialize_api(self):
        print("\n---------------------\n")
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

                self.api = tweepy.API(auth)
                self.__validate_login()
                print("\n---------------------\n")
            except:
                print("Error while reading API keys from file, program will terminate")
                sys.exit(-1)

    def __validate_login(self):
        print("Verifying credentials. . .")

        try:
            self.api.verify_credentials()
            print("Authentication OK")
        except:
            print("Error during authentication, program will terminate")
            sys.exit(-1)
    
    def test_timeline(self):
        timeline = self.api.home_timeline()
        print(f"{timeline[0].user.name}:\n\n{timeline[0].text}\n")