#!/usr/bin/python

import sys
from PyQt5.QtWidgets import QWidget 
from PyQt5.QtGui import QPainter, QColor, QFont, QImage
from PyQt5.QtCore import Qt, QByteArray, QRect
from PyQt5.QtWidgets import QApplication 
import app_widgets.common as apw_comm 


## 用于显示图像的 Widget 控件
 #
class BasicDisplayWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.display_image = None 
        self.display_width = 0 
        self.display_height = 0
        return

    def paintEvent(self, e):
        painter = QPainter(self)
        if (self.display_image == None):
            painter.setPen(Qt.black)
            painter.setFont(QFont("Arial", 30))
            painter.drawText(e.rect(), Qt.AlignCenter, "Text Detection")
        else:
            window_rect = self.geometry()
            image_rect = QRect(0,0,self.display_width, self.display_height)
            ratio_of_image = image_rect.width() / image_rect.height()
            ratio_of_window = window_rect.width() / window_rect.height()
            if ratio_of_image > ratio_of_window:
                window_rect.setHeight(window_rect.width()/ratio_of_image)
                delta = (self.geometry().height()-window_rect.height())*0.5
                window_rect.setY(delta)
                window_rect.setHeight(window_rect.height()+delta)
            else:
                window_rect.setWidth(window_rect.height()*ratio_of_image)
                delta = (self.geometry().width()-window_rect.width())*0.5
                window_rect.setX(delta)
                window_rect.setWidth(window_rect.width()+delta)
            painter.drawImage(window_rect, self.display_image, image_rect)
        return

    def setDisplayCvImage(self, img_cv):
        self.setDisplayQImage(apw_comm.img_cv2qt(img_cv))
        return

    def setDisplayQImage(self, img_qt):
        self.display_image = img_qt
        self.display_width = img_qt.width()
        self.display_height = img_qt.height()
        self.update()
        return


if __name__ == '__main__':
    img = cv2.imread("/root/Documents/GitReps/text-detection/data/CarPlates/Common/冀FA3215.jpg")
    app = QApplication(sys.argv)
    widget = DisplayWidget()
    # widget.setDisplayImage(img)
    widget.show()
    sys.exit(app.exec_())
