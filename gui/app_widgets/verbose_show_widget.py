#!/usr/bin/python

'''
弹窗显示指定图像
'''
import cv2
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QListWidgetItem
from gui.ui.verbose_show_ui import Ui_VerboseDisplay
from gui.app_widgets.basic_display_widget import BasicDisplayWidget
from gui.text_detection.merging_textline import debugGenerateCompareImage

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
        self.setWindowIcon(QIcon(':/images/verbose.png'))

        # 替换 display_widget
        old_display_widget = self.ui.widget_display
        old_display_widget_item = self.ui.horizontalLayout.itemAt(0)
        self.ui.horizontalLayout.removeItem(old_display_widget_item)
        self.ui.horizontalLayout.insertWidget(0, self.display_widget)
        old_display_widget.close()

    def onActionStateChangeUseFinalRetAsBg(self, state):
        ''' 使用最终结果图最为背景
        '''
        self.temp_image_1 = None
        self.cv_image = None

    def setPrepVerboseData(self, cv_verbose_dict):
        ''' 添加 Prep Verbose 数据
        '''
        self.clearData()
        self.ui.label_sources.setVisible(True)
        self.ui.combo_sources.setVisible(True)
        self.ui.line_horiz_1.setVisible(True)
        self.ui.list_widget.setEnabled(False)
        self.ui.list_widget.setVisible(False)
        self.ui.line_horiz_2.setVisible(False)
        self.ui.checkbox_color_keep.setVisible(False)
        self.ui.checkbox_use_final_ret_as_bg.setVisible(False)
        self.ui.line_horiz_3.setVisible(False)
        self.ui.textbrowser_info.setVisible(False)
        self.ui.textbrowser_info.setText("Info:\n")
        self.ui.list_widget_sec.setVisible(False)
        self.ui.list_widget_sec.setEnabled(False)
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
        self.ui.label_sources.setVisible(True)
        self.ui.combo_sources.setVisible(True)
        self.ui.line_horiz_1.setVisible(True)
        self.ui.list_widget.setEnabled(True)
        self.ui.list_widget.setVisible(True)
        self.ui.line_horiz_2.setVisible(True)
        self.ui.checkbox_color_keep.setVisible(True)
        self.ui.checkbox_use_final_ret_as_bg.setVisible(True)
        self.ui.line_horiz_3.setVisible(True)
        self.ui.textbrowser_info.setVisible(True)
        self.ui.textbrowser_info.setText("Info:\n")
        self.ui.list_widget_sec.setVisible(False)
        self.ui.list_widget_sec.setEnabled(False)

        self.cv_verbose_dict = cv_verbose_dict
        self.ui.combo_sources.clear()
        for item in cv_verbose_dict:
            self.ui.combo_sources.addItem(item["name"])

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
        self.ui.textbrowser_info.setText(message)

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

    def setMergeVerboseData(self, cv_verbose_dict):
        ''' 添加 Merging Verbose 数据
        '''
        self.clearData()
        self.ui.label_sources.setVisible(False)
        self.ui.combo_sources.setVisible(False)
        self.ui.line_horiz_1.setVisible(False)
        self.ui.list_widget.setEnabled(True)
        self.ui.list_widget.setVisible(True)
        self.ui.line_horiz_2.setVisible(False)
        self.ui.checkbox_color_keep.setVisible(False)
        self.ui.checkbox_use_final_ret_as_bg.setVisible(False)
        self.ui.line_horiz_3.setVisible(True)
        self.ui.textbrowser_info.setVisible(True)
        self.ui.textbrowser_info.setText("Info:\n")
        self.ui.list_widget_sec.setVisible(True)
        self.ui.list_widget_sec.setEnabled(True)
        self.cv_verbose_dict = cv_verbose_dict

        self.ui.combo_sources.clear()
        self.ui.list_widget.clear()
        self.ui.list_widget.setVisible(True)
        self.ui.list_widget.setEnabled(True)
        for i in range(self.cv_verbose_dict.getTotalElections()):
            self.ui.list_widget.addItem(QListWidgetItem("election_"+str(i), self.ui.list_widget))
        self.ui.list_widget.itemSelectionChanged.connect(self.onAction_ListWidget_Merging_ItemSelectionChanged)

        self.ui.list_widget_sec.clear()
        self.ui.list_widget_sec.setVisible(True)
        self.ui.list_widget_sec.setEnabled(True)
        self.ui.list_widget_sec.itemSelectionChanged.connect(self.onAction_ListWidgetSec_Merging_ItemSelectionChanged)

    def onAction_ListWidget_Merging_ItemSelectionChanged(self):
        ''' 切换显示
        '''
        self.ui.list_widget_sec.clear()
        elec_idx = self.ui.list_widget.currentRow()
        chosen_id = self.cv_verbose_dict.getElection_ChosenId(elec_idx)
        for i in range(self.cv_verbose_dict.getElection_TotalSatisfied(elec_idx)):
            sat_id = self.cv_verbose_dict.getElection_SatisfiedId(elec_idx, i)
            self.ui.list_widget_sec.addItem(QListWidgetItem("%d-%s-%d"%(elec_idx, str(bool(sat_id == chosen_id)), i)))
        self.ui.list_widget_sec.setCurrentRow(0)

    def onAction_ListWidgetSec_Merging_ItemSelectionChanged(self):
        ''' 切换显示
        '''
        text = self.ui.list_widget_sec.currentItem().text()
        elec_idx, _, sat_idx = text.split('-')
        elec_idx = int(elec_idx)
        sat_idx = int(sat_idx)
        item = self.cv_verbose_dict.getElection_SatisfiedItem(elec_idx, sat_idx)
        cur_id = self.cv_verbose_dict.getElection_CurId(elec_idx)
        sat_id = item['id']

        orig_data = self.cv_verbose_dict.getOriginalRegionData()
        t1 = "ID:%d [w:%d h:%d s:%d a:%.3f]\n"%(cur_id, orig_data.getParamWidth(cur_id), \
                                orig_data.getParamHeight(cur_id), \
                                orig_data.getParamAreaSize(cur_id), \
                                orig_data.getParamAspectRatio(cur_id))
        t2 = "ID:%d [w:%d h:%d s:%d a:%.3f]\n"%(sat_id, orig_data.getParamWidth(sat_id), \
                                orig_data.getParamHeight(sat_id), \
                                orig_data.getParamAreaSize(sat_id), \
                                orig_data.getParamAspectRatio(sat_id))
        text = "Region ID:%s - %s\n"%(str(cur_id), str(sat_id))
        text += (t1 + t2)

        text += "Joint Area Size:\n"
        value = item['compare_params'].get('joint_area_size', None)
        text += "  none\n" if value is None else "  %.3f (< %.3f)\n"%(value[0], value[1])

        text += "Joint Aspect Ratio:\n"
        value = item['compare_params'].get('joint_aspect_ratio', None)
        text += "  none\n" if value is None else "  %.3f in [%.3f, %.3f]\n"%(value[0], value[1][0], value[1][1])

        text += "Overlap Ratio:\n"
        value = item['compare_params'].get('overlap_ratio', None)
        text += "  none\n" if value is None else " %.3f (%.3f)\n"%(value[0], value[1])

        text += "Position Ratio:\n"
        value = item['compare_params'].get('position_ratio', None)
        text += "  none\n" if value is None else "  %.3f (> %.3f)\n"%(value[0], value[1])

        text += "Direction:\n"
        value = item['compare_params'].get('direction', None)
        text += "  none\n" if value is None else \
                "  dir1:%.3f\n"%value[0] + \
                "  dir2:%.3f\n"%value[1] + \
                "  centerLineDir:%.3f\n"%value[2] + \
                "  threshold:[%.3f, %.3f]\n"%(value[3][0], value[3][1]) + \
                "  dirtype:%d\n"%value[4] + \
                "  ret1:%s\n"%value[5] + \
                "  ret2:%s\n"%value[6]

        text += "Distance:\n"
        value = item['compare_params'].get('distance', None)
        text += "  none\n" if value is None else \
                "  kel size: %d\n"%value[0] + \
                "  retval: %s\n"%value[1]

        text += "Strategy:\n"
        value = item['compare_params'].get('strategy', None)
        text += "  none\n" if value is None else \
                "  center1: %.3f\n"%value[0] + \
                "  center2: %.3f\n"%value[1] + \
                "  threshold: %.3f\n"%value[2] + \
                "  strategy: %d\n"%value[3] + \
                "  retval: %s\n"%value[4]
        self.ui.textbrowser_info.setText(text)

        image = debugGenerateCompareImage(self.cv_verbose_dict, elec_idx, sat_idx)
        self.display_widget.setDisplayCvImage(image)

        

    def clearData(self):
        ''' 删除所有数据
        '''
        self.temp_image_1 = None
        self.cv_image = None
        self.ui.combo_sources.clear()
        self.ui.list_widget.clear()
        self.ui.textbrowser_info.setText("Info:")
        self.display_widget.setDisplayCvImage(None)
