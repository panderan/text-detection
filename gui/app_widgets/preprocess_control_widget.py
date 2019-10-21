#!/usr/bin/python

'''
预处理控制面板
'''

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon
import gui.ui.preprocess_control_ui as prep_ctrl_ui
from config.config import TdConfig

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
        return

    def getConfiguration(self):
        '''
        获得配置信息
        '''
        config = {}
        config['TotalPixels'] = self.ui.linedit_total_pixels.text()
        config['Source'] = self.ui.combo_sources.currentText()
        config['StructElementSize'] = self.ui.spinbox_struct_element_size.value()
        config['GaussBlurSize'] = self.ui.spinbox_guass_blur_size.value()
        config['Gamma'] = self.ui.spinbox_gama.value()
        return config
