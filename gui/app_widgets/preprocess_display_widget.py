#!/usr/bin/python

''' Preprocess Display Widget
'''

from gui.app_widgets.basic_display_widget import BasicDisplayWidget
from gui.text_detection.preprocessing import TdPreprocessing
from gui.app_widgets.preprocess_control_widget import PreprocessDisplayCtrlWidget
import gui.app_widgets.common as apw_comm
from gui.app_widgets.verbose_show_widget import VerboseDisplayWidget

class PreprocessDisplayWidget(BasicDisplayWidget):
    ''' 用于显示预处理图像的 Widget 控件
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.control_panel = None
        self.preprocesser = TdPreprocessing()
        self.cur_config = {}
        self.dr_widget = None
        return

    def paintEvent(self, e):
        ''' 重载绘制函数
        '''
        super().paintEvent(e)
        return

    def doPreprocess(self):
        ''' 进行预处理
        '''
        # 获取参数,进行预处理
        config = self.control_panel.getConfiguration()
        preped_images_dict = self.preprocesser.doPreprocessing(config["source"], config)
        # 显示预处理结果
        if config['show_verbose'] and preped_images_dict is not None:
            if self.dr_widget is None:
                self.dr_widget = VerboseDisplayWidget()
            self.dr_widget.setPrepVerboseData(preped_images_dict)
            self.dr_widget.show()

        try:
            self.setDisplayCvImage(preped_images_dict['Result'])
        except (KeyError, TypeError):
            self.setDisplayCvImage(None)
            return

        self.cur_config = config
        return

    def openControlPanel(self):
        ''' 打开参数控制面板
        '''
        if self.control_panel is None:
            self.control_panel = PreprocessDisplayCtrlWidget()
            self.control_panel.ui.btn_ok.clicked.connect(self.doPreprocess)
        self.control_panel.show()
        return

    def setImage(self, qimage):
        ''' 载入图像
        '''
        self.setDisplayQImage(qimage)
        self.preprocesser.setImage(apw_comm.img_qt2cv(qimage))
        return
