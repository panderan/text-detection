#!/usr/bin/python

from PyQt5.QtWidgets import QWidget 
import ui.preprocess_control_ui as prep_ctrl_ui


## 预处理控制面板
 #
class PreprocessDisplayCtrlWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = prep_ctrl_ui.Ui_PrepCtrlWidget()
        self.ui.setupUi(self)
        return
    
    def getConfiguration(self):
        config = {}
        config['TotalPixels'] = self.ui.linedit_total_pixels.text()
        config['Source'] = self.ui.combo_sources.currentText()
        return config

