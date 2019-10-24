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
    def __init__(self, cv_images_dict, parent=None):
        super().__init__(parent)
        self.cv_images_dict = cv_images_dict
        self.ui = Ui_ResultDisplay()
        self.ui.setupUi(self)

        # 将所有源插入 comboBox 中
        for keystr in cv_images_dict:
            self.ui.combo_sources.addItem(keystr)
        # 显示 comboBox 中第一个图像
        if self.ui.combo_sources.count() > 0:
            self.setDisplayCvImage(self.cv_images_dict[self.ui.combo_sources.itemText(0)])
        self.ui.combo_sources.activated.connect(self.onActionActived)

    def onActionActived(self, idx):
        '''
        切换显示
        '''
        if self.ui.combo_sources.count() > 0:
            self.setDisplayCvImage(self.cv_images_dict[self.ui.combo_sources.itemText(idx)])
