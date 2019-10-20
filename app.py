#!/usr/bin/python

""" GUI APP """

import sys
from PyQt5.QtWidgets import QApplication
from gui import mainwindow


if __name__ == '__main__':
    APP = QApplication(sys.argv)
    MW = mainwindow.AppMainWindow()
    MW.show()
    sys.exit(APP.exec_())
