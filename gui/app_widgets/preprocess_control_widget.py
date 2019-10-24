#!/usr/bin/python

'''
预处理控制面板
'''

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon
import gui.ui.preprocess_control_ui as prep_ctrl_ui
from conf.config import TdConfig

class PreprocessDisplayCtrlWidget(QWidget):
    '''
    预处理控制面板
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = prep_ctrl_ui.Ui_PrepCtrlWidget()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(':/images/icon.png'))

        conf_from_file = TdConfig().getPrepConfig()
        self.ui.linedit_total_pixels.setText(str(conf_from_file["total_pixels"]))
        self.ui.spinbox_gama.setValue(conf_from_file["gamma"])
        self.ui.spinbox_guass_blur_size.setValue(conf_from_file["gauss_blur_size"])
        self.ui.spinbox_struct_element_size.setValue(conf_from_file["struct_element_size"])
        self.ui.spinbox_canny_max.setValue(conf_from_file["canny"][0])
        self.ui.spinbox_canny_min.setValue(conf_from_file["canny"][1])
        return

    def getConfiguration(self):
        '''
        获得配置信息
        '''
        config = {}
        config['total_pixels'] = self.ui.linedit_total_pixels.text()
        config['source'] = self.ui.combo_sources.currentText()
        config['struct_element_size'] = self.ui.spinbox_struct_element_size.value()
        config['gauss_blur_size'] = self.ui.spinbox_guass_blur_size.value()
        config['gamma'] = self.ui.spinbox_gama.value()
        config['canny'] = [self.ui.spinbox_canny_max.value(), self.ui.spinbox_canny_min.value()]
        return config
