#!/usr/bin/python

''' Extract Display Widget
'''
import logging
from PyQt5.QtCore import pyqtSignal
from gui.app_widgets.basic_display_widget import BasicDisplayWidget
from gui.text_detection.extract_connect_domain import TdExtractConnectDomain
from gui.text_detection.region_filter import TdFilter
from gui.app_widgets.extract_control_widget import ExtractDisplayCtrlWidget
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
        config = self.control_panel.getConfiguration()
        self.extracter.setConfig(config)
        self.filter.setConfig(config['filter_params'])
        logger.info("Extractor require datas")
        self.requireData.emit(config['channels'])
        logger.info("Extractor tell data was recevied")

        # 提取连通域
        result_image = self.extracter.extract_with_labels_for_images(self.input_images, self.filter)
        self.setDisplayCvImage(result_image)
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
