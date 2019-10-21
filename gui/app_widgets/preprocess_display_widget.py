#!/usr/bin/python

'''
 Preprocess Display Widget
'''

from gui.app_widgets.basic_display_widget import BasicDisplayWidget
from gui.text_detection.preprocessing import TdPreprocessing
from gui.app_widgets.preprocess_control_widget import PreprocessDisplayCtrlWidget
import gui.app_widgets.common as apw_comm
from gui.app_widgets.popup_display_widget import DisplayResultWidget

class PreprocessDisplayWidget(BasicDisplayWidget):
    '''
    用于显示预处理图像的 Widget 控件
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.control_panel = None
        self.preprocesser = TdPreprocessing()
        self.cur_config = {}
        self.dr_widget = None
        return

    def paintEvent(self, e):
        '''
        重载绘制函数
        '''
        super().paintEvent(e)
        return

    def doPreprocess(self):
        '''
        进行预处理
        '''
        # 获取参数,进行预处理
        config = self.control_panel.getConfiguration()
        self.preprocesser.doPreprocessing(config["Source"], config)
        # 显示预处理结果
        preped_image = {"Gray": self.preprocesser.gray_img_preped,
                        "Blue Channel": self.preprocesser.blue_channel_preped,
                        "Red Channel": self.preprocesser.red_channel_preped,
                        "Green Channel": self.preprocesser.green_channel_preped}
        try:
            self.dr_widget = DisplayResultWidget(preped_image[config["Source"]], None)
            self.dr_widget.show()
        except KeyError:
            return
        # 显示原图
        srcs_image = {"Color Image (RGB)": self.preprocesser.color_img,
                      "Gray": self.preprocesser.gray_img,
                      "Blue Channel": self.preprocesser.blue_channel,
                      "Red Channel": self.preprocesser.red_channel,
                      "Green Channel": self.preprocesser.green_channel}
        try:
            self.setDisplayCvImage(srcs_image[config["Source"]])
        except KeyError:
            self.setDisplayCvImage(None)
            return

        self.cur_config = config
        return

    def openControlPanel(self):
        '''
        打开参数控制面板
        '''
        if self.control_panel is None:
            self.control_panel = PreprocessDisplayCtrlWidget()
            self.control_panel.ui.btn_ok.clicked.connect(self.doPreprocess)
        self.control_panel.show()
        return

    def setImage(self, qimage):
        '''
        载入图像
        '''
        self.setDisplayQImage(qimage)
        self.preprocesser.setImage(apw_comm.img_qt2cv(qimage))
        return
