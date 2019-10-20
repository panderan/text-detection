#!/usr/bin/env python

'''
@package text_detection

@file preprocessing.py
基本预处理

@author panderan@163.com

'''
from math import sqrt
import cv2
import numpy as np



class TdPreprocessing:
    '''
    图像预处理
    '''
    def __init__(self, color_img=None, total_pixels=400000):
        self.total_pixels = total_pixels
        self.color_img = color_img
        self.height = 0
        self.width = 0
        self.gray_img = None
        self.red_channel = None
        self.green_channel = None
        self.blue_channel = None
        self.canny_img = None
        self.sobelX = None
        self.sobelY = None
        self.stepsX = None
        self.stepsY = None
        self.magnitudes = None
        self.gradsX = None
        self.gradsY = None
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
        self.canny_img = self._applyCanny(self.gray_img)
        self.sobelX = cv2.Sobel(self.gray_img, cv2.CV_64F, 1, 0, ksize=-1)
        self.sobelY = cv2.Sobel(self.gray_img, cv2.CV_64F, 0, 1, ksize=-1)
        self.stepsX = self.sobelY.astype(int)  ## Steps are inversed!! (x-step -> sobelY)
        self.stepsY = self.sobelX.astype(int)
        self.magnitudes = np.sqrt(self.stepsX * self.stepsX + self.stepsY * self.stepsY)
        self.gradsX = self.stepsX / (self.magnitudes + 1e-10)
        self.gradsY = self.stepsY / (self.magnitudes + 1e-10)
        return

    def _applyCanny(self, img, sigma=0.33):
        '''
        提取 Canny 边缘
        '''
        v = np.median(img)
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        return cv2.Canny(img, lower, upper)
