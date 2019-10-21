#!/usr/bin/python

'''
弹窗显示指定图像
'''

from gui.ui.display_result_ui import Ui_ResultDisplay
from gui.app_widgets.basic_display_widget import BasicDisplayWidget

class DisplayResultWidget(BasicDisplayWidget):
    '''
    弹窗显示指定图像
    '''
    def __init__(self, cv_image, parent=None):
        super().__init__(parent)
        self.ui = Ui_ResultDisplay()
        self.ui.setupUi(self)
        self.setDisplayCvImage(cv_image)