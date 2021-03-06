# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'app.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.view_image = QtWidgets.QGraphicsView(self.centralwidget)
        self.view_image.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.view_image.setObjectName("view_image")
        self.verticalLayout.addWidget(self.view_image)
        self.h1_layout = QtWidgets.QHBoxLayout()
        self.h1_layout.setObjectName("h1_layout")
        self.btn_locate = QtWidgets.QPushButton(self.centralwidget)
        self.btn_locate.setMaximumSize(QtCore.QSize(150, 16777215))
        self.btn_locate.setObjectName("btn_locate")
        self.h1_layout.addWidget(self.btn_locate)
        self.btn_recognize = QtWidgets.QPushButton(self.centralwidget)
        self.btn_recognize.setMaximumSize(QtCore.QSize(150, 16777215))
        self.btn_recognize.setObjectName("btn_recognize")
        self.h1_layout.addWidget(self.btn_recognize)
        self.verticalLayout.addLayout(self.h1_layout)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setMaximumSize(QtCore.QSize(16777215, 150))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        self.menu_file = QtWidgets.QMenu(self.menubar)
        self.menu_file.setObjectName("menu_file")
        self.menu_settings = QtWidgets.QMenu(self.menubar)
        self.menu_settings.setObjectName("menu_settings")
        self.menu_help = QtWidgets.QMenu(self.menubar)
        self.menu_help.setObjectName("menu_help")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_open = QtWidgets.QAction(MainWindow)
        self.action_open.setObjectName("action_open")
        self.action_exit = QtWidgets.QAction(MainWindow)
        self.action_exit.setObjectName("action_exit")
        self.action_load_config = QtWidgets.QAction(MainWindow)
        self.action_load_config.setObjectName("action_load_config")
        self.action_preferences = QtWidgets.QAction(MainWindow)
        self.action_preferences.setObjectName("action_preferences")
        self.action_save_config = QtWidgets.QAction(MainWindow)
        self.action_save_config.setObjectName("action_save_config")
        self.action_about = QtWidgets.QAction(MainWindow)
        self.action_about.setObjectName("action_about")
        self.menu_file.addAction(self.action_open)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_exit)
        self.menu_settings.addAction(self.action_load_config)
        self.menu_settings.addAction(self.action_save_config)
        self.menu_settings.addAction(self.action_preferences)
        self.menu_help.addAction(self.action_about)
        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_settings.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())

        self.retranslateUi(MainWindow)
        self.action_exit.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_locate.setText(_translate("MainWindow", "Locate"))
        self.btn_recognize.setText(_translate("MainWindow", "Recognize"))
        self.menu_file.setTitle(_translate("MainWindow", "File"))
        self.menu_settings.setTitle(_translate("MainWindow", "Settings"))
        self.menu_help.setTitle(_translate("MainWindow", "Help"))
        self.action_open.setText(_translate("MainWindow", "Open"))
        self.action_exit.setText(_translate("MainWindow", "Exit"))
        self.action_load_config.setText(_translate("MainWindow", "Load Config"))
        self.action_preferences.setText(_translate("MainWindow", "Preferences"))
        self.action_save_config.setText(_translate("MainWindow", "Save Config"))
        self.action_about.setText(_translate("MainWindow", "About"))
