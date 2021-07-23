import sqlite3

class DatabaseHandler:

    def add_account(self, twitter_handler):
        try:
            con = sqlite3.connect("./src/resources/DB.db")
            cursor = con.cursor()

            cursor.execute(f"INSERT INTO Account VALUES(\'{twitter_handler.strip()}\');")
            con.commit()

            cursor.close()
            con.close()

        except:
            print("Error while attempting to create a new followed account.")
    
    def read_followed_accounts(self):
        con = sqlite3.connect("./src/resources/DB.db")
        cursor = con.cursor()

        cursor.execute("SELECT * FROM Account;")

        result = cursor.fetchall()
        cursor.close()
        con.close()

        print(result)

        return result
    
    def delete_followed_account(self, twitter_handler):
        con = sqlite3.connect("./src/resources/DB.db")
        cursor = con.cursor()

        cursor.execute(f"DELETE FROM Account WHERE twitter_handler=\'{twitter_handler.strip()}\';")
        con.commit()

        rows = cursor.rowcount

        cursor.close()
        con.close()

        if rows == 1:
            print("Succesfully deleted followed twitter account")
        else:
            print("Error while trying to delete followed twitter account.")
            


DatabaseHandler().add_account("sanchezrum")
DatabaseHandler().read_followed_accounts()
DatabaseHandler().delete_followed_account("sanchezrum")
DatabaseHandler().read_followed_accounts()