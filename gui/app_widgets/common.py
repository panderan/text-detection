import cv2, numpy
from PyQt5.QtGui import QImage


## 将 OpenCV 格式的图片转换成 QImage
 #
def img_cv2qt(img_cv):
    format = None
    height, width, chns = img_cv.shape
    if (img_cv.dtype != numpy.dtype(numpy.uint8)):
        return None
    else:
        if (chns == 3):
            format = QImage.Format_RGB888
        elif (chns == 1):
            format = QImage.Format_Grayscale8
        else:
            return None
    return QImage(img_cv.data, width, height, width*chns, format)


## 将 QImage 格式转换为 OpenCV 格式
 #
def img_qt2cv(img_qt):
    width = img_qt.width()
    height = img_qt.height()
    fmt_dict = {
        QImage.Format_RGB888 : 3,
        QImage.Format_Grayscale8 : 1
        }
    channels = fmt_dict.get(img_qt.format(), -1)
    if (channels == -1):
        return None

    ptr = img_qt.bits()
    ptr.setsize(img_qt.byteCount())
    return numpy.array(ptr).reshape(height, width, channels);


