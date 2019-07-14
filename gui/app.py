#!/usr/bin/python

import sys
import ui.app_ui as ui
import mainwindow
from PyQt5.QtWidgets import QApplication,QWidget,QMainWindow
from PyQt5.QtGui import QIcon


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    mw = mainwindow.app_mainwindow()
    mw.show() 
    sys.exit(app.exec_())
