from io import BytesIO
from TwitterHandler import TwitterHandler
from PyQt5 import QtCore, QtGui, QtWidgets
import requests
from PIL import Image

import sys


class Ui_MainWindow(object):
    def __init__(self, twitter_handler: TwitterHandler):
        super().__init__()
        self.twitter_handler = twitter_handler
        
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.setupUi(MainWindow)

        MainWindow.show()
        sys.exit(app.exec_())

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(900, 600))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(25, 25, 25, 25)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout.addWidget(self.textEdit, 0, QtCore.Qt.AlignHCenter)
        self.search_button = QtWidgets.QPushButton(self.centralwidget)
        self.search_button.setObjectName("search_button")
        self.horizontalLayout.addWidget(self.search_button, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setAlternatingRowColors(False)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 2, item)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(75)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.tableWidget)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.tableWidget.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.search_button.clicked.connect(self.search_twitter)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TFM"))
        self.search_button.setText(_translate("MainWindow", "Buscar"))
        self.tableWidget.setSortingEnabled(True)
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "0"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Imagen"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Usuario"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Tweet"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("MainWindow", "test"))
        item = self.tableWidget.item(0, 1)
        item.setText(_translate("MainWindow", "test"))
        item = self.tableWidget.item(0, 2)
        item.setText(_translate("MainWindow", "test"))
        self.tableWidget.setSortingEnabled(__sortingEnabled)

    def search_twitter(self):
        query = self.textEdit.toPlainText()
        self.populate_table(query)

    def populate_table(self, query):
        self.tableWidget.setRowCount(0)

        tweets = self.twitter_handler.custom_twitter_search(query)
        self.tableWidget.setRowCount(len(tweets))

        for i in range(len(tweets)):
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.tableWidget.setItem(i, 0, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.tableWidget.setItem(i, 1, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.tableWidget.setItem(i, 2, item)

            image_label = self.__get_image_label(tweets[i].user.profile_image_url)
            self.tableWidget.setCellWidget(i, 0, image_label)
            self.tableWidget.item(i, 1).setText(tweets[i].user.screen_name)
            self.tableWidget.item(i, 2).setText(tweets[i].full_text)
        
    def __get_image_label(self, image_url):
        container_widget = QtWidgets.QWidget()
        center_layout = QtWidgets.QHBoxLayout()
        
        image_label = QtWidgets.QLabel()
        image_label.setFixedSize(80, 80)
        image_label.setScaledContents(True)

        center_layout.addWidget(image_label)
        container_widget.setLayout(center_layout)
        
        try:
            response = requests.get(image_url.replace("_normal", ""))
            image = Image.open(BytesIO(response.content))

            byte_array = BytesIO()
            image.save(byte_array, format=image.format)
            byte_array = byte_array.getvalue()

            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(byte_array)

            image_label.setPixmap(pixmap)
        
        except:
            image_label.setText("")

        return container_widget

if __name__ == "__main__":
    Ui_MainWindow()
