#!/usr/bin/python

'''
mainwindow.py
'''
import logging
from PyQt5.QtCore import Qt, QFile, QIODevice, QTextStream
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtGui import QImage, QIcon
import gui.ui.app_ui as ui
import gui.resources.resources
from gui.app_widgets.preprocess_display_widget import PreprocessDisplayWidget
from gui.app_widgets.extract_display_widget import ExtractDisplayWidget


logger = logging.getLogger(__name__)


class AppMainWindow(QMainWindow):
    '''
    AppMainWindow
    '''
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
        self.setWindowIcon(QIcon(':/images/icon.png'))
        self.default_display_widget = self.ui.display_widget

        self.initConnects()
        self.initResources()
        self.onActionPreprocessing()
        return

    def initConnects(self):
        '''
        初始化信号和槽
        '''
        self.ui.action_about.triggered.connect(self.onActionAbout)
        self.ui.action_open.triggered.connect(self.onActionOpen)
        self.ui.action_open_current_control_panel.triggered.connect(self.onActionOpenCurrentControlPanel)
        self.ui.action_preprocessing.triggered.connect(self.onActionPreprocessing)
        self.ui.action_extract_connect_domain.triggered.connect(self.onActionExtratConnectDomain)
        self.ui.action_merging_text_line.triggered.connect(self.onActionMergingTextLine)
        self.ui.action_identify_with_feature.triggered.connect(self.onActionIdentifyWithFeature)
        return

    def initResources(self):
        '''
        初始化资源文件
        '''
        strfile = QFile(':/string/strings')
        strfile.open(QIODevice.ReadOnly | QIODevice.Text)
        ts = QTextStream(strfile)
        key, value = "", ""
        while not ts.atEnd():
            line = ts.readLine()
            if len(line) < 1:
                continue
            if line[0] == '@':
                if key != "":
                    self.strings[key] = value
                    key, value = "", ""
                key = line[1:]
            else:
                value += line
        self.strings[key] = value
        strfile.close()
        return

    def onActionAbout(self):
        '''
        About 响应函数
        '''
        QMessageBox.about(self, "About", self.strings["ABOUT"])
        return

    def onActionOpen(self):
        '''
        Open 响应函数
        '''
        fname, _ = QFileDialog.getOpenFileName(self, "Open file", \
                                        '~', "Image files (*.jpg *.gif)")
        if fname == '':
            return
        input_image = QImage(fname).convertToFormat(QImage.Format_RGB888)
        self.preprocess_display_widget.setImage(input_image)
        return

    def onActionOpenCurrentControlPanel(self):
        '''
        OpenCurrentControlPanel 响应函数
        '''
        self.ui.display_widget.openControlPanel()
        return

    def onActionPreprocessing(self):
        '''
        Stage->Preprocessing 菜单响应函数，将预处理窗口设置为当前窗口
        '''
        if self.preprocess_display_widget is None:
            self.preprocess_display_widget = PreprocessDisplayWidget(self)
            self.preprocess_display_widget.setSizePolicy(self.default_display_widget.sizePolicy())
            self.preprocess_display_widget.setObjectName("prep_display_widget")
        old_display_widget_item = self.ui.verticalLayout.itemAt(0)
        self.ui.verticalLayout.removeItem(old_display_widget_item)
        self.ui.verticalLayout.insertWidget(0, self.preprocess_display_widget)
        self.ui.display_widget = self.preprocess_display_widget

        self.ui.action_preprocessing.setChecked(True)
        self.preprocess_display_widget.show()
        self.ui.action_extract_connect_domain.setChecked(False)
        if self.extract_display_widget is not None:
            self.extract_display_widget.hide()
        self.ui.action_merging_text_line.setChecked(False)
        if self.merging_display_widget is not None:
            self.merging_display_widget.hide()
        self.ui.action_identify_with_feature.setChecked(False)
        if self.ldp_display_widget is not None:
            self.ldp_display_widget.hide()
        return

    def onActionExtratConnectDomain(self):
        '''
        Stage->Extract Connect Domain 菜单响应函数，将连通域提取窗口设置为当前窗口
        '''
        if self.extract_display_widget is None:
            self.extract_display_widget = ExtractDisplayWidget(self)
            self.extract_display_widget.setSizePolicy(self.default_display_widget.sizePolicy())
            self.extract_display_widget.setObjectName("extract_display_widget")
            self.extract_display_widget.requireData.connect(self.onActionExtractorRequireData, Qt.DirectConnection)
        old_display_widget_item = self.ui.verticalLayout.itemAt(0)
        self.ui.verticalLayout.removeItem(old_display_widget_item)
        self.ui.verticalLayout.insertWidget(0, self.extract_display_widget)
        self.ui.display_widget = self.extract_display_widget

        self.ui.action_extract_connect_domain.setChecked(True)
        self.extract_display_widget.show()
        self.ui.action_preprocessing.setChecked(False)
        if self.preprocess_display_widget is not None:
            self.preprocess_display_widget.hide()
        self.ui.action_merging_text_line.setChecked(False)
        if self.merging_display_widget is not None:
            self.merging_display_widget.hide()
        self.ui.action_identify_with_feature.setChecked(False)
        if self.ldp_display_widget is not None:
            self.ldp_display_widget.hide()
        return


    def onActionMergingTextLine(self):
        '''
        Stage->Merging Text Line 菜单响应函数，将文本行合并窗口设置为当前窗口
        '''
        self.ui.action_preprocessing.setChecked(False)
        self.ui.action_extract_connect_domain.setChecked(False)
        self.ui.action_merging_text_line.setChecked(True)
        self.ui.action_identify_with_feature.setChecked(False)
        return


    def onActionIdentifyWithFeature(self):
        '''
        Stage->Identify with Feature 菜单响应函数，将特征鉴别窗口设置为当前窗口
        '''
        self.ui.action_preprocessing.setChecked(False)
        self.ui.action_extract_connect_domain.setChecked(False)
        self.ui.action_merging_text_line.setChecked(False)
        self.ui.action_identify_with_feature.setChecked(True)
        return

    def onActionExtractorRequireData(self, chnls):
        datas = []
        if "Gray" in chnls:
            datas.append(self.preprocess_display_widget.preprocesser.gray_img_preped)
        if "Blue Channel" in chnls:
            datas.append(self.preprocess_display_widget.preprocesser.blue_channel_preped)
        if "Red Channel" in chnls:
            datas.append(self.preprocess_display_widget.preprocesser.red_channel_preped)
        if "Green Channel" in chnls:
            datas.append(self.preprocess_display_widget.preprocesser.green_channel_preped)
        self.extract_display_widget.input_images = datas
        logger.info("Data is fed for extractor")
