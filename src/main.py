from TwitterHandler import TwitterHandler
import main_window

def main():
    foo = TwitterHandler()
    #foo.test_timeline()

    main_window.Ui_MainWindow(foo)

if __name__ == '__main__':
    main()