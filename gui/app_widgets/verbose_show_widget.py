#!/usr/bin/python

'''
弹窗显示指定图像
'''
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from gui.ui.verbose_show_ui import Ui_VerboseDisplay
from gui.app_widgets.basic_display_widget import BasicDisplayWidget


class VerboseDisplayWidget(QWidget):
    '''
    弹窗显示指定图像
    '''
    def __init__(self, cv_images_dict, parent=None):
        super().__init__(parent)
        self.cv_images_dict = cv_images_dict
        self.ui = Ui_VerboseDisplay()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_QuitOnClose, False)
        self.display_widget = BasicDisplayWidget()

        # 替换 display_widget
        old_display_widget = self.ui.widget_display
        old_display_widget_item = self.ui.horizontalLayout.itemAt(0)
        self.ui.horizontalLayout.removeItem(old_display_widget_item)
        self.ui.horizontalLayout.insertWidget(0, self.display_widget)
        old_display_widget.close()

        self.ui.label_info.hide()
        self.ui.line_vertical_2.hide()
        self.ui.list_view.setEnabled(False)

        # 将所有源插入 comboBox 中
        for keystr in cv_images_dict:
            self.ui.combo_sources.addItem(keystr)
        # 显示 comboBox 中第一个图像
        if self.ui.combo_sources.count() > 0:
            self.display_widget.setDisplayCvImage(self.cv_images_dict[self.ui.combo_sources.itemText(0)])
        self.ui.combo_sources.activated.connect(self.onActionActived)

    def onActionActived(self, idx):
        ''' 切换显示
        '''
        if self.ui.combo_sources.count() > 0:
            self.display_widget.setDisplayCvImage(self.cv_images_dict[self.ui.combo_sources.itemText(idx)])
