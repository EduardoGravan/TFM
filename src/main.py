import main_window
from database_handler import DatabaseHandler
from twitter_handler import TwitterHandler

def main():
    twitter_handler = TwitterHandler()
    database_handler = DatabaseHandler()

    main_window.Ui_MainWindow(twitter_handler, database_handler)

if __name__ == '__main__':
    main()