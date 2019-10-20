#!/usr/bin/python

'''
预处理控制面板
'''

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon
import gui.ui.preprocess_control_ui as prep_ctrl_ui


class PreprocessDisplayCtrlWidget(QWidget):
    '''
    预处理控制面板
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = prep_ctrl_ui.Ui_PrepCtrlWidget()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(':/images/icon.png'))
        return

    def getConfiguration(self):
        '''
        获得配置信息
        '''
        config = {}
        config['TotalPixels'] = self.ui.linedit_total_pixels.text()
        config['Source'] = self.ui.combo_sources.currentText()
        return config
