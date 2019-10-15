#!/usr/bin/python

import sys
import ui.app_ui as ui
import resources.resources
from PyQt5.QtCore import QFile,QIODevice,QTextStream
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon, QImage
from display_widget import DisplayWidget

class app_mainwindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.strings = {}
        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_connects()
        self.init_resources()       

    def init_connects(self):
        self.ui.action_about.triggered.connect(self.on_action_about)
        self.ui.action_open.triggered.connect(self.on_action_open)

    def init_resources(self):
        strfile = QFile(':/string/strings')
        strfile.open(QIODevice.ReadOnly | QIODevice.Text)
        ts = QTextStream(strfile)
        key,value="",""
        while ts.atEnd() == False:
            line = ts.readLine()
            if len(line) < 1:
                continue
            elif line[0] == '@':
                if key!="":
                    self.strings[key] = value
                    key,value="",""
                key = line[1:]
            else:
                value += line 
        self.strings[key] = value
        strfile.close()
    
    def on_action_about(self):
        QMessageBox.about(self, "关于", self.strings["ABOUT"])

    def on_action_open(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Open file", \
                                        '~', "Image files (*.jpg *.gif)");
        input_image = QImage(fname)
        self.ui.display_widget.setDisplayQImage(input_image)

