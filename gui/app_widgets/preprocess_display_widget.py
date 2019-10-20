#!/usr/bin/python

'''
 Preprocess Display Widget
'''

from gui.app_widgets.basic_display_widget import BasicDisplayWidget
from gui.text_detection.preprocessing import TdPreprocessing
from gui.app_widgets.preprocess_control_widget import PreprocessDisplayCtrlWidget
import gui.app_widgets.common as apw_comm


class PreprocessDisplayWidget(BasicDisplayWidget):
    '''
    用于显示预处理图像的 Widget 控件
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.control_panel = None
        self.preprocesser = TdPreprocessing()
        self.cur_config = {}
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
        config = self.control_panel.getConfiguration()
        print("TotalPixels:%s，Source:%s"%(config["TotalPixels"], config["Source"]))

        if config['Source'] == 'Color Image (RGB)':
            self.setDisplayCvImage(self.preprocesser.color_img)
        elif config['Source'] == 'Gray':
            self.setDisplayCvImage(self.preprocesser.gray_img)
        elif config['Source'] == 'Blue Channel':
            self.setDisplayCvImage(self.preprocesser.blue_channel)
        elif config['Source'] == 'Red Channel':
            self.setDisplayCvImage(self.preprocesser.red_channel)
        elif config['Source'] == 'Green Channel':
            self.setDisplayCvImage(self.preprocesser.green_channel)
        elif config['Source'] == 'Canny Image':
            self.setDisplayCvImage(self.preprocesser.canny_img)
        elif config['Source'] == 'Sobel X':
            self.setDisplayCvImage(self.preprocesser.sobelX)
        elif config['Source'] == 'Sobel Y':
            self.setDisplayCvImage(self.preprocesser.sobelY)
        elif config['Source'] == 'Magnitudes':
            self.setDisplayCvImage(self.preprocesser.magnitudes)
        elif config['Source'] == 'Grads X':
            self.setDisplayCvImage(self.preprocesser.gradsX)
        elif config['Source'] == 'Grads Y':
            self.setDisplayCvImage(self.preprocesser.gradsY)
        else:
            self.setDisplayCvImage(None)
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
