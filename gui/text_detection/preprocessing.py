#!/usr/bin/env python

'''
@package text_detection

@file preprocessing.py
基本预处理

@author panderan@163.com

'''
import logging
from math import sqrt
import cv2
import numpy as np


logger = logging.getLogger(__name__)


def applyCanny(img, sigma=0.2):
    '''
    提取 Canny 边缘
    '''
    lower = int(np.max(img)*(1-sigma))
    upper = int(np.max(img)*0.5)
    return cv2.Canny(img, lower, upper)


class TdPreprocessing:
    '''
    图像预处理
    '''
    def __init__(self, color_img=None, total_pixels=400000, \
                    gamma=3.0, struct_element_size=5, gauss_blur_size=51, \
                    canny_max=0.9, canny_min=0.7):
        # 参数
        self.total_pixels = total_pixels
        self.gamma = gamma
        self.struct_element_size = struct_element_size
        self.gauss_blur_size = gauss_blur_size
        self.canny_max = canny_max
        self.canny_min = canny_min
        self.height = 0
        self.width = 0
        # 数据
        self.color_img = color_img
        self.gray_img = None
        self.gray_img_preped = None
        self.red_channel = None
        self.red_channel_preped = None
        self.green_channel = None
        self.green_channel_preped = None
        self.blue_channel = None
        self.blue_channel_preped = None
        return

    def setTotalPixels(self, total_pixels):
        '''
        设置总像素量参数
        '''
        self.total_pixels = total_pixels
        return

    def setImage(self, color_img):
        '''
        输入图像
        '''
        if color_img is None:
            return
        self.color_img = color_img

        # 缩放图像并获得宽高
        zoom_level = sqrt(self.color_img.shape[0] * self.color_img.shape[1] / self.total_pixels)
        self.color_img = cv2.resize(self.color_img, (int(self.color_img.shape[1]/zoom_level), int(self.color_img.shape[0]/zoom_level)))
        self.height, self.width = color_img[:2]

        # 由原图解析出的各种图像
        self.gray_img = cv2.cvtColor(self.color_img.copy(), cv2.COLOR_RGB2GRAY)
        self.red_channel = self.color_img[:, :, 0].copy()
        self.green_channel = self.color_img[:, :, 1].copy()
        self.blue_channel = self.color_img[:, :, 2].copy()
        return

    def doPreprocessing(self, img_type_name="Gray", config=None):
        ''' 图像预处理
        '''
        self.setConfig(config)
        self.printParams("Do preprocessing")
        input_image = None
        input_srcs = {"Red Channel": self.red_channel,
                      "Blue Channel": self.blue_channel,
                      "Green Channel": self.green_channel,
                      "Gray": self.gray_img}
        try:
            input_image = input_srcs[img_type_name]
        except KeyError:
            return None

        # 顶帽运算
        struct_element = cv2.getStructuringElement(cv2.MORPH_RECT, \
                                    (self.struct_element_size, self.struct_element_size))
        tophat = cv2.morphologyEx(input_image, cv2.MORPH_TOPHAT, struct_element)
        backhat = cv2.morphologyEx(input_image, cv2.MORPH_BLACKHAT, struct_element)
        hat = tophat*(tophat >= backhat) + backhat*(backhat > tophat)
        # 提取 Canny 边缘
        cy = cv2.Canny(hat, \
                        np.max(hat)*self.canny_max, \
                        np.max(hat)*self.canny_min)
        # 消除水平边缘
        sobely = cv2.Sobel(cy, -1, 1, 0)
        # 高斯模糊
        blur = cv2.GaussianBlur(sobely, (self.gauss_blur_size, self.gauss_blur_size), 0)
        # 归一化
        blurf = blur/blur.max()
        # 与原图相乘并直方图均衡化
        out_image = np.uint8(input_image * blurf)
        equ = cv2.equalizeHist(out_image)
        # Gamma 变换
        tp = equ/255.0
        o = np.power(tp, self.gamma)
        out_image = np.uint8(o*255.0)

        if img_type_name == "Gray":
            self.gray_img_preped = out_image
        elif img_type_name == "Red Channel":
            self.red_channel_preped = out_image
        elif img_type_name == "Blue Channel":
            self.blue_channel_preped = out_image
        elif img_type_name == "Green Channel":
            self.green_channel_preped = out_image
        else:
            return None

        ret_dict = {"Result": out_image,
                    "Gray": input_image,
                    "Hat": hat,
                    "Canny": cy,
                    "SobelY": sobely,
                    "GaussBlur": blur}
        return ret_dict

    def __setConfigItem(self, keystr, config):
        try:
            if keystr == "gamma":
                self.gamma = config[keystr]
            elif keystr == "struct_element_size":
                self.struct_element_size = config[keystr]
            elif keystr == "gauss_blur_size":
                self.gauss_blur_size = config[keystr]
            elif keystr == "total_pixels":
                old_total_pixels = self.total_pixels
                self.total_pixels = config[keystr]
                if old_total_pixels != self.total_pixels:
                    self.setImage(self.color_img)
            elif keystr == "canny":
                self.canny_max = config[keystr][0]
                self.canny_min = config[keystr][1]
            else:
                pass
        except KeyError:
            pass
        return

    def setConfig(self, config):
        ''' 设置配置文件
        '''
        if config is None:
            return
        self.__setConfigItem("gamma", config)
        self.__setConfigItem("struct_element_size", config)
        self.__setConfigItem("gauss_blur_size", config)
        self.__setConfigItem("total_pixels", config)
        self.__setConfigItem("canny", config)
        return


    def printParams(self, msg):
        '''
        打印当前参数
        '''
        params = {"total_pixels": self.total_pixels,
                  "gamma": self.gamma,
                  "canny": [self.canny_max, self.canny_min],
                  "gauss_blur_size": self.gauss_blur_size,
                  "struct_element_size": self.struct_element_size}
        msg = "%s,%s" %(msg, params)
        logger.info(msg)

    @property
    def gray_img_preped(self):
        '''
        获取 Gray 预处理后图像，获取时计算
        '''
        if self.__gray_img_preped is None:
            self.doPreprocessing("Gray")
        return self.__gray_img_preped
    @gray_img_preped.setter
    def gray_img_preped(self, val):
        self.__gray_img_preped = val

    @property
    def red_channel_preped(self):
        '''
        获取 Red Channel 预处理后图像，获取时计算
        '''
        if self.__red_channel_preped is None:
            self.doPreprocessing("Red Channel")
        return self.__red_channel_preped
    @red_channel_preped.setter
    def red_channel_preped(self, val):
        self.__red_channel_preped = val

    @property
    def green_channel_preped(self):
        '''
        获取 Green Channel 预处理后图像，获取时计算
        '''
        if self.__green_channel_preped is None:
            self.doPreprocessing("Green Channel")
        return self.__green_channel_preped
    @green_channel_preped.setter
    def green_channel_preped(self, val):
        self.__green_channel_preped = val

    @property
    def blue_channel_preped(self):
        '''
        获取 Blue Channel 预处理后图像，获取时计算
        '''
        if self.__blue_channel_preped is None:
            self.doPreprocessing("Blue Channel")
        return self.__blue_channel_preped
    @blue_channel_preped.setter
    def blue_channel_preped(self, val):
        self.__blue_channel_preped = val
