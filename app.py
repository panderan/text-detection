#!/usr/bin/python

""" GUI APP """

import sys
import logging
from PyQt5.QtWidgets import QApplication
from gui import mainwindow


logging.basicConfig(level=logging.INFO, \
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', \
                    datefmt='%a, %d %b %Y %H:%M:%S')
logger = logging.getLogger(__name__)


if __name__ == '__main__':

    logger.info("Text Detection Started")
    APP = QApplication(sys.argv)
    MW = mainwindow.AppMainWindow()
    MW.show()
    sys.exit(APP.exec_())
