# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'preprocess_control.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PrepCtrlWidget(object):
    def setupUi(self, PrepCtrlWidget):
        PrepCtrlWidget.setObjectName("PrepCtrlWidget")
        PrepCtrlWidget.resize(319, 262)
        self.verticalLayout = QtWidgets.QVBoxLayout(PrepCtrlWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.paramsLayout = QtWidgets.QFormLayout()
        self.paramsLayout.setObjectName("paramsLayout")
        self.label_total_pixels = QtWidgets.QLabel(PrepCtrlWidget)
        self.label_total_pixels.setObjectName("label_total_pixels")
        self.paramsLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_total_pixels)
        self.linedit_total_pixels = QtWidgets.QLineEdit(PrepCtrlWidget)
        self.linedit_total_pixels.setObjectName("linedit_total_pixels")
        self.paramsLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.linedit_total_pixels)
        self.label_display_source = QtWidgets.QLabel(PrepCtrlWidget)
        self.label_display_source.setObjectName("label_display_source")
        self.paramsLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_display_source)
        self.combo_sources = QtWidgets.QComboBox(PrepCtrlWidget)
        self.combo_sources.setObjectName("combo_sources")
        self.combo_sources.addItem("")
        self.combo_sources.addItem("")
        self.combo_sources.addItem("")
        self.combo_sources.addItem("")
        self.combo_sources.addItem("")
        self.combo_sources.addItem("")
        self.combo_sources.addItem("")
        self.combo_sources.addItem("")
        self.combo_sources.addItem("")
        self.combo_sources.addItem("")
        self.paramsLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.combo_sources)
        self.label_gama = QtWidgets.QLabel(PrepCtrlWidget)
        self.label_gama.setObjectName("label_gama")
        self.paramsLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_gama)
        self.spinbox_gama = QtWidgets.QDoubleSpinBox(PrepCtrlWidget)
        self.spinbox_gama.setObjectName("spinbox_gama")
        self.paramsLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.spinbox_gama)
        self.verticalLayout.addLayout(self.paramsLayout)
        self.btn_ok = QtWidgets.QPushButton(PrepCtrlWidget)
        self.btn_ok.setObjectName("btn_ok")
        self.verticalLayout.addWidget(self.btn_ok)

        self.retranslateUi(PrepCtrlWidget)
        QtCore.QMetaObject.connectSlotsByName(PrepCtrlWidget)

    def retranslateUi(self, PrepCtrlWidget):
        _translate = QtCore.QCoreApplication.translate
        PrepCtrlWidget.setWindowTitle(_translate("PrepCtrlWidget", "Preprocess Control Panel"))
        self.label_total_pixels.setText(_translate("PrepCtrlWidget", "Total Pixels :"))
        self.linedit_total_pixels.setText(_translate("PrepCtrlWidget", "400000"))
        self.label_display_source.setText(_translate("PrepCtrlWidget", "Display Source :"))
        self.combo_sources.setItemText(0, _translate("PrepCtrlWidget", "Color Image (RGB)"))
        self.combo_sources.setItemText(1, _translate("PrepCtrlWidget", "Blue Channel"))
        self.combo_sources.setItemText(2, _translate("PrepCtrlWidget", "Red Channel"))
        self.combo_sources.setItemText(3, _translate("PrepCtrlWidget", "Green Channel"))
        self.combo_sources.setItemText(4, _translate("PrepCtrlWidget", "Canny Image"))
        self.combo_sources.setItemText(5, _translate("PrepCtrlWidget", "Sobel X"))
        self.combo_sources.setItemText(6, _translate("PrepCtrlWidget", "Sobel Y"))
        self.combo_sources.setItemText(7, _translate("PrepCtrlWidget", "Magnitudes"))
        self.combo_sources.setItemText(8, _translate("PrepCtrlWidget", "Grads X"))
        self.combo_sources.setItemText(9, _translate("PrepCtrlWidget", "Grads Y"))
        self.label_gama.setText(_translate("PrepCtrlWidget", "Gama :"))
        self.btn_ok.setText(_translate("PrepCtrlWidget", "OK"))
