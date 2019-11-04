# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'verbose_show.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_VerboseDisplay(object):
    def setupUi(self, VerboseDisplay):
        VerboseDisplay.setObjectName("VerboseDisplay")
        VerboseDisplay.resize(1029, 669)
        self.horizontalLayout = QtWidgets.QHBoxLayout(VerboseDisplay)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget_display = QtWidgets.QWidget(VerboseDisplay)
        self.widget_display.setObjectName("widget_display")
        self.horizontalLayout.addWidget(self.widget_display)
        self.line_vertical_1 = QtWidgets.QFrame(VerboseDisplay)
        self.line_vertical_1.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_vertical_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_vertical_1.setObjectName("line_vertical_1")
        self.horizontalLayout.addWidget(self.line_vertical_1)
        self.label_info = QtWidgets.QLabel(VerboseDisplay)
        self.label_info.setEnabled(True)
        self.label_info.setMinimumSize(QtCore.QSize(150, 0))
        self.label_info.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_info.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_info.setObjectName("label_info")
        self.horizontalLayout.addWidget(self.label_info)
        self.line_vertical_2 = QtWidgets.QFrame(VerboseDisplay)
        self.line_vertical_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_vertical_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_vertical_2.setObjectName("line_vertical_2")
        self.horizontalLayout.addWidget(self.line_vertical_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_sources = QtWidgets.QLabel(VerboseDisplay)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_sources.sizePolicy().hasHeightForWidth())
        self.label_sources.setSizePolicy(sizePolicy)
        self.label_sources.setMinimumSize(QtCore.QSize(200, 0))
        self.label_sources.setMaximumSize(QtCore.QSize(200, 16777215))
        self.label_sources.setObjectName("label_sources")
        self.verticalLayout.addWidget(self.label_sources)
        self.combo_sources = QtWidgets.QComboBox(VerboseDisplay)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_sources.sizePolicy().hasHeightForWidth())
        self.combo_sources.setSizePolicy(sizePolicy)
        self.combo_sources.setMinimumSize(QtCore.QSize(200, 0))
        self.combo_sources.setMaximumSize(QtCore.QSize(200, 16777215))
        self.combo_sources.setObjectName("combo_sources")
        self.verticalLayout.addWidget(self.combo_sources)
        self.line_horiz_1 = QtWidgets.QFrame(VerboseDisplay)
        self.line_horiz_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_horiz_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_horiz_1.setObjectName("line_horiz_1")
        self.verticalLayout.addWidget(self.line_horiz_1)
        self.list_view = QtWidgets.QListView(VerboseDisplay)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list_view.sizePolicy().hasHeightForWidth())
        self.list_view.setSizePolicy(sizePolicy)
        self.list_view.setMinimumSize(QtCore.QSize(200, 0))
        self.list_view.setMaximumSize(QtCore.QSize(200, 16777215))
        self.list_view.setObjectName("list_view")
        self.verticalLayout.addWidget(self.list_view)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.setStretch(0, 1)

        self.retranslateUi(VerboseDisplay)
        QtCore.QMetaObject.connectSlotsByName(VerboseDisplay)

    def retranslateUi(self, VerboseDisplay):
        _translate = QtCore.QCoreApplication.translate
        VerboseDisplay.setWindowTitle(_translate("VerboseDisplay", "Verbose Result"))
        self.label_info.setText(_translate("VerboseDisplay", "Info:"))
        self.label_sources.setText(_translate("VerboseDisplay", "Sources:"))
