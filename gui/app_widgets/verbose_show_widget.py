#!/usr/bin/python

'''
弹窗显示指定图像
'''
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QListWidgetItem
from gui.ui.verbose_show_ui import Ui_VerboseDisplay
from gui.app_widgets.basic_display_widget import BasicDisplayWidget
from gui.text_detection.merging_textline import debugGenerateElectionImage
import cv2
import numpy as np

class VerboseDisplayWidget(QWidget):
    ''' 弹窗显示指定图像
    '''
    cv_image = None
    temp_image_1 = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.cv_verbose_dict = None
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
        self.ui.line_horiz_2.hide()
        self.ui.checkbox_color_keep.hide()
        self.ui.checkbox_use_final_ret_as_bg.hide()
        self.ui.list_widget.setEnabled(False)
        self.ui.list_widget_sec.setEnabled(False)
        self.ui.list_widget_sec.setVisible(False)

    def onActionStateChangeUseFinalRetAsBg(self, state):
        self.temp_image_1 = None
        self.cv_image = None

    def setPrepVerboseData(self, cv_verbose_dict):
        ''' 添加 Prep Verbose 数据
        '''
        self.cv_verbose_dict = cv_verbose_dict

        # 将所有源插入 comboBox 中
        self.ui.combo_sources.clear()
        for keystr in cv_verbose_dict:
            self.ui.combo_sources.addItem(keystr)
        # 显示 comboBox 中第一个图像
        if self.ui.combo_sources.count() > 0:
            self.display_widget.setDisplayCvImage(self.cv_verbose_dict[self.ui.combo_sources.itemText(0)])
        self.ui.combo_sources.activated.connect(self.onActionPrepActived)

    def onActionPrepActived(self, idx):
        ''' 切换显示
        '''
        if self.ui.combo_sources.count() > 0:
            self.display_widget.setDisplayCvImage(self.cv_verbose_dict[self.ui.combo_sources.itemText(idx)])

    def setExtracterVerboseData(self, cv_verbose_dict):
        ''' 添加 Extracter Verbose 数据
        '''
        self.clearData()
        self.cv_verbose_dict = cv_verbose_dict
        self.ui.combo_sources.clear()
        for item in cv_verbose_dict:
            self.ui.combo_sources.addItem(item["name"])

        self.ui.label_info.setVisible(True)
        self.ui.line_horiz_2.setVisible(True)
        self.ui.checkbox_color_keep.setVisible(True)
        self.ui.checkbox_use_final_ret_as_bg.setVisible(True)
        self.ui.label_info.setText("Info:\n")
        self.ui.list_widget.setEnabled(True)
        self.onActionExtracterActived(0)
        self.ui.combo_sources.activated.connect(self.onActionExtracterActived)
        self.ui.list_widget.itemSelectionChanged.connect(self.onActionExtracterItemSelectionChanged)
        self.ui.checkbox_use_final_ret_as_bg.stateChanged.connect(self.onActionStateChangeUseFinalRetAsBg)

    def onActionExtracterActived(self, idx):
        ''' 切换显示
        '''
        cur_data = self.cv_verbose_dict[idx]
        self.display_widget.setDisplayCvImage(cur_data["result"])

        self.ui.list_widget.clear()
        for i in range(len(cur_data["regions"])):
            self.ui.list_widget.addItem(QListWidgetItem("region_"+str(i), self.ui.list_widget))

    def onActionExtracterItemSelectionChanged(self):
        ''' 显示
        '''
        row = self.ui.list_widget.currentRow()
        if row < 0:
            return

        cur_data = self.cv_verbose_dict[self.ui.combo_sources.currentIndex()]
        cur_info = cur_data["regions"][row]
        message = "Info Idx:" + str(row) + "\n----------------\n"
        if cur_info['flt_params']['area'] is not None:
            message = message + "("+str(cur_info['flt_params']['area']['result'])+") Area:\n    "\
                              + str(cur_info['flt_params']['area']['value']) + " ∈ " \
                              + str(cur_info['flt_params']['area']['lim']) + "\n"
        if cur_info['flt_params']['width'] is not None:
            message = message + "("+str(cur_info['flt_params']['width']['result'])+") Width:\n    "\
                              + str(cur_info['flt_params']['width']['value']) + " ∈ " \
                              + str(cur_info['flt_params']['width']['lim']) + "\n"
        if cur_info['flt_params']['height'] is not None:
            message = message + "("+str(cur_info['flt_params']['height']['result'])+") Height:\n    "\
                              + str(cur_info['flt_params']['height']['value']) + " ∈ " \
                              + str(cur_info['flt_params']['height']['lim']) + "\n"
        if cur_info['flt_params']['perimeter'] is not None:
            message = message + "("+str(cur_info['flt_params']['perimeter']['result'])+") Perimeter:\n    "\
                              + str(cur_info['flt_params']['perimeter']['value']) + " > " \
                              + str(cur_info['flt_params']['perimeter']['lim']) + "\n"
        if cur_info['flt_params']['aspect_ratio'] is not None:
            message = message + "("+str(cur_info['flt_params']['aspect_ratio']['result'])+") Aspect Ratio:\n    "\
                              + str(format(cur_info['flt_params']['aspect_ratio']['value'], '.3f')) + " ∈ " \
                              + str(cur_info['flt_params']['aspect_ratio']['lim']) + "\n"
        if cur_info['flt_params']['occupation_ratio'] is not None:
            message = message + "("+str(cur_info['flt_params']['occupation_ratio']['result'])+") Occupation Ratio:\n    "\
                              + str(format(cur_info['flt_params']['occupation_ratio']['value'], '.3f')) + " ∈ " \
                              + str(cur_info['flt_params']['occupation_ratio']['lim']) + "\n"
        if cur_info['flt_params']['compactness'] is not None:
            message = message + "("+str(cur_info['flt_params']['compactness']['result'])+") Compactness:\n    "\
                              + str(format(cur_info['flt_params']['compactness']['value'], '.3f')) + " ∈ " \
                              + str(cur_info['flt_params']['compactness']['lim']) + "\n"
        self.ui.label_info.setText(message)

        # temp_image_1 作为背景图像
        if self.temp_image_1 is None:
            if self.ui.checkbox_use_final_ret_as_bg.isChecked():
                self.temp_image_1 = np.zeros_like(cur_data['result'])
                for item in self.cv_verbose_dict:
                    self.temp_image_1[:, :] = item['result'][:, :]
            else:
                self.temp_image_1 = cur_data['result'].copy()

        if self.cv_image is None:
            self.cv_image = self.temp_image_1.copy()
            self.cv_image = cv2.cvtColor(self.cv_image, cv2.COLOR_GRAY2RGB)
        else:
            if not self.ui.checkbox_color_keep.isChecked():
                self.cv_image[:, :, 0] = self.temp_image_1[:, :]
                self.cv_image[:, :, 1] = self.temp_image_1[:, :]
                self.cv_image[:, :, 2] = self.temp_image_1[:, :]

        self.cv_image[cur_info['points'][:, 1], cur_info['points'][:, 0], 0] = 255
        self.cv_image[cur_info['points'][:, 1], cur_info['points'][:, 0], 1] = 0
        self.cv_image[cur_info['points'][:, 1], cur_info['points'][:, 0], 2] = 0
        self.display_widget.setDisplayCvImage(self.cv_image)

    def setMergingVerboseData(self, cv_verbose_dict):
        ''' 添加 Merging Verbose 数据
        '''
        self.clearData()
        self.cv_verbose_dict = cv_verbose_dict
        self.ui.label_info.setVisible(True)
        self.ui.label_info.setText("Info:\n")
        self.ui.combo_sources.clear()
        self.ui.combo_sources.setEnabled(False)
        self.ui.combo_sources.setVisible(False)

        election = self.cv_verbose_dict['election']
        self.ui.list_widget.clear()
        self.ui.list_widget.setVisible(True)
        self.ui.list_widget.setEnabled(True)
        for i in range(len(election)):
            self.ui.list_widget.addItem(QListWidgetItem("election_"+str(i), self.ui.list_widget))

        self.ui.list_widget_sec.clear()
        self.ui.list_widget_sec.setVisible(True)
        self.ui.list_widget_sec.setEnabled(True)

    def onActionListWidgetSecMergingItemSelectionChanged(self, idx):
        ''' 切换显示
        '''
        image = debugGenerateElectionImage(self.cv_verbose_dict, idx)
        self.display_widget.setDisplayCvImage(image)

    def clearData(self):
        ''' 删除所有数据
        '''
        self.temp_image_1 = None
        self.cv_image = None
        self.ui.combo_sources.clear()
        self.ui.list_widget.clear()
        self.ui.label_info.setText("Info:")
        self.display_widget.setDisplayCvImage(None)

