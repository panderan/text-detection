'''
公共函数
'''

import numpy
from PyQt5.QtGui import QImage


def img_cv2qt(img_cv):
    '''
    将 OpenCV 格式的图像转换为 QImage
    '''
    img_format = None
    shape_len = len(img_cv.shape)
    if shape_len == 3:
        height, width, chns = img_cv.shape
    elif shape_len == 2:
        height, width = img_cv.shape
        chns = 1
    else:
        return None

    if img_cv.dtype != numpy.dtype(numpy.uint8):
        return None

    if chns == 3:
        img_format = QImage.Format_RGB888
    elif chns == 1:
        img_format = QImage.Format_Grayscale8
    else:
        return None
    return QImage(img_cv.data, width, height, width*chns, img_format)


def img_qt2cv(img_qt):
    '''
    将 QImage 格式的图像转换为 OpenCV 图像
    '''
    width = img_qt.width()
    height = img_qt.height()
    fmt_dict = {
        QImage.Format_RGB888 : 3,
        QImage.Format_Grayscale8 : 1
        }
    channels = fmt_dict.get(img_qt.format(), -1)
    if channels == -1:
        return None

    ptr = img_qt.bits()
    total_bytes = img_qt.byteCount()
    if total_bytes != width*height*channels:
        print("QImage byteCount(%d) is not equal to w*h*c(%d*%d*%d)" \
            %(total_bytes, width, height, channels))
        delta = total_bytes - width*height*channels
        if delta%(height*channels) == 0:
            width += int(delta/(height*channels))
        elif delta%(width*channels) == 0:
            height += int(delta/(width*channels))
        else:
            total_bytes = width*height*channels
    ptr.setsize(total_bytes)
    return numpy.array(ptr).reshape(height, width, channels)
