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
from gui.app_widgets.merging_display_widget import MergeDisplayWidget
from conf.config import TdConfig

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
        self.createPrepDisplayWidget()
        self.createExtractDisplayWidget()
        self.createMergeDisplayWidget()
        self.createIdentifyWithFeatureDisplayWidget()

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

    def _onlyShow(self, tgtname):
        ''' 只显示某一模块的 widget
        '''
        data = [{'name':"prep",
                 'obj': self.preprocess_display_widget,
                 'checked_obj':self.ui.action_preprocessing},
                {'name':"extract",
                 'obj': self.extract_display_widget,
                 'checked_obj':self.ui.action_extract_connect_domain},
                {'name':"merge",
                 'obj': self.merging_display_widget,
                 'checked_obj':self.ui.action_merging_text_line},
                {'name':"feature",
                 'obj': self.ldp_display_widget,
                 'checked_obj':self.ui.action_identify_with_feature}]
        for item in data:
            if item['name'] == tgtname:
                item['obj'].show()
                item['checked_obj'].setChecked(True)
            else:
                if item['obj'] is not None:
                    item['obj'].hide()
                item['checked_obj'].setChecked(False)

    def createPrepDisplayWidget(self):
        ''' 创建 Prep Display Widget
        '''
        if self.preprocess_display_widget is None:
            self.preprocess_display_widget = PreprocessDisplayWidget(self)
            self.preprocess_display_widget.setSizePolicy(self.default_display_widget.sizePolicy())
            self.preprocess_display_widget.setObjectName("prep_display_widget")
            self.preprocess_display_widget.hide()

    def createExtractDisplayWidget(self):
        ''' 创建 Extract Display Widget
        '''
        if self.extract_display_widget is None:
            self.extract_display_widget = ExtractDisplayWidget(self)
            self.extract_display_widget.setSizePolicy(self.default_display_widget.sizePolicy())
            self.extract_display_widget.setObjectName("extract_display_widget")
            self.extract_display_widget.requireData.connect(self.onActionExtractorRequireData, Qt.DirectConnection)
            self.extract_display_widget.hide()

    def createMergeDisplayWidget(self):
        ''' 创建 Merge Display Widget
        '''
        if self.merging_display_widget is None:
            self.merging_display_widget = MergeDisplayWidget(self)
            self.merging_display_widget.setSizePolicy(self.default_display_widget.sizePolicy())
            self.merging_display_widget.setObjectName("merge_display_widget")
            self.merging_display_widget.requireData.connect(self.onActionMergerRequireData, Qt.DirectConnection)
            self.merging_display_widget.hide()

    def createIdentifyWithFeatureDisplayWidget(self):
        ''' 创建 IdentifyWithFeature 窗体
        '''

    def onActionPreprocessing(self):
        '''
        Stage->Preprocessing 菜单响应函数，将预处理窗口设置为当前窗口
        '''
        self.createPrepDisplayWidget()
        old_display_widget_item = self.ui.verticalLayout.itemAt(0)
        self.ui.verticalLayout.removeItem(old_display_widget_item)
        self.ui.verticalLayout.insertWidget(0, self.preprocess_display_widget)
        self.ui.display_widget = self.preprocess_display_widget
        self._onlyShow("prep")
        return

    def onActionExtratConnectDomain(self):
        '''
        Stage->Extract Connect Domain 菜单响应函数，将连通域提取窗口设置为当前窗口
        '''
        self.createExtractDisplayWidget()
        old_display_widget_item = self.ui.verticalLayout.itemAt(0)
        self.ui.verticalLayout.removeItem(old_display_widget_item)
        self.ui.verticalLayout.insertWidget(0, self.extract_display_widget)
        self.ui.display_widget = self.extract_display_widget
        self._onlyShow("extract")
        return

    def onActionMergingTextLine(self):
        '''
        Stage->Merging Text Line 菜单响应函数，将文本行合并窗口设置为当前窗口
        '''
        self.createMergeDisplayWidget()
        old_display_widget_item = self.ui.verticalLayout.itemAt(0)
        self.ui.verticalLayout.removeItem(old_display_widget_item)
        self.ui.verticalLayout.insertWidget(0, self.merging_display_widget)
        self.ui.display_widget = self.merging_display_widget
        self._onlyShow("merge")
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
        ''' 获取 Extracter 所需的数据
        '''
        config = TdConfig().getPrepConfig() if self.preprocess_display_widget.control_panel is None \
                                            else self.preprocess_display_widget.control_panel.getConfiguration()
        self.preprocess_display_widget.preprocesser.setConfig(config)

        datas = []
        if "Gray" in chnls:
            datas.append({"name":"Gray",
                          "image":self.preprocess_display_widget.preprocesser.gray_img_preped})
        if "Blue Channel" in chnls:
            datas.append({"name":"Blue Channel",
                          "image":self.preprocess_display_widget.preprocesser.blue_channel_preped})
        if "Red Channel" in chnls:
            datas.append({"name":"Red Channel",
                          "image":self.preprocess_display_widget.preprocesser.red_channel_preped})
        if "Green Channel" in chnls:
            datas.append({"name":"Green Channel",
                          "image":self.preprocess_display_widget.preprocesser.green_channel_preped})
        self.extract_display_widget.input_images = datas

        msg = "Data is fed for extractor. channels:%s."%chnls
        logger.info(msg)

    def onActionMergerRequireData(self):
        ''' 获取 Merger 所需的数据
        '''
        self.merging_display_widget.input_image = self.extract_display_widget.last_result
        self.merging_display_widget.color_image = self.preprocess_display_widget.preprocesser.color_img
        msg = "Data is fed for merger"
        logger.info(msg)
