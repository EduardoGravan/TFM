import sys
import csv
import requests
from PIL import Image
from io import BytesIO
from PyQt5 import QtCore, QtGui, QtWidgets
from twitter_handler import TwitterHandler
from database_handler import DatabaseHandler
from datetime import date, datetime, timedelta


class ImageLoader(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal(QtWidgets.QTableWidget, int, QtWidgets.QWidget)

    def run(self, ui_window, table, image_list):
        for i in range(len(image_list)):
            QtWidgets.QApplication.processEvents()
            self.progress.emit(
                table, i, ui_window.get_profile_image_label(image_list[i])
            )
            QtWidgets.QApplication.processEvents()
        self.finished.emit()


class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == QtCore.Qt.LeftButton:
            self.clicked.emit()


class Ui_MainWindow(object):
    def __init__(
        self, twitter_handler: TwitterHandler, database_handler: DatabaseHandler
    ):
        super().__init__()
        self.twitter_handler = twitter_handler
        self.database_handler = database_handler

        self.last_basic_tweets = []
        self.last_advanced_tweets = []
        self.following_list = []

        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.setupUi(MainWindow)

        MainWindow.show()
        sys.exit(app.exec_())

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
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
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tab_widget = QtWidgets.QTabWidget(self.centralwidget)
        self.tab_widget.setObjectName("tab_widget")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_1)
        self.verticalLayout_4.setContentsMargins(25, 25, 25, 25)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label = QtWidgets.QLabel(self.tab_1)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setScaledContents(False)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.line_2 = QtWidgets.QFrame(self.tab_1)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_4.addWidget(self.line_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(50, 0, 50, 5)
        self.horizontalLayout.setSpacing(50)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textEdit = QtWidgets.QTextEdit(self.tab_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setMinimumSize(QtCore.QSize(0, 75))
        self.textEdit.setMaximumSize(QtCore.QSize(16777215, 75))
        self.textEdit.setAcceptRichText(False)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout.addWidget(self.textEdit, 0, QtCore.Qt.AlignVCenter)
        self.search_button = QtWidgets.QPushButton(self.tab_1)
        self.search_button.setObjectName("search_button")
        self.horizontalLayout.addWidget(self.search_button)
        self.label_save_basic_search = ClickableLabel(self.tab_1)
        self.label_save_basic_search.setMinimumSize(QtCore.QSize(60, 60))
        self.label_save_basic_search.setMaximumSize(QtCore.QSize(60, 60))
        self.label_save_basic_search.setText("")
        self.label_save_basic_search.setObjectName("label_save_basic_search")
        self.horizontalLayout.addWidget(self.label_save_basic_search)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(self.tab_1)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_4.addWidget(self.line)
        self.tableWidget_simple = QtWidgets.QTableWidget(self.tab_1)
        self.tableWidget_simple.setAlternatingRowColors(False)
        self.tableWidget_simple.setTextElideMode(QtCore.Qt.ElideRight)
        self.tableWidget_simple.setObjectName("tableWidget_simple")
        self.tableWidget_simple.setColumnCount(5)
        self.tableWidget_simple.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_simple.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_simple.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_simple.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_simple.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_simple.setHorizontalHeaderItem(4, item)
        self.tableWidget_simple.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_simple.horizontalHeader().setMinimumSectionSize(75)
        self.tableWidget_simple.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidget_simple.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_simple.verticalHeader().setVisible(False)
        self.verticalLayout_4.addWidget(self.tableWidget_simple)
        self.tab_widget.addTab(self.tab_1, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.tab_6)
        self.verticalLayout_7.setContentsMargins(25, 25, 25, 25)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_5 = QtWidgets.QLabel(self.tab_6)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setTextFormat(QtCore.Qt.AutoText)
        self.label_5.setScaledContents(False)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_7.addWidget(self.label_5, 0, QtCore.Qt.AlignHCenter)
        self.line_8 = QtWidgets.QFrame(self.tab_6)
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.verticalLayout_7.addWidget(self.line_8)
        self.frame = QtWidgets.QFrame(self.tab_6)
        self.frame.setMaximumSize(QtCore.QSize(16777215, 200))
        self.frame.setObjectName("frame")
        self.formLayout = QtWidgets.QFormLayout(self.frame)
        self.formLayout.setContentsMargins(50, 1, 50, 5)
        self.formLayout.setObjectName("formLayout")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.textEdit_advanced_query = QtWidgets.QTextEdit(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_advanced_query.sizePolicy().hasHeightForWidth())
        self.textEdit_advanced_query.setSizePolicy(sizePolicy)
        self.textEdit_advanced_query.setMinimumSize(QtCore.QSize(0, 30))
        self.textEdit_advanced_query.setMaximumSize(QtCore.QSize(16777215, 30))
        self.textEdit_advanced_query.setAcceptRichText(False)
        self.textEdit_advanced_query.setObjectName("textEdit_advanced_query")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.textEdit_advanced_query)
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.textEdit_user_handle = QtWidgets.QTextEdit(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_user_handle.sizePolicy().hasHeightForWidth())
        self.textEdit_user_handle.setSizePolicy(sizePolicy)
        self.textEdit_user_handle.setMinimumSize(QtCore.QSize(0, 30))
        self.textEdit_user_handle.setMaximumSize(QtCore.QSize(16777215, 30))
        self.textEdit_user_handle.setAcceptRichText(False)
        self.textEdit_user_handle.setObjectName("textEdit_user_handle")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.textEdit_user_handle)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(50, -1, 50, -1)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.checkBox_date_from = QtWidgets.QCheckBox(self.frame)
        self.checkBox_date_from.setMaximumSize(QtCore.QSize(150, 16777215))
        self.checkBox_date_from.setObjectName("checkBox_date_from")
        self.horizontalLayout_3.addWidget(self.checkBox_date_from)
        self.dateEdit_from = QtWidgets.QDateEdit(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateEdit_from.sizePolicy().hasHeightForWidth())
        self.dateEdit_from.setSizePolicy(sizePolicy)
        self.dateEdit_from.setMaximumSize(QtCore.QSize(100, 16777215))
        self.dateEdit_from.setDateTime(QtCore.QDateTime(QtCore.QDate(2006, 3, 21), QtCore.QTime(0, 0, 0)))
        self.dateEdit_from.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(2006, 3, 21), QtCore.QTime(0, 0, 0)))
        self.dateEdit_from.setMinimumDate(QtCore.QDate(2006, 3, 21))
        self.dateEdit_from.setObjectName("dateEdit_from")
        self.horizontalLayout_3.addWidget(self.dateEdit_from)
        self.formLayout.setLayout(9, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.radioButton_30_day = QtWidgets.QRadioButton(self.frame)
        self.radioButton_30_day.setMinimumSize(QtCore.QSize(0, 40))
        self.radioButton_30_day.setObjectName("radioButton_30_day")
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.LabelRole, self.radioButton_30_day)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(50, -1, 50, -1)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.checkBox_date_to = QtWidgets.QCheckBox(self.frame)
        self.checkBox_date_to.setMaximumSize(QtCore.QSize(150, 16777215))
        self.checkBox_date_to.setObjectName("checkBox_date_to")
        self.horizontalLayout_2.addWidget(self.checkBox_date_to)
        self.dateEdit_to = QtWidgets.QDateEdit(self.frame)
        self.dateEdit_to.setMaximumSize(QtCore.QSize(100, 16777215))
        self.dateEdit_to.setMinimumDate(QtCore.QDate(2006, 3, 21))
        self.dateEdit_to.setObjectName("dateEdit_to")
        self.horizontalLayout_2.addWidget(self.dateEdit_to)
        spacerItem = QtWidgets.QSpacerItem(450, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.label_save_advanced_search = ClickableLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_save_advanced_search.sizePolicy().hasHeightForWidth())
        self.label_save_advanced_search.setSizePolicy(sizePolicy)
        self.label_save_advanced_search.setMinimumSize(QtCore.QSize(40, 40))
        self.label_save_advanced_search.setMaximumSize(QtCore.QSize(40, 40))
        self.label_save_advanced_search.setText("")
        self.label_save_advanced_search.setObjectName("label_save_advanced_search")
        self.horizontalLayout_2.addWidget(self.label_save_advanced_search)
        self.formLayout.setLayout(11, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.radioButton_full_archive = QtWidgets.QRadioButton(self.frame)
        self.radioButton_full_archive.setMinimumSize(QtCore.QSize(0, 0))
        self.radioButton_full_archive.setChecked(True)
        self.radioButton_full_archive.setObjectName("radioButton_full_archive")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.radioButton_full_archive)
        self.verticalLayout_7.addWidget(self.frame)
        self.advanced_search_button = QtWidgets.QPushButton(self.tab_6)
        self.advanced_search_button.setObjectName("advanced_search_button")
        self.verticalLayout_7.addWidget(self.advanced_search_button)
        self.line_7 = QtWidgets.QFrame(self.tab_6)
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.verticalLayout_7.addWidget(self.line_7)
        self.tableWidget_advanced = QtWidgets.QTableWidget(self.tab_6)
        self.tableWidget_advanced.setMinimumSize(QtCore.QSize(0, 425))
        self.tableWidget_advanced.setAlternatingRowColors(False)
        self.tableWidget_advanced.setTextElideMode(QtCore.Qt.ElideRight)
        self.tableWidget_advanced.setObjectName("tableWidget_advanced")
        self.tableWidget_advanced.setColumnCount(5)
        self.tableWidget_advanced.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_advanced.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_advanced.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_advanced.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_advanced.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_advanced.setHorizontalHeaderItem(4, item)
        self.tableWidget_advanced.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_advanced.horizontalHeader().setMinimumSectionSize(75)
        self.tableWidget_advanced.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidget_advanced.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_advanced.verticalHeader().setVisible(False)
        self.verticalLayout_7.addWidget(self.tableWidget_advanced)
        self.tab_widget.addTab(self.tab_6, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_5)
        self.verticalLayout_3.setContentsMargins(25, 25, 25, 25)
        self.verticalLayout_3.setSpacing(10)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.tab_5)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_2.setScaledContents(False)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2, 0, QtCore.Qt.AlignHCenter)
        self.line_3 = QtWidgets.QFrame(self.tab_5)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_3.addWidget(self.line_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(15)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.update_follower_list_button = QtWidgets.QPushButton(self.tab_5)
        self.update_follower_list_button.setObjectName("update_follower_list_button")
        self.horizontalLayout_4.addWidget(self.update_follower_list_button, 0, QtCore.Qt.AlignHCenter)
        self.label_lookup_following = ClickableLabel(self.tab_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_lookup_following.sizePolicy().hasHeightForWidth())
        self.label_lookup_following.setSizePolicy(sizePolicy)
        self.label_lookup_following.setMinimumSize(QtCore.QSize(60, 60))
        self.label_lookup_following.setMaximumSize(QtCore.QSize(60, 60))
        self.label_lookup_following.setText("")
        self.label_lookup_following.setObjectName("label_lookup_following")
        self.horizontalLayout_4.addWidget(self.label_lookup_following)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.tableWidget_following = QtWidgets.QTableWidget(self.tab_5)
        self.tableWidget_following.setAlternatingRowColors(False)
        self.tableWidget_following.setTextElideMode(QtCore.Qt.ElideRight)
        self.tableWidget_following.setObjectName("tableWidget_following")
        self.tableWidget_following.setColumnCount(6)
        self.tableWidget_following.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_following.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_following.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_following.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_following.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_following.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_following.setHorizontalHeaderItem(5, item)
        self.tableWidget_following.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_following.horizontalHeader().setMinimumSectionSize(75)
        self.tableWidget_following.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidget_following.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_following.verticalHeader().setVisible(False)
        self.verticalLayout_3.addWidget(self.tableWidget_following)
        self.tab_widget.addTab(self.tab_5, "")
        self.verticalLayout.addWidget(self.tab_widget)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.tableWidget_simple.verticalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents
        )
        self.tableWidget_following.verticalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents
        )
        self.tableWidget_advanced.verticalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents
        )

        today = date.today()
        today = today.strftime("%d/%m/%Y").split("/")
        self.search_button.clicked.connect(self.basic_twitter_search)
        self.advanced_search_button.clicked.connect(self.advanced_twitter_search)
        self.update_follower_list_button.clicked.connect(self.update_following_list)
        self.radioButton_full_archive.clicked.connect(self.radio_full_archive_clicked)
        self.radioButton_30_day.clicked.connect(self.radio_30_day_clicked)
        self.dateEdit_to.setMaximumDate(
            QtCore.QDate(int(today[2]), int(today[1]), int(today[0]))
        )
        self.dateEdit_from.setMaximumDate(
            QtCore.QDate(int(today[2]), int(today[1]), int(today[0]))
        )
        self.dateEdit_from.setCalendarPopup(True)
        self.dateEdit_to.setCalendarPopup(True)

        pixmap = QtGui.QPixmap("./src/resources/images/save_button.png")
        self.label_save_basic_search.setScaledContents(True)
        self.label_save_basic_search.clicked.connect(self.save_basic_search)
        self.label_save_basic_search.setPixmap(pixmap)
        self.label_save_advanced_search.setScaledContents(True)
        self.label_save_advanced_search.clicked.connect(self.save_advanced_search)
        self.label_save_advanced_search.setPixmap(pixmap)

        pixmap = QtGui.QPixmap("./src/resources/images/lookup_tweets.png")
        self.label_lookup_following.setScaledContents(True)
        self.label_lookup_following.clicked.connect(self.lookup_following_tweets)
        self.label_lookup_following.setPixmap(pixmap)


        self.retranslateUi(MainWindow)
        self.tab_widget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TFM"))
        self.label.setText(_translate("MainWindow", "Búsqueda rápida en Twitter"))
        self.textEdit.setPlaceholderText(_translate("MainWindow", "Introduzca sus términos de búsqueda en este campo. . . (Recupera hasta 200 tweets recientes que coincidan con la consulta)"))
        self.search_button.setText(_translate("MainWindow", "Buscar"))
        self.tableWidget_simple.setSortingEnabled(True)
        item = self.tableWidget_simple.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Imagen"))
        item = self.tableWidget_simple.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Usuario"))
        item = self.tableWidget_simple.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Seguimiento"))
        item = self.tableWidget_simple.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Fecha"))
        item = self.tableWidget_simple.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Tweet"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_1), _translate("MainWindow", "Búsqueda rápida"))
        self.label_5.setText(_translate("MainWindow", "Búsqueda en profundidad en Twitter"))
        self.label_3.setText(_translate("MainWindow", "Consulta:"))
        self.textEdit_advanced_query.setPlaceholderText(_translate("MainWindow", "Introduzca sus términos de búsqueda. . ."))
        self.label_4.setText(_translate("MainWindow", "Cuenta de usuario:"))
        self.textEdit_user_handle.setPlaceholderText(_translate("MainWindow", "Introduzca el handle del usuario sobre el que quiere realizar la búsqueda. . ."))
        self.checkBox_date_from.setText(_translate("MainWindow", "Fecha - Desde:"))
        self.radioButton_30_day.setText(_translate("MainWindow", "Búsqueda 30 días"))
        self.checkBox_date_to.setText(_translate("MainWindow", "Fecha - Hasta"))
        self.radioButton_full_archive.setText(_translate("MainWindow", "Búsqueda en archivo"))
        self.advanced_search_button.setText(_translate("MainWindow", "Buscar"))
        self.tableWidget_advanced.setSortingEnabled(True)
        item = self.tableWidget_advanced.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Imagen"))
        item = self.tableWidget_advanced.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Usuario"))
        item = self.tableWidget_advanced.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Seguimiento"))
        item = self.tableWidget_advanced.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Fecha"))
        item = self.tableWidget_advanced.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Tweet"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_6), _translate("MainWindow", "Búsqueda en profundidad"))
        self.label_2.setText(_translate("MainWindow", "Panel de seguimiento de cuentas"))
        self.update_follower_list_button.setText(_translate("MainWindow", "Actualizar lista de seguimiento"))
        self.tableWidget_following.setSortingEnabled(True)
        item = self.tableWidget_following.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Imagen"))
        item = self.tableWidget_following.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Usuario"))
        item = self.tableWidget_following.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Seguimiento"))
        item = self.tableWidget_following.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Creación"))
        item = self.tableWidget_following.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Buscar"))
        item = self.tableWidget_following.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Siguiendo desde"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_5), _translate("MainWindow", "Cuentas seguidas"))


    def basic_twitter_search(self):
        self.__populate_simple_search_table()

    def advanced_twitter_search(self):
        self.__populate_advanced_search_table()

    def update_following_list(self):
        self.__populate_following_table()

    def __loading_menu(self, string, horizontal_size=250):
        dialog = QtWidgets.QDialog(self.centralwidget)
        dialog.setWindowTitle(f"Cargando {string}. . .")
        dialog.resize(horizontal_size, 1)
        dialog.open()

        return dialog

    def __populate_simple_search_table(self):
        query = self.textEdit.toPlainText()

        if query.strip() == "":
            QtWidgets.QMessageBox().critical(
                self.centralwidget,
                "Error",
                "Debe introducir la consulta para realizar la búsqueda",
            )

        else:
            loading_dialog = self.__loading_menu("tweets", horizontal_size=250)
            profile_image_list = []
            self.tableWidget_simple.setRowCount(0)
            self.last_basic_tweets = self.twitter_handler.custom_twitter_search(query)
            self.tableWidget_simple.setRowCount(len(self.last_basic_tweets))

            for i in range(len(self.last_basic_tweets)):
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.tableWidget_simple.setItem(i, 0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.tableWidget_simple.setItem(i, 1, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.tableWidget_simple.setItem(i, 2, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.tableWidget_simple.setItem(i, 3, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.tableWidget_simple.setItem(i, 4, item)

                profile_image_list.append(
                    self.last_basic_tweets[i].user.profile_image_url_https
                )

                followed_image_label = self.__get_followed_image_label(
                    self.last_basic_tweets[i].user.screen_name
                )

                self.tableWidget_simple.item(i, 1).setText(
                    self.last_basic_tweets[i].user.screen_name
                )
                self.tableWidget_simple.setCellWidget(i, 2, followed_image_label)
                self.tableWidget_simple.item(i, 3).setText(
                    self.last_basic_tweets[i].created_at.strftime("%Y-%m-%d %H:%M:%S")
                )
                self.last_basic_tweets[i].full_text = (
                    f"RT @{self.last_basic_tweets[i].retweeted_status.user.screen_name}: "
                    + self.last_basic_tweets[i].retweeted_status.full_text
                    if self.last_basic_tweets[i].full_text.startswith("RT @")
                    else self.last_basic_tweets[i].full_text
                )
                self.tableWidget_simple.item(i, 4).setText(
                    self.last_basic_tweets[i].full_text
                )

            self.launch_profile_image_thread(
                self.tableWidget_simple, profile_image_list
            )
            loading_dialog.close()

    def __populate_advanced_search_table(self):
        query = self.textEdit_advanced_query.toPlainText()
        handle = self.textEdit_user_handle.toPlainText()

        if query.strip() == "" and handle.strip() == "":
            QtWidgets.QMessageBox().critical(
                self.centralwidget,
                "Error",
                "Debe introducir al menos una consulta o una cuenta de usuario para realizar la búsqueda",
            )

        else:
            loading_dialog = self.__loading_menu("tweets", horizontal_size=250)
            profile_image_list = []
            self.tableWidget_advanced.setRowCount(0)

            if self.radioButton_30_day.isChecked():
                try:
                    self.last_advanced_tweets = self.twitter_handler.thirty_day_search(
                        query,
                        handle,
                        self.dateEdit_from.text()
                        if self.checkBox_date_from.isChecked()
                        else -1,
                        self.dateEdit_to.text()
                        if self.checkBox_date_to.isChecked()
                        else -1,
                    )
                except:
                    QtWidgets.QMessageBox().critical(
                        self.centralwidget,
                        "Error",
                        "Esta aplicación ha sobrepasado el límite de consultas mensual a la API 30_day_search.\nIntente volver a hacerla en modo archivo.",
                    )
                    loading_dialog.close()

                    return
            else:
                try:
                    self.last_advanced_tweets = self.twitter_handler.full_archive_search(
                        query,
                        handle,
                        self.dateEdit_from.text()
                        if self.checkBox_date_from.isChecked()
                        else -1,
                        self.dateEdit_to.text()
                        if self.checkBox_date_to.isChecked()
                        else -1,
                    )
                except:
                    QtWidgets.QMessageBox().critical(
                        self.centralwidget,
                        "Error",
                        "Esta aplicación ha sobrepasado el límite de consultas mensual a la API full_archive_search.\nIntente volver a hacer la consulta en modo 30-day.",
                    )
                    loading_dialog.close()

                    return

            self.tableWidget_advanced.setRowCount(len(self.last_advanced_tweets))

            for i in range(len(self.last_advanced_tweets)):
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.tableWidget_advanced.setItem(i, 0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.tableWidget_advanced.setItem(i, 1, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.tableWidget_advanced.setItem(i, 2, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.tableWidget_advanced.setItem(i, 3, item)
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.tableWidget_advanced.setItem(i, 4, item)

                profile_image_list.append(self.last_advanced_tweets[i].user.profile_image_url_https)

                followed_image_label = self.__get_followed_image_label(
                    self.last_advanced_tweets[i].user.screen_name
                )

                self.last_advanced_tweets[i].full_text = self.__recover_archive_tweet_text(self.last_advanced_tweets[i])
                self.tableWidget_advanced.item(i, 1).setText(self.last_advanced_tweets[i].user.screen_name)
                self.tableWidget_advanced.setCellWidget(i, 2, followed_image_label)
                self.tableWidget_advanced.item(i, 3).setText(
                    self.last_advanced_tweets[i].created_at.strftime("%Y-%m-%d %H:%M:%S")
                )
                self.tableWidget_advanced.item(i, 4).setText(
                    self.last_advanced_tweets[i].full_text
                )

            self.launch_profile_image_thread(
                self.tableWidget_advanced, profile_image_list
            )
            loading_dialog.close()

    def __populate_following_table(self):
        loading_dialog = self.__loading_menu("cuentas seguidas", horizontal_size=300)
        profile_image_list = []
        self.tableWidget_following.setRowCount(0)

        self.following_list = self.database_handler.read_followed_accounts()
        self.tableWidget_following.setRowCount(len(self.following_list))

        for i in range(len(self.following_list)):
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.tableWidget_following.setItem(i, 0, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.tableWidget_following.setItem(i, 1, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.tableWidget_following.setItem(i, 2, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.tableWidget_following.setItem(i, 3, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.tableWidget_following.setItem(i, 4, item)
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.tableWidget_following.setItem(i, 5, item)

            additional_acc_info = self.twitter_handler.recover_account_info(
                self.following_list[i][0]
            )

            profile_image_list.append(additional_acc_info.profile_image_url_https)

            followed_image_label = self.__get_followed_image_label(self.following_list[i][0])
            lookup_image_label = self.__get_following_image_label(self.following_list[i][0])
            self.tableWidget_following.item(i, 1).setText(self.following_list[i][0])
            self.tableWidget_following.setCellWidget(i, 2, followed_image_label)
            self.tableWidget_following.item(i, 3).setText(
                additional_acc_info.created_at.strftime("%Y-%m-%d %H:%M:%S")
            )
            self.tableWidget_following.setCellWidget(i, 4, lookup_image_label)
            self.tableWidget_following.item(i, 5).setText(self.following_list[i][1])

        self.launch_profile_image_thread(self.tableWidget_following, profile_image_list)
        loading_dialog.close()

    def get_profile_image_label(self, image_url):
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

    def __get_followed_image_label(self, twitter_handle):
        container_widget = QtWidgets.QWidget()
        center_layout = QtWidgets.QHBoxLayout()

        image_label = ClickableLabel()
        image_label.setFixedSize(60, 60)
        image_label.setScaledContents(True)

        center_layout.addWidget(image_label)
        container_widget.setLayout(center_layout)

        try:
            if self.database_handler.find_followed_account(twitter_handle):
                pixmap = QtGui.QPixmap("./src/resources/images/check_mark.png")
                image_label.setToolTip("Pulse para dejar de seguir.")
                image_label.clicked.connect(
                    lambda: self.__unfollow_account(twitter_handle, image_label)
                )
            else:
                pixmap = QtGui.QPixmap("./src/resources/images/follow_account.png")
                image_label.setToolTip("Pulse para empezar a seguir.")
                image_label.clicked.connect(
                    lambda: self.__follow_account(twitter_handle, image_label)
                )

            image_label.setPixmap(pixmap)

        except:
            image_label.setText("")

        return container_widget

    def __get_following_image_label(self, handle):
        container_widget = QtWidgets.QWidget()
        center_layout = QtWidgets.QHBoxLayout()

        image_label = ClickableLabel()
        image_label.setFixedSize(60, 60)
        image_label.setScaledContents(True)

        center_layout.addWidget(image_label)
        container_widget.setLayout(center_layout)

        try:
            pixmap = QtGui.QPixmap("./src/resources/images/lookup_tweets.png")
            image_label.setToolTip("Pulse para empezar a seguir.")
            image_label.clicked.connect(lambda: self.lookup_following_tweets_single_account(handle))
            image_label.setPixmap(pixmap)

        except:
            image_label.setText("")

        return container_widget

    def __follow_account(self, twitter_handle, image_label):
        message_box = self.__generate_message_box()
        message_box.setText(
            f"¿Desea añadir la cuenta @{twitter_handle} a la lista de cuentas seguidas?"
        )
        result = message_box.exec_()

        if result == QtWidgets.QMessageBox.Yes:
            self.database_handler.add_account(twitter_handle)
            image_label.clicked.disconnect()
            image_label.setToolTip("Pulse para dejar de seguir.")
            image_label.setPixmap(
                QtGui.QPixmap("./src/resources/images/check_mark.png")
            )
            image_label.clicked.connect(
                lambda: self.__unfollow_account(twitter_handle, image_label)
            )

    def __unfollow_account(self, twitter_handle, image_label):
        message_box = self.__generate_message_box()
        message_box.setText(
            f"¿Desea eliminar la cuenta @{twitter_handle} de la lista de cuentas seguidas?"
        )
        result = message_box.exec_()

        if result == QtWidgets.QMessageBox.Yes:
            self.database_handler.delete_followed_account(twitter_handle)
            image_label.clicked.disconnect()
            image_label.setToolTip("Pulse para empezar a seguir.")
            image_label.setPixmap(
                QtGui.QPixmap("./src/resources/images/follow_account.png")
            )
            image_label.clicked.connect(
                lambda: self.__follow_account(twitter_handle, image_label)
            )

    def __generate_message_box(self):
        message_box = QtWidgets.QMessageBox()
        message_box.setIcon(QtWidgets.QMessageBox.Question)
        message_box.setWindowTitle("Confirmación")
        message_box.setStandardButtons(
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        yes_button = message_box.button(QtWidgets.QMessageBox.Yes)
        yes_button.setText("Sí")
        no_button = message_box.button(QtWidgets.QMessageBox.No)
        no_button.setText("No")
        message_box.setDefaultButton(QtWidgets.QMessageBox.No)

        return message_box

    def __recover_archive_tweet_text(self, tweet):
        if tweet.truncated:
            str_tweet = tweet.extended_tweet["full_text"]
        else:
            if hasattr(tweet, "retweeted_status"):
                if tweet.retweeted_status.truncated:
                    str_tweet = f"RT @{tweet.retweeted_status.user.screen_name}: {tweet.retweeted_status.extended_tweet['full_text']}"
                else:
                    str_tweet = f"RT @{tweet.retweeted_status.user.screen_name}: {tweet.retweeted_status.text}"
            else:
                str_tweet = tweet.text

        return str_tweet

    def launch_profile_image_thread(self, table, profile_image_list):
        self.thread = QtCore.QThread(self.centralwidget)
        self.worker = ImageLoader()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(
            lambda: self.worker.run(self, table, profile_image_list)
        )
        self.worker.progress.connect(self.load_image)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def load_image(self, table, index, image_widget):
        table.setCellWidget(index, 0, image_widget)

    def radio_30_day_clicked(self):
        min_date = date.today() - timedelta(days=30)
        min_date = min_date.strftime("%d/%m/%Y").split("/")
        self.dateEdit_from.setMinimumDate(
            QtCore.QDate(int(min_date[2]), int(min_date[1]), int(min_date[0]))
        )
        self.dateEdit_to.setMinimumDate(
            QtCore.QDate(int(min_date[2]), int(min_date[1]), int(min_date[0]))
        )

    def radio_full_archive_clicked(self):
        self.dateEdit_from.setMinimumDate(QtCore.QDate(2006, 3, 21))
        self.dateEdit_to.setMinimumDate(QtCore.QDate(2006, 3, 21))

    def save_basic_search(self):
        if not self.last_basic_tweets:
            self.__show_save_error()
        else:
            message_box = self.__generate_message_box()
            message_box.setText(
                "¿Desea guardar la última consulta rápida en formato CSV?"
            )
            result = message_box.exec_()

            if result == QtWidgets.QMessageBox.Yes:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                with open(
                    f"./src/saved_queries/simple_search_result_{timestamp}.csv", "w"
                ) as f:
                    writer = csv.writer(f)
                    writer.writerow(["id", "screen_name", "created_at", "text"])
                    for tweet in self.last_basic_tweets:
                        writer.writerow(
                            [
                                tweet.id,
                                tweet.user.screen_name,
                                tweet.created_at,
                                tweet.full_text.encode("utf-8"),
                            ]
                        )

    def save_advanced_search(self):
        if not self.last_advanced_tweets:
            self.__show_save_error()
        else:
            message_box = self.__generate_message_box()
            message_box.setText(
                "¿Desea guardar la última consulta en profundidad en formato CSV?"
            )
            result = message_box.exec_()

            if result == QtWidgets.QMessageBox.Yes:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                with open(
                    f"./src/saved_queries/advanced_search_result_{timestamp}.csv", "w"
                ) as f:
                    writer = csv.writer(f)
                    writer.writerow(["id", "screen_name", "created_at", "text"])

                    for tweet in self.last_advanced_tweets:
                        writer.writerow(
                            [
                                tweet.id,
                                tweet.user.screen_name,
                                tweet.created_at,
                                tweet.full_text.encode("utf-8"),
                            ]
                        )

    def lookup_following_tweets(self):
        if not self.following_list:
            QtWidgets.QMessageBox().critical(
            self.centralwidget,
            "Error",
            "Debe actualizar la lista de cuentas seguidas antes de hacer la consulta (y tener, al menos, una cuenta seguida).",
            )
        else:
            str_following = "("
            for account in self.following_list:
                str_following += f"from:{account[0]} OR "
            str_following = str_following [:len(str_following)-4] + ")"
            
            self.tab_widget.setCurrentIndex(0)
            self.textEdit.setText(str_following)
            self.search_button.click()

    def lookup_following_tweets_single_account(self, handle):
            self.tab_widget.setCurrentIndex(0)
            self.textEdit.setText(f"from:{handle}")
            self.search_button.click()

    def __show_save_error(self):
        QtWidgets.QMessageBox().critical(
            self.centralwidget,
            "Error",
            "Debe haber hecho una consulta para poder guardarla",
        )
