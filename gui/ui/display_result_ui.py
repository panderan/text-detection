# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'display_result.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ResultDisplay(object):
    def setupUi(self, ResultDisplay):
        ResultDisplay.setObjectName("ResultDisplay")
        ResultDisplay.resize(627, 474)
        self.combo_sources = QtWidgets.QComboBox(ResultDisplay)
        self.combo_sources.setGeometry(QtCore.QRect(0, 0, 171, 31))
        self.combo_sources.setObjectName("combo_sources")

        self.retranslateUi(ResultDisplay)
        QtCore.QMetaObject.connectSlotsByName(ResultDisplay)

    def retranslateUi(self, ResultDisplay):
        _translate = QtCore.QCoreApplication.translate
        ResultDisplay.setWindowTitle(_translate("ResultDisplay", "Display Result"))
