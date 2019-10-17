#!/usr/bin/python

import ui.app_ui as ui
import resources.resources
from PyQt5.QtCore import QFile,QIODevice,QTextStream
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtGui import QImage
from app_widgets.preprocess_display_widget import PreprocessDisplayWidget

class AppMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.strings = {}
        self.default_display_widget = None
        self.preprocess_display_widget = None
        self.extract_display_widget = None
        self.merging_display_widget = None
        self.ldp_display_widget = None

        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.default_display_widget = self.ui.display_widget

        self.initConnects()
        self.initResources()       
        self.setPreprocessDisplayWidget()
        return

    def initConnects(self):
        self.ui.action_about.triggered.connect(self.onActionAbout)
        self.ui.action_open.triggered.connect(self.onActionOpen)
        self.ui.action_open_current_control_panel.triggered.connect(self.onActionOpenCurrentControlPanel)
        return

    def initResources(self):
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
        return

    def setPreprocessDisplayWidget(self):
        if (self.preprocess_display_widget == None): 
            self.preprocess_display_widget = PreprocessDisplayWidget(self)
            self.preprocess_display_widget.setSizePolicy(self.default_display_widget.sizePolicy())
            self.preprocess_display_widget.setObjectName("prep_display_widget")
        old_display_widget_item = self.ui.verticalLayout.itemAt(0)
        self.ui.verticalLayout.removeItem(old_display_widget_item)
        self.ui.verticalLayout.insertWidget(0, self.preprocess_display_widget)
        self.ui.display_widget = self.preprocess_display_widget
        return
    
    def onActionAbout(self):
        QMessageBox.about(self, "About", self.strings["ABOUT"])
        return

    def onActionOpen(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Open file", \
                                        '~', "Image files (*.jpg *.gif)");
        input_image = QImage(fname)
        self.ui.display_widget.setImage(input_image)
        return

    def onActionOpenCurrentControlPanel(self):
        self.preprocess_display_widget.openControlPanel()
        return

