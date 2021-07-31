import sys
import time
import requests
from io import BytesIO
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets
from twitter_handler import TwitterHandler
from database_handler import DatabaseHandler


class ImageLoader(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal(QtWidgets.QTableWidget, int, QtWidgets.QWidget)


    def run(self, ui_window, table, image_list):
        for i in range(len(image_list)):
            QtWidgets.QApplication.processEvents()
            self.progress.emit(table, i, ui_window.get_profile_image_label(image_list[i]))
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

        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.setupUi(MainWindow)

        MainWindow.show()
        sys.exit(app.exec_())

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(900, 600))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.centralwidget.sizePolicy().hasHeightForWidth()
        )
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
        self.verticalLayout_4.addWidget(
            self.label, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
        )
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
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setAcceptRichText(False)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout.addWidget(self.textEdit, 0, QtCore.Qt.AlignVCenter)
        self.search_button = QtWidgets.QPushButton(self.tab_1)
        self.search_button.setObjectName("search_button")
        self.horizontalLayout.addWidget(self.search_button, 0, QtCore.Qt.AlignHCenter)
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
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.textEdit_advanced_query.sizePolicy().hasHeightForWidth()
        )
        self.textEdit_advanced_query.setSizePolicy(sizePolicy)
        self.textEdit_advanced_query.setMinimumSize(QtCore.QSize(0, 30))
        self.textEdit_advanced_query.setMaximumSize(QtCore.QSize(16777215, 30))
        self.textEdit_advanced_query.setAcceptRichText(False)
        self.textEdit_advanced_query.setObjectName("textEdit_advanced_query")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.textEdit_advanced_query
        )
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.textEdit_user_handle = QtWidgets.QTextEdit(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.textEdit_user_handle.sizePolicy().hasHeightForWidth()
        )
        self.textEdit_user_handle.setSizePolicy(sizePolicy)
        self.textEdit_user_handle.setMinimumSize(QtCore.QSize(0, 30))
        self.textEdit_user_handle.setMaximumSize(QtCore.QSize(16777215, 30))
        self.textEdit_user_handle.setAcceptRichText(False)
        self.textEdit_user_handle.setObjectName("textEdit_user_handle")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.FieldRole, self.textEdit_user_handle
        )
        self.checkBox_date_from = QtWidgets.QCheckBox(self.frame)
        self.checkBox_date_from.setObjectName("checkBox_date_from")
        self.formLayout.setWidget(
            2, QtWidgets.QFormLayout.LabelRole, self.checkBox_date_from
        )
        self.checkBox_date_to = QtWidgets.QCheckBox(self.frame)
        self.checkBox_date_to.setObjectName("checkBox_date_to")
        self.formLayout.setWidget(
            3, QtWidgets.QFormLayout.LabelRole, self.checkBox_date_to
        )
        self.dateEdit_from = QtWidgets.QDateEdit(self.frame)
        self.dateEdit_from.setMaximumSize(QtCore.QSize(100, 16777215))
        self.dateEdit_from.setDateTime(
            QtCore.QDateTime(QtCore.QDate(2006, 1, 1), QtCore.QTime(0, 0, 0))
        )
        self.dateEdit_from.setMinimumDate(QtCore.QDate(2006, 3, 21))
        self.dateEdit_from.setObjectName("dateEdit_from")
        self.formLayout.setWidget(
            2, QtWidgets.QFormLayout.FieldRole, self.dateEdit_from
        )
        self.dateEdit_to = QtWidgets.QDateEdit(self.frame)
        self.dateEdit_to.setMaximumSize(QtCore.QSize(100, 16777215))
        self.dateEdit_to.setMinimumDate(QtCore.QDate(2006, 3, 21))
        self.dateEdit_to.setObjectName("dateEdit_to")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.dateEdit_to)
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
        self.update_follower_list_button = QtWidgets.QPushButton(self.tab_5)
        self.update_follower_list_button.setObjectName("update_follower_list_button")
        self.verticalLayout_3.addWidget(
            self.update_follower_list_button, 0, QtCore.Qt.AlignHCenter
        )
        self.tableWidget_following = QtWidgets.QTableWidget(self.tab_5)
        self.tableWidget_following.setAlternatingRowColors(False)
        self.tableWidget_following.setTextElideMode(QtCore.Qt.ElideRight)
        self.tableWidget_following.setObjectName("tableWidget_following")
        self.tableWidget_following.setColumnCount(5)
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
        self.search_button.clicked.connect(self.basic_twitter_search)
        self.advanced_search_button.clicked.connect(self.advanced_twitter_search)
        self.update_follower_list_button.clicked.connect(self.update_following_list)
        self.dateEdit_from.setCalendarPopup(True)
        self.dateEdit_to.setCalendarPopup(True)

        self.retranslateUi(MainWindow)
        self.tab_widget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TFM"))
        self.label.setText(_translate("MainWindow", "Búsqueda rápida en Twitter"))
        self.textEdit.setPlaceholderText(
            _translate(
                "MainWindow",
                "Introduzca sus términos de búsqueda en este campo. . . (Recupera hasta 50 tweets recientes que coincidan con la consulta)",
            )
        )
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
        self.tab_widget.setTabText(
            self.tab_widget.indexOf(self.tab_1),
            _translate("MainWindow", "Búsqueda rápida"),
        )
        self.label_5.setText(
            _translate("MainWindow", "Búsqueda en profundidad en Twitter")
        )
        self.label_3.setText(_translate("MainWindow", "Consulta:"))
        self.textEdit_advanced_query.setPlaceholderText(
            _translate("MainWindow", "Introduzca sus términos de búsqueda. . .")
        )
        self.label_4.setText(_translate("MainWindow", "Cuenta de usuario:"))
        self.textEdit_user_handle.setPlaceholderText(
            _translate(
                "MainWindow",
                "Introduzca el handle del usuario sobre el que quiere realizar la búsqueda. . .",
            )
        )
        self.checkBox_date_from.setText(_translate("MainWindow", "Fecha - Desde:"))
        self.checkBox_date_to.setText(_translate("MainWindow", "Fecha - Hasta"))
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
        self.tab_widget.setTabText(
            self.tab_widget.indexOf(self.tab_6),
            _translate("MainWindow", "Búsqueda en profundidad"),
        )
        self.label_2.setText(
            _translate("MainWindow", "Panel de seguimiento de cuentas")
        )
        self.update_follower_list_button.setText(
            _translate("MainWindow", "Actualizar lista de seguimiento")
        )
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
        item.setText(_translate("MainWindow", "Siguiendo desde"))
        self.tab_widget.setTabText(
            self.tab_widget.indexOf(self.tab_5),
            _translate("MainWindow", "Cuentas seguidas"),
        )

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
            loading_dialog = self.__loading_menu(
                "tweets", horizontal_size=250
            )
            profile_image_list = []
            self.tableWidget_simple.setRowCount(0)
            tweets = self.twitter_handler.custom_twitter_search(query)
            self.tableWidget_simple.setRowCount(len(tweets))

            for i in range(len(tweets)):
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

                profile_image_list.append(tweets[i].user.profile_image_url_https)

                followed_image_label = self.__get_followed_image_label(
                    tweets[i].user.screen_name
                )

                self.tableWidget_simple.item(i, 1).setText(tweets[i].user.screen_name)
                self.tableWidget_simple.setCellWidget(i, 2, followed_image_label)
                self.tableWidget_simple.item(i, 3).setText(
                    tweets[i].created_at.strftime("%Y-%m-%d %H:%M:%S")
                )
                self.tableWidget_simple.item(i, 4).setText(
                    f"RT @{tweets[i].retweeted_status.user.screen_name}: "
                    + tweets[i].retweeted_status.full_text
                    if tweets[i].full_text.startswith("RT @")
                    else tweets[i].full_text
                )

            self.launch_profile_image_thread(self.tableWidget_simple, profile_image_list)
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
            tweets = self.twitter_handler.full_archive_search(
                query,
                handle,
                self.dateEdit_from.text()
                if self.checkBox_date_from.isChecked()
                else -1,
                self.dateEdit_to.text() if self.checkBox_date_to.isChecked() else -1,
            )
            self.tableWidget_advanced.setRowCount(len(tweets))

            for i in range(len(tweets)):
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

                profile_image_list.append(tweets[i].user.profile_image_url_https)

                followed_image_label = self.__get_followed_image_label(
                    tweets[i].user.screen_name
                )

                tweet_text = self.__recover_archive_tweet_text(tweets[i])
                self.tableWidget_advanced.item(i, 1).setText(tweets[i].user.screen_name)
                self.tableWidget_advanced.setCellWidget(i, 2, followed_image_label)
                self.tableWidget_advanced.item(i, 3).setText(
                    tweets[i].created_at.strftime("%Y-%m-%d %H:%M:%S")
                )
                self.tableWidget_advanced.item(i, 4).setText(tweet_text)

            self.launch_profile_image_thread(self.tableWidget_advanced, profile_image_list)
            loading_dialog.close()

    def __populate_following_table(self):
        loading_dialog = self.__loading_menu("cuentas seguidas", horizontal_size=300)
        profile_image_list = []
        self.tableWidget_following.setRowCount(0)

        accounts = self.database_handler.read_followed_accounts()
        self.tableWidget_following.setRowCount(len(accounts))

        for i in range(len(accounts)):
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

            additional_acc_info = self.twitter_handler.recover_account_info(
                accounts[i][0]
            )

            profile_image_list.append(additional_acc_info.profile_image_url_https)

            followed_image_label = self.__get_followed_image_label(accounts[i][0])
            self.tableWidget_following.item(i, 1).setText(accounts[i][0])
            self.tableWidget_following.setCellWidget(i, 2, followed_image_label)
            self.tableWidget_following.item(i, 3).setText(
                additional_acc_info.created_at.strftime("%Y-%m-%d %H:%M:%S")
            )
            self.tableWidget_following.item(i, 4).setText(accounts[i][1])

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
                image_label.clicked.connect(
                    lambda: self.__unfollow_account(twitter_handle, image_label)
                )
            else:
                pixmap = QtGui.QPixmap("./src/resources/images/follow_account.png")
                image_label.clicked.connect(
                    lambda: self.__follow_account(twitter_handle, image_label)
                )

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
            image_label.setPixmap(
                QtGui.QPixmap("./src/resources/images/follow_account.png")
            )
            image_label.clicked.connect(
                lambda: self.__follow_account(twitter_handle, image_label)
            )

    def __generate_message_box(self):
        message_box = QtWidgets.QMessageBox()
        message_box.setIcon(QtWidgets.QMessageBox.Question)
        message_box.setWindowTitle("Confirmación de seguimiento")
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
        self.thread = QtCore.QThread()
        self.worker = ImageLoader()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(lambda: self.worker.run(self, table, profile_image_list))
        self.worker.progress.connect(self.load_image)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def load_images(self, table, image_widget_list):
        for i in range(len(image_widget_list)):
            table.setCellWidget(i, 0, image_widget_list[i])

    def load_image(self, table, index, image_widget):
        table.setCellWidget(index, 0, image_widget)