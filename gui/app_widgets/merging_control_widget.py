#!/usr/bin/python


''' 连通域提取控制面板
'''

import logging
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon
import gui.ui.merging_textline_control_ui as merge_ctrl_ui
from gui.text_detection.region_filter import TdFilterCheckType
from gui.text_detection.merging_textline import MergingStrategy
from conf.config import TdConfig, TdMergeTLConfig, TdFilterConfig

logger = logging.getLogger(__name__)


class MergeDisplayCtrlWidget(QWidget):
    ''' 连通域提取控制面板
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = merge_ctrl_ui.Ui_MergeCtrlWidget()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(':/images/icon.png'))
        self.setAttribute(Qt.WA_QuitOnClose, False)

        merge_conf = TdConfig().getMergeTLConfig()
        self.ui.linedit_combined_area_size_lim.setText(str(merge_conf['combined_area_size_lim']))
        self.ui.dspinbox_overlap_ratio.setValue(merge_conf['overlap_ratio'])
        self.ui.dspinbox_distance.setValue(merge_conf['distance'])
        self.ui.dspinbox_combined_aspect_ratio_low.setValue(merge_conf['combined_aspect_ratio_lim'][0])
        self.ui.dspinbox_combined_aspect_ratio_high.setValue(merge_conf['combined_aspect_ratio_lim'][1])
        strategy_dict = {"horizon": MergingStrategy.HORIZON.value-1,
                         "vertical": MergingStrategy.VERTICAL.value-1}
        self.ui.combobox_strategy.setCurrentIndex(strategy_dict.get(merge_conf['strategy'], 0))
        self.initConnects()
        return

    def initConnects(self):
        ''' 初始化信号与槽的连接
        '''
        return

    def getConfiguration(self, flag=0):
        ''' 获得配置信息
        '''
        if flag == 0:
            megconf = TdMergeTLConfig()
            megconf.setConfigItem('combined_area_size_lim', int(self.ui.linedit_combined_area_size_lim.text()))
            megconf.setConfigItem('combined_aspect_ratio_lim', [self.ui.dspinbox_combined_aspect_ratio_low.value(), \
                                                                self.ui.dspinbox_combined_aspect_ratio_high.value() \
                                                               ])
            megconf.setConfigItem('overlap_ratio', self.ui.dspinbox_overlap_ratio.value())
            megconf.setConfigItem('distance', self.ui.dspinbox_distance.value())
            megconf.setConfigItem('strategy', self.ui.combobox_strategy.currentText())
            megconf.setConfigItem('show_verbose', self.ui.checkbox_show_verbsoe.isChecked())
            return megconf.getConfig()
        else:
            fltconf = TdFilterConfig()
            fltconf.setConfigItem('default', 'flag', TdFilterCheckType.AREA.value)
            fltconf.setConfigItem('default', 'area_lim', int(self.ui.spinbox_morph_area_size_lim.value()))
            return fltconf.getConfig('default')
