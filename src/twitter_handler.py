import sys
import tweepy


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

    def custom_twitter_search(self, search_param):
        return self.api.search(search_param.strip(), tweet_mode="extended", count=200)

    def recover_account_info(self, handle):
        return self.api.get_user(handle)

    def lookup_users(self, query):
        return self.api.search_users(query, 2)

    def thirty_day_search(self, query, handle="", fromDate="-1", toDate="-1"):
        full_query = query if handle == "" else f"{query} from:{handle}"

        if fromDate != -1:
            from_date = self.__format_date_to_archive(fromDate) + "0000"
            if toDate != -1:
                to_date = self.__format_date_to_archive(toDate) + "2359"
                result = self.api.search_30_day(
                    "tfm30day", full_query, fromDate=from_date, toDate=to_date
                )
            else:
                result = self.api.search_30_day(
                    "tfm30day", full_query, fromDate=from_date
                )
        else:
            if toDate != -1:
                to_date = self.__format_date_to_archive(toDate) + "2359"
                result = self.api.search_30_day("tfm30day", full_query, toDate=to_date)
            else:
                result = self.api.search_30_day("tfm30day", full_query)

        return result

    def full_archive_search(self, query, handle="", fromDate="-1", toDate="-1"):
        full_query = query if handle == "" else f"{query} from:{handle}"

        if fromDate != -1:
            from_date = self.__format_date_to_archive(fromDate) + "0000"
            if toDate != -1:
                to_date = self.__format_date_to_archive(toDate) + "2359"
                result = self.api.search_full_archive(
                    "tfm", full_query, fromDate=from_date, toDate=to_date
                )
            else:
                result = self.api.search_full_archive(
                    "tfm", full_query, fromDate=from_date
                )
        else:
            if toDate != -1:
                to_date = self.__format_date_to_archive(toDate) + "2359"
                result = self.api.search_full_archive("tfm", full_query, toDate=to_date)
            else:
                result = self.api.search_full_archive("tfm", full_query)

        return result

    def __print_separator(self):
        print("\n---------------------\n")

    def __format_date_to_archive(self, date):
        formatted_date = date.split("/")
        str_formatted_date = formatted_date[2] + formatted_date[1] + formatted_date[0]

        return str_formatted_date
