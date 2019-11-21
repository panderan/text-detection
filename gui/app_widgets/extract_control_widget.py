#!/usr/bin/python


''' 连通域提取控制面板
'''

import logging
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon
import gui.ui.extract_control_ui as extract_ctrl_ui
from gui.text_detection.region_filter import TdFilterCheckType
from gui.text_detection.extract_connect_domain import ExtractDirection
from conf.config import TdConfig, TdExtractConfig, TdFilterConfig

logger = logging.getLogger(__name__)


class ExtractDisplayCtrlWidget(QWidget):
    ''' 连通域提取控制面板
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = extract_ctrl_ui.Ui_ExtractCtrlWidget()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(':/images/icon.png'))
        self.setAttribute(Qt.WA_QuitOnClose, False)

        extract_conf = TdConfig().getExtractConfig()
        self.ui.spinbox_mser_delta.setValue(extract_conf['delta'])
        self.ui.spinbox_mser_area_high.setValue(extract_conf['max_area'])
        self.ui.spinbox_mser_area_low.setValue(extract_conf['min_area'])
        self.ui.dspinbox_mser_variation.setValue(extract_conf['variation'])
        check_flag = True if "Gray" in extract_conf['channels'] else False
        self.ui.checkbox_mser_gray.setChecked(check_flag)
        check_flag = True if "Red Channel" in extract_conf['channels'] else False
        self.ui.checkbox_mser_red.setChecked(check_flag)
        check_flag = True if "Blue Channel" in extract_conf['channels'] else False
        self.ui.checkbox_mser_blue.setChecked(check_flag)
        check_flag = True if "Green Channel" in extract_conf['channels'] else False
        self.ui.checkbox_mser_green.setChecked(check_flag)
        check_flag = True if int(extract_conf['direction']) & ExtractDirection.Positive.value else False
        self.ui.checkbox_mser_direction_positive.setChecked(check_flag)
        check_flag = True if int(extract_conf['direction']) & ExtractDirection.Negitive.value else False
        self.ui.checkbox_mser_direction_negative.setChecked(check_flag)

        filter_conf = TdConfig().getFilterConfig('extract')
        self.ui.spinbox_filter_area_lim.setValue(filter_conf['area_lim'])
        self.ui.spinbox_filter_perimeter_low.setValue(filter_conf['perimeter_lim'][0])
        self.ui.spinbox_filter_perimeter_high.setValue(filter_conf['perimeter_lim'][1])
        self.ui.dspinbox_filter_aspect_ratio_low.setValue(filter_conf['aspect_ratio_lim'][0])
        self.ui.dspinbox_filter_aspect_ratio_high.setValue(filter_conf['aspect_ratio_lim'][1])
        self.ui.checkbox_filter_abs_aspect_ratio.setChecked(filter_conf['aspect_ratio_gt1'])
        self.ui.dspinbox_filter_occupation_low.setValue(filter_conf['occupation_lim'][0])
        self.ui.dspinbox_filter_occupation_high.setValue(filter_conf['occupation_lim'][1])
        self.ui.dspinbox_filter_compactness_low.setValue(filter_conf['compactness_lim'][0])
        self.ui.dspinbox_filter_compactness_high.setValue(filter_conf['compactness_lim'][1])
        self.ui.spinbox_filter_width_low.setValue(filter_conf['width_lim'][0])
        self.ui.spinbox_filter_width_high.setValue(filter_conf['width_lim'][1])
        self.ui.spinbox_filter_height_low.setValue(filter_conf['height_lim'][0])
        self.ui.spinbox_filter_height_high.setValue(filter_conf['height_lim'][1])

        filter_swt_conf = filter_conf['swt']
        self.ui.spinbox_filter_swt_total_points.setValue(filter_swt_conf['total_points'])
        self.ui.dspinbox_filter_swt_mode_lim.setValue(filter_swt_conf['mode_lim'])
        self.ui.dspinbox_filter_swt_mean_low.setValue(filter_swt_conf['mean_lim'][0])
        self.ui.dspinbox_filter_swt_mean_high.setValue(filter_swt_conf['mean_lim'][1])
        self.ui.dspinbox_filter_swt_std_low.setValue(filter_swt_conf['std_lim'][0])
        self.ui.dspinbox_filter_swt_std_high.setValue(filter_swt_conf['std_lim'][1])

        self.setEnabledForFilter(filter_conf['flag'])
        self.initConnects()
        return

    def initConnects(self):
        ''' 初始化信号与槽的连接
        '''
        self.ui.checkbox_filter_area_lim.stateChanged.connect(self.onActionCheckboxFilterAreaLim)
        self.ui.checkbox_filter_perimeter_lim.stateChanged.connect(self.onActionCheckboxFilterPerimeterLim)
        self.ui.checkbox_filter_aspect_ratio_lim.stateChanged.connect(self.onActionCheckboxFilterAspectRatioLim)
        self.ui.checkbox_filter_occupation_lim.stateChanged.connect(self.onActionCheckboxFilterOccupationLim)
        self.ui.checkbox_filter_compactness_lim.stateChanged.connect(self.onActionCheckboxFilterCompactnessLim)
        self.ui.checkbox_filter_width_lim.stateChanged.connect(self.onActionCheckboxFilterWidthLim)
        self.ui.checkbox_filter_height_lim.stateChanged.connect(self.onActionCheckboxFilterHeightLim)
        self.ui.checkbox_filter_swt_filter_enable.stateChanged.connect(self.onActionCheckboxFilterSwtFilterEnable)

    def getConfiguration(self, flag=0):
        ''' 获得配置信息
        '''
        if flag == 0:
            extconf = TdExtractConfig()
            extconf.setConfigItem('delta', self.ui.spinbox_mser_delta.value())
            extconf.setConfigItem('min_area', self.ui.spinbox_mser_area_low.value())
            extconf.setConfigItem('max_area', self.ui.spinbox_mser_area_high.value())
            extconf.setConfigItem('variation', self.ui.dspinbox_mser_variation.value())
            extconf.setConfigItem('debug', self.ui.checkbox_mser_debug_enable.isChecked())
            extconf.setConfigItem('show_verbose', self.ui.checkbox_mser_debug_enable.isChecked()) 
            chnls = []
            if self.ui.checkbox_mser_gray.isChecked():
                chnls.append("Gray")
            if self.ui.checkbox_mser_blue.isChecked():
                chnls.append("Blue Channel")
            if self.ui.checkbox_mser_red.isChecked():
                chnls.append("Red Channel")
            if self.ui.checkbox_mser_green.isChecked():
                chnls.append("Green Channel")
            extconf.setConfigItem('channels', chnls)
            ret = ExtractDirection.Positive.value if self.ui.checkbox_mser_direction_positive.isChecked() else 0
            ret += ExtractDirection.Negitive.value if self.ui.checkbox_mser_direction_negative.isChecked() else 0
            extconf.setConfigItem('direction', ret)
            return extconf.ext_configs
        else:
            fltconf = TdFilterConfig()
            fltconf.setConfigItem('default', 'area_lim', self.ui.spinbox_filter_area_lim.value())
            fltconf.setConfigItem('default', 'perimeter_lim', [self.ui.spinbox_filter_perimeter_low.value(), self.ui.spinbox_filter_perimeter_high.value()])
            fltconf.setConfigItem('default', 'aspect_ratio_lim', [self.ui.dspinbox_filter_aspect_ratio_low.value(), self.ui.dspinbox_filter_aspect_ratio_high.value()])
            fltconf.setConfigItem('default', 'aspect_ratio_gt1', self.ui.checkbox_filter_abs_aspect_ratio.isChecked())
            fltconf.setConfigItem('default', 'occupation_lim', [self.ui.dspinbox_filter_occupation_low.value(), self.ui.dspinbox_filter_occupation_high.value()])
            fltconf.setConfigItem('default', 'compactness_lim', [self.ui.dspinbox_filter_compactness_low.value(), self.ui.dspinbox_filter_compactness_high.value()])
            fltconf.setConfigItem('default', 'width_lim', [self.ui.spinbox_filter_width_low.value(), self.ui.spinbox_filter_width_high.value()])
            fltconf.setConfigItem('default', 'height_lim', [self.ui.spinbox_filter_height_low.value(), self.ui.spinbox_filter_height_high.value()])
            flt_flag = 0
            if self.ui.checkbox_filter_area_lim.isChecked():
                flt_flag += TdFilterCheckType.AREA.value
            if self.ui.checkbox_filter_width_lim.isChecked():
                flt_flag += TdFilterCheckType.WIDTH.value
            if self.ui.checkbox_filter_height_lim.isChecked():
                flt_flag += TdFilterCheckType.HEIGHT.value
            if self.ui.checkbox_filter_perimeter_lim.isChecked():
                flt_flag += TdFilterCheckType.PERIMETER.value
            if self.ui.checkbox_filter_aspect_ratio_lim.isChecked():
                flt_flag += TdFilterCheckType.ASPECTRATIO.value
            if self.ui.checkbox_filter_occupation_lim.isChecked():
                flt_flag += TdFilterCheckType.OCCUPIEDRATIO.value
            if self.ui.checkbox_filter_compactness_lim.isChecked():
                flt_flag += TdFilterCheckType.COMPACTNESS.value
            if self.ui.checkbox_filter_swt_filter_enable.isChecked():
                flt_flag += TdFilterCheckType.SWT.value
            fltconf.setConfigItem('default', 'flag', flt_flag)

            swt_config = {}
            swt_config['total_points'] = self.ui.spinbox_filter_swt_total_points.value()
            swt_config['mode_lim'] = self.ui.dspinbox_filter_swt_mode_lim.value()
            swt_config['mean_lim'] = [self.ui.dspinbox_filter_swt_mean_low.value(), self.ui.dspinbox_filter_swt_mean_high.value()]
            swt_config['std_lim'] = [self.ui.dspinbox_filter_swt_std_low.value(), self.ui.dspinbox_filter_swt_std_high.value()]
            fltconf.setConfigItem('default', 'swt', swt_config)
            return fltconf.flt_configs

    def setEnabledForFilter(self, flag):
        ''' Filter 参数启用/禁用控制
        '''
        self.ui.checkbox_filter_area_lim.setChecked(bool(flag & TdFilterCheckType.AREA.value))
        self.ui.spinbox_filter_area_lim.setEnabled(bool(flag & TdFilterCheckType.AREA.value))
        self.ui.checkbox_filter_perimeter_lim.setChecked(bool(flag & TdFilterCheckType.PERIMETER.value))
        self.ui.spinbox_filter_perimeter_low.setEnabled(bool(flag & TdFilterCheckType.PERIMETER.value))
        self.ui.spinbox_filter_perimeter_high.setEnabled(bool(flag & TdFilterCheckType.PERIMETER.value))
        self.ui.checkbox_filter_aspect_ratio_lim.setChecked(bool(flag & TdFilterCheckType.ASPECTRATIO.value))
        self.ui.dspinbox_filter_aspect_ratio_low.setEnabled(bool(flag & TdFilterCheckType.ASPECTRATIO.value))
        self.ui.dspinbox_filter_aspect_ratio_high.setEnabled(bool(flag & TdFilterCheckType.ASPECTRATIO.value))
        self.ui.checkbox_filter_occupation_lim.setChecked(bool(flag & TdFilterCheckType.OCCUPIEDRATIO.value))
        self.ui.dspinbox_filter_occupation_low.setEnabled(bool(flag & TdFilterCheckType.OCCUPIEDRATIO.value))
        self.ui.dspinbox_filter_occupation_high.setEnabled(bool(flag & TdFilterCheckType.OCCUPIEDRATIO.value))
        self.ui.checkbox_filter_compactness_lim.setChecked(bool(flag & TdFilterCheckType.COMPACTNESS.value))
        self.ui.dspinbox_filter_compactness_low.setEnabled(bool(flag & TdFilterCheckType.COMPACTNESS.value))
        self.ui.dspinbox_filter_compactness_high.setEnabled(bool(flag & TdFilterCheckType.COMPACTNESS.value))
        self.ui.checkbox_filter_width_lim.setChecked(bool(flag & TdFilterCheckType.WIDTH.value))
        self.ui.spinbox_filter_height_low.setEnabled(bool(flag & TdFilterCheckType.WIDTH.value))
        self.ui.spinbox_filter_height_high.setEnabled(bool(flag & TdFilterCheckType.WIDTH.value))
        self.ui.checkbox_filter_height_lim.setChecked(bool(flag & TdFilterCheckType.HEIGHT.value))
        self.ui.spinbox_filter_height_low.setEnabled(bool(flag & TdFilterCheckType.HEIGHT.value))
        self.ui.spinbox_filter_height_high.setEnabled(bool(flag & TdFilterCheckType.HEIGHT.value))
        self.ui.checkbox_filter_swt_filter_enable.setChecked(bool(flag & TdFilterCheckType.SWT.value))
        self.setEnabledForFilterSWT()

    def setEnabledForFilterSWT(self, bflag = None):
        ''' SWT Filter 参数启用/禁用控制
        '''
        bflag = self.ui.checkbox_filter_swt_filter_enable.isChecked() if bflag is None else bflag
        self.ui.checkbox_filter_swt_filter_enable.setChecked(bflag)
        self.ui.spinbox_filter_swt_total_points.setEnabled(bflag)
        self.ui.dspinbox_filter_swt_mode_lim.setEnabled(bflag)
        self.ui.dspinbox_filter_swt_mean_low.setEnabled(bflag)
        self.ui.dspinbox_filter_swt_mean_high.setEnabled(bflag)
        self.ui.dspinbox_filter_swt_std_low.setEnabled(bflag)
        self.ui.dspinbox_filter_swt_std_high.setEnabled(bflag)

    def onActionCheckboxFilterAreaLim(self, state):
        ''' 响应 CheckBox Filter Area
        '''
        self.ui.spinbox_filter_area_lim.setEnabled(bool(state))

    def onActionCheckboxFilterPerimeterLim(self, state):
        ''' 响应 Checkbox Filter Perimeter Lim
        '''
        self.ui.spinbox_filter_perimeter_low.setEnabled(bool(state))
        self.ui.spinbox_filter_perimeter_high.setEnabled(bool(state))

    def onActionCheckboxFilterAspectRatioLim(self, state):
        ''' 响应 Checkbox Filter Aspect Ratio Lim
        '''
        self.ui.dspinbox_filter_aspect_ratio_low.setEnabled(bool(state))
        self.ui.dspinbox_filter_aspect_ratio_high.setEnabled(bool(state))
        self.ui.checkbox_filter_abs_aspect_ratio.setEnabled(bool(state))

    def onActionCheckboxFilterOccupationLim(self, state):
        ''' 响应 Checkbox Filter Occupation Lim
        '''
        self.ui.dspinbox_filter_occupation_low.setEnabled(bool(state))
        self.ui.dspinbox_filter_occupation_high.setEnabled(bool(state))

    def onActionCheckboxFilterCompactnessLim(self, state):
        ''' 响应 Checkbox Filter Compactness Lim
        '''
        self.ui.dspinbox_filter_compactness_low.setEnabled(bool(state))
        self.ui.dspinbox_filter_compactness_high.setEnabled(bool(state))

    def onActionCheckboxFilterWidthLim(self, state):
        ''' 响应 Checkbox Filter Width Lim
        '''
        self.ui.spinbox_filter_width_low.setEnabled(bool(state))
        self.ui.spinbox_filter_width_high.setEnabled(bool(state))

    def onActionCheckboxFilterHeightLim(self, state):
        ''' 响应 Checkbox Filter Height Lim
        '''
        self.ui.spinbox_filter_height_low.setEnabled(bool(state))
        self.ui.spinbox_filter_height_high.setEnabled(bool(state))

    def onActionCheckboxFilterSwtFilterEnable(self, state):
        ''' 响应 Checkbox Filter Swt Filter Enable
        '''
        self.setEnabledForFilterSWT(bool(state))
