from TwitterHandler import TwitterHandler
from test_interfaz import Ui_Dialog

def main():
    foo = TwitterHandler()

    foo.test_timeline()
    #Ui_Dialog()

    try:
        query = input("Input search term: ")
        foo.test_search(query)
    except:
        print("Error while searching for a custom query")

if __name__ == '__main__':
    main()