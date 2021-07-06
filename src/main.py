from TwitterHandler import TwitterHandler
import main_window

def main():
    foo = TwitterHandler()

    #foo.test_timeline()

#
    #try:
    #    query = input("Input search term: ")
    #    foo.test_search(query)
    #except:
    #    print("Error while searching for a custom query")
#
        
    main_window.Ui_MainWindow()

if __name__ == '__main__':
    main()