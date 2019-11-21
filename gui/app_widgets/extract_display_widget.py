#!/usr/bin/python

''' Extract Display Widget
'''
import logging
from PyQt5.QtCore import pyqtSignal
from gui.app_widgets.basic_display_widget import BasicDisplayWidget
from gui.text_detection.extract_connect_domain import TdExtractConnectDomain
from gui.text_detection.region_filter import TdFilter
from gui.app_widgets.extract_control_widget import ExtractDisplayCtrlWidget
from gui.app_widgets.verbose_show_widget import VerboseDisplayWidget
from conf.config import TdConfig
# import gui.app_widgets.common as apw_comm
# from gui.app_widgets.popup_display_widget import DisplayResultWidget


logger = logging.getLogger(__name__)


class ExtractDisplayWidget(BasicDisplayWidget):
    ''' 用于显示连通域提取图像的 Widget 控件
    '''

    requireData = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.control_panel = None
        self.extracter = TdExtractConnectDomain()
        self.filter = TdFilter()
        self.cur_config = {}
        self.dr_widget = None
        self.input_images = None
        self.last_result = None
        return

    def paintEvent(self, e):
        ''' 重载绘制函数
        '''
        super().paintEvent(e)
        return

    def doPreprocess(self):
        ''' 进行预处理
        '''
        # 获取参数，进行预处理
        extconf = self.control_panel.getConfiguration(flag=0) if self.control_panel is not None \
                 else TdConfig().getExtractConfig()
        fltconf = self.control_panel.getConfiguration(flag=1) if self.control_panel is not None \
                 else TdConfig().getFilterConfig("extract")
        self.filter.setConfig(fltconf)
        self.extracter.setConfig(extconf)

        # 获取输入数据
        msg = "Extractor require datas. channels:%s."%extconf['channels']
        logger.info(msg)
        self.requireData.emit(extconf['channels'])
        logger.info("Extractor tell data was recevied")

        # 提取连通域
        self.extracter.debug_enable = extconf['debug']
        self.last_result = self.extracter.extract_with_labels_for_images(self.input_images, self.filter)

        # 显示处理结果
        if extconf['show_verbose'] and self.extracter.debug_data is not None:
            if self.dr_widget is None:
                self.dr_widget = VerboseDisplayWidget()
            self.dr_widget.setExtracterVerboseData(self.extracter.debug_data)
            self.dr_widget.show()
        self.setDisplayCvImage(self.last_result)
        return

    def openControlPanel(self):
        ''' 打开参数控制面板
        '''
        if self.control_panel is None:
            self.control_panel = ExtractDisplayCtrlWidget()
            self.control_panel.ui.btn_ok.clicked.connect(self.doPreprocess)
        self.control_panel.show()
        return

    def setImage(self, qimage):
        ''' 载入图像
        '''
        self.setDisplayQImage(qimage)
        return

    @property
    def last_result(self):
        '''
        获取 Gray 预处理后图像，获取时计算
        '''
        if self.__last_result is None:
            self.doPreprocess()
        return self.__last_result
    @last_result.setter
    def last_result(self, val):
        self.__last_result = val
