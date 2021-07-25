from datetime import datetime
import sqlite3



class DatabaseHandler:

    def add_account(self, twitter_handle):
        try:
            con = sqlite3.connect("./src/resources/database/DB.db")
            cursor = con.cursor()

            cursor.execute(f"INSERT INTO Account VALUES(\'{twitter_handle.strip()}\', \'{self.__get_timestamp()}\');")
            con.commit()

            cursor.close()
            con.close()

        except:
            print("Error while attempting to create a new followed account.")
    
    def read_followed_accounts(self):
        con = sqlite3.connect("./src/resources/database/DB.db")
        cursor = con.cursor()

        cursor.execute("SELECT * FROM Account;")

        result = cursor.fetchall()
        cursor.close()
        con.close()

        return result
    
    def find_followed_account(self, twitter_handle):
        con = sqlite3.connect("./src/resources/database/DB.db")
        cursor = con.cursor()

        cursor.execute(f"SELECT twitter_handle FROM Account WHERE twitter_handle=\'{twitter_handle}\';")

        result = cursor.fetchall()
        cursor.close()
        con.close()

        return result
    
    def delete_followed_account(self, twitter_handle):
        con = sqlite3.connect("./src/resources/database/DB.db")
        cursor = con.cursor()

        cursor.execute(f"DELETE FROM Account WHERE twitter_handle=\'{twitter_handle.strip()}\';")
        con.commit()

        rows = cursor.rowcount

        cursor.close()
        con.close()

        if rows != 1:
            print("Error while trying to delete followed twitter account.")

    def __get_timestamp(self):
        return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))
