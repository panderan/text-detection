# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/ui/preprocess_control.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PrepCtrlWidget(object):
    def setupUi(self, PrepCtrlWidget):
        PrepCtrlWidget.setObjectName("PrepCtrlWidget")
        PrepCtrlWidget.setWindowModality(QtCore.Qt.NonModal)
        PrepCtrlWidget.resize(447, 332)
        self.verticalLayout = QtWidgets.QVBoxLayout(PrepCtrlWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.paramsLayout = QtWidgets.QFormLayout()
        self.paramsLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.paramsLayout.setObjectName("paramsLayout")
        self.label_total_pixels = QtWidgets.QLabel(PrepCtrlWidget)
        self.label_total_pixels.setObjectName("label_total_pixels")
        self.paramsLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_total_pixels)
        self.linedit_total_pixels = QtWidgets.QLineEdit(PrepCtrlWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.linedit_total_pixels.sizePolicy().hasHeightForWidth())
        self.linedit_total_pixels.setSizePolicy(sizePolicy)
        self.linedit_total_pixels.setMinimumSize(QtCore.QSize(150, 0))
        self.linedit_total_pixels.setObjectName("linedit_total_pixels")
        self.paramsLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.linedit_total_pixels)
        self.label_display_source = QtWidgets.QLabel(PrepCtrlWidget)
        self.label_display_source.setObjectName("label_display_source")
        self.paramsLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_display_source)
        self.combo_sources = QtWidgets.QComboBox(PrepCtrlWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_sources.sizePolicy().hasHeightForWidth())
        self.combo_sources.setSizePolicy(sizePolicy)
        self.combo_sources.setMinimumSize(QtCore.QSize(150, 0))
        self.combo_sources.setObjectName("combo_sources")
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinbox_gama.sizePolicy().hasHeightForWidth())
        self.spinbox_gama.setSizePolicy(sizePolicy)
        self.spinbox_gama.setMinimumSize(QtCore.QSize(100, 0))
        self.spinbox_gama.setObjectName("spinbox_gama")
        self.paramsLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.spinbox_gama)
        self.spinbox_struct_element_size = QtWidgets.QSpinBox(PrepCtrlWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinbox_struct_element_size.sizePolicy().hasHeightForWidth())
        self.spinbox_struct_element_size.setSizePolicy(sizePolicy)
        self.spinbox_struct_element_size.setMinimumSize(QtCore.QSize(100, 0))
        self.spinbox_struct_element_size.setMaximum(1000)
        self.spinbox_struct_element_size.setObjectName("spinbox_struct_element_size")
        self.paramsLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.spinbox_struct_element_size)
        self.label_struct_element_size = QtWidgets.QLabel(PrepCtrlWidget)
        self.label_struct_element_size.setObjectName("label_struct_element_size")
        self.paramsLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_struct_element_size)
        self.label_guass_blur_size = QtWidgets.QLabel(PrepCtrlWidget)
        self.label_guass_blur_size.setObjectName("label_guass_blur_size")
        self.paramsLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_guass_blur_size)
        self.spinbox_guass_blur_size = QtWidgets.QSpinBox(PrepCtrlWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinbox_guass_blur_size.sizePolicy().hasHeightForWidth())
        self.spinbox_guass_blur_size.setSizePolicy(sizePolicy)
        self.spinbox_guass_blur_size.setMinimumSize(QtCore.QSize(100, 0))
        self.spinbox_guass_blur_size.setMaximum(1000)
        self.spinbox_guass_blur_size.setObjectName("spinbox_guass_blur_size")
        self.paramsLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.spinbox_guass_blur_size)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_canny_max = QtWidgets.QLabel(PrepCtrlWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_canny_max.sizePolicy().hasHeightForWidth())
        self.label_canny_max.setSizePolicy(sizePolicy)
        self.label_canny_max.setObjectName("label_canny_max")
        self.horizontalLayout.addWidget(self.label_canny_max)
        self.spinbox_canny_max = QtWidgets.QDoubleSpinBox(PrepCtrlWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinbox_canny_max.sizePolicy().hasHeightForWidth())
        self.spinbox_canny_max.setSizePolicy(sizePolicy)
        self.spinbox_canny_max.setMinimumSize(QtCore.QSize(100, 0))
        self.spinbox_canny_max.setMaximum(1.0)
        self.spinbox_canny_max.setObjectName("spinbox_canny_max")
        self.horizontalLayout.addWidget(self.spinbox_canny_max)
        self.label_canny_min = QtWidgets.QLabel(PrepCtrlWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_canny_min.sizePolicy().hasHeightForWidth())
        self.label_canny_min.setSizePolicy(sizePolicy)
        self.label_canny_min.setObjectName("label_canny_min")
        self.horizontalLayout.addWidget(self.label_canny_min)
        self.spinbox_canny_min = QtWidgets.QDoubleSpinBox(PrepCtrlWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinbox_canny_min.sizePolicy().hasHeightForWidth())
        self.spinbox_canny_min.setSizePolicy(sizePolicy)
        self.spinbox_canny_min.setMinimumSize(QtCore.QSize(100, 0))
        self.spinbox_canny_min.setMaximum(1.0)
        self.spinbox_canny_min.setObjectName("spinbox_canny_min")
        self.horizontalLayout.addWidget(self.spinbox_canny_min)
        self.paramsLayout.setLayout(5, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_canny = QtWidgets.QLabel(PrepCtrlWidget)
        self.label_canny.setObjectName("label_canny")
        self.paramsLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_canny)
        self.label_show_verbose = QtWidgets.QLabel(PrepCtrlWidget)
        self.label_show_verbose.setObjectName("label_show_verbose")
        self.paramsLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_show_verbose)
        self.checkbox_show_verbose = QtWidgets.QCheckBox(PrepCtrlWidget)
        self.checkbox_show_verbose.setChecked(True)
        self.checkbox_show_verbose.setObjectName("checkbox_show_verbose")
        self.paramsLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.checkbox_show_verbose)
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
        self.combo_sources.setItemText(1, _translate("PrepCtrlWidget", "Gray"))
        self.combo_sources.setItemText(2, _translate("PrepCtrlWidget", "Blue Channel"))
        self.combo_sources.setItemText(3, _translate("PrepCtrlWidget", "Red Channel"))
        self.combo_sources.setItemText(4, _translate("PrepCtrlWidget", "Green Channel"))
        self.combo_sources.setItemText(5, _translate("PrepCtrlWidget", "Canny Image"))
        self.label_gama.setText(_translate("PrepCtrlWidget", "Gama :"))
        self.label_struct_element_size.setText(_translate("PrepCtrlWidget", "Struct Element Size :"))
        self.label_guass_blur_size.setText(_translate("PrepCtrlWidget", "Guass Blur Size :"))
        self.label_canny_max.setText(_translate("PrepCtrlWidget", "Max:"))
        self.label_canny_min.setText(_translate("PrepCtrlWidget", "Min:"))
        self.label_canny.setText(_translate("PrepCtrlWidget", "Canny :"))
        self.label_show_verbose.setText(_translate("PrepCtrlWidget", "Show Verbose :"))
        self.checkbox_show_verbose.setText(_translate("PrepCtrlWidget", "Enable"))
        self.btn_ok.setText(_translate("PrepCtrlWidget", "OK"))
