#!/usr/bin/python

''' Merge Display Widget
'''
import logging
import cv2
from PyQt5.QtCore import pyqtSignal
from gui.app_widgets.basic_display_widget import BasicDisplayWidget
from gui.text_detection.morph_ops import TdMorphOperator
from gui.text_detection.region_filter import TdFilter
from gui.text_detection.merging_textline import TdMergingTextLine, threshold_of_position_ratio_for_idcard
from gui.app_widgets.merging_control_widget import MergeDisplayCtrlWidget
from gui.app_widgets.verbose_show_widget import VerboseDisplayWidget
from conf.config import TdConfig

logger = logging.getLogger(__name__)


class MergeDisplayWidget(BasicDisplayWidget):
    ''' 用于显示文本行合并图像的 Widget 控件
    '''

    requireData = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.control_panel = None
        self.filter = TdFilter()
        self.morpher = TdMorphOperator()
        self.merger = TdMergingTextLine()
        self.cur_config = {}
        self.dr_widget = None
        self.input_image = None
        self.color_image = None
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
        megconf = self.control_panel.getConfiguration() if self.control_panel is not None \
                  else TdConfig().getMergeTLConfig()
        fltconf = self.control_panel.getConfiguration(flag=1) if self.control_panel is not None \
                    else TdConfig().getFilterConfig("morph")
        self.merger.setConfig(megconf)
        self.filter.setConfig(fltconf)

        logger.info("Merger require datas.")
        self.requireData.emit()
        logger.info("Merger tell data was recevied")

        # 合并文本行
        self.merger.debug.enableDebug(self.input_image.shape)
        self.merger.debug.setBgColorImage(self.color_image)
        self.merger.get_position_ratio_threshold = threshold_of_position_ratio_for_idcard
        regions = self.morpher.morph_operation(self.input_image, self.filter)
        tlregions = self.merger.mergeTextLine(regions)

        # 显示处理结果
        if megconf['show_verbose'] and self.merger.debug is not None:
            if self.dr_widget is None:
                self.dr_widget = VerboseDisplayWidget()
            self.dr_widget.setMergeVerboseData(self.merger.debug)
            self.dr_widget.show()
        result_image = self.color_image.copy()
        result_image = TdMergingTextLine.drawRegions(result_image, (255, 255, 255), cv2.LINE_4, tlregions)
        self.setDisplayCvImage(result_image)
        return

    def openControlPanel(self):
        ''' 打开参数控制面板
        '''
        if self.control_panel is None:
            self.control_panel = MergeDisplayCtrlWidget()
            self.control_panel.ui.btn_ok.clicked.connect(self.doPreprocess)
        self.control_panel.show()
        return

    def setImage(self, qimage):
        ''' 载入图像
        '''
        self.setDisplayQImage(qimage)
        return
