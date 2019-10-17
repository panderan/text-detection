#!/usr/bin/python

from app_widgets.basic_display_widget import BasicDisplayWidget
from text_detection.preprocessing import TdPreprocessing
from app_widgets.preprocess_control_widget import PreprocessDisplayCtrlWidget
import app_widgets.common as apw_comm 


## 用于显示图像的 Widget 控件
 #
class PreprocessDisplayWidget(BasicDisplayWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.control_panel = None
        self.preprocesser = TdPreprocessing()
        return

    def paintEvent(self, e):
        super().paintEvent(e)
        return
    
    def doPreprocess(self):
        config = self.control_panel.getConfiguration()
        print("TotalPixels:%s，Source:%s"%(config["TotalPixels"], config["Source"]))
        return 

    def openControlPanel(self):
        if (self.control_panel == None):
            self.control_panel = PreprocessDisplayCtrlWidget()
            self.control_panel.ui.btn_ok.clicked.connect(self.doPreprocess)
        self.control_panel.show()
        return

    def setImage(self, qimage):
        self.setDisplayQImage(qimage)
        self.preprocesser.setImage(apw_comm.img_qt2cv(qimage))
        return

