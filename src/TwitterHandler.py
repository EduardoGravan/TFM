import tweepy
import sys

class TwitterHandler:
    def __init__(self):
        self.__initialize_api()
        self.__validate_login()

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

                self.api = tweepy.API(auth)
            
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
    
    def test_timeline(self):
        timeline = self.api.home_timeline()
        print(f"{timeline[0].user.name}:\n\n{timeline[0].text}\n")
        self.__print_separator()

    def test_search(self, search_param):
        print(f"\nSearching for tweets with query: \"{search_param}\"")
        self.__print_separator()
        tweets = self.api.search(search_param)

        for i in range(3):
            print(f"{tweets[i].user.name}:\n\n{tweets[i].text}")
            self.__print_separator()

    
    def __print_separator(self):
        print("\n---------------------\n")
