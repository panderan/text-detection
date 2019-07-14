#!/usr/bin/env python

## @package text_detection
#   
# @file preprocessing.py
# 基本预处理
#   
# @author panderan@163.com 
#

import cv2
import numpy as np


class preprocessing:
    
    def __init__(self, bgr_img, total_pixels = 400000):
        self.total_pixels = total_pixels
        zoom_level = sqrt(bgrImg.shape[0] * bgrImg.shape[1] / self.total_pixels)
        bgr_img = cv2.resize(bgr_img, (int(bgr_img.shape[1]/zoom_level), int(bgr_img.shape[0]/zoom_level)))

        self.color_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
        self.gray_img = cv2.cvtColor(self.color_img.copy(), cv2.COLOR_RGB2GRAY)
        self.red_channel = self.color_img[:,:,0]
        self.green_channel = self.color_img[:,:,1]
        self.blue_channel = self.color_img[:,:,2]
        self.canny_img = self.applyCanny(self.gray_img)
        self.sobelX = cv2.Sobel(self.grayImg, cv2.CV_64F, 1, 0, ksize=-1)
        self.sobelY = cv2.Sobel(self.grayImg, cv2.CV_64F, 0, 1, ksize=-1)
        self.stepsX = self.sobelY.astype(int)  ## Steps are inversed!! (x-step -> sobelY)
        self.stepsY = self.sobelX.astype(int)
        self.magnitudes = np.sqrt(self.stepsX * self.stepsX + self.stepsY * self.stepsY)
        self.gradsX = self.stepsX / (self.magnitudes + 1e-10)
        self.gradsY = self.stepsY / (self.magnitudes + 1e-10)

        self.height, self.width = self.color_img.shape[:2]

	def applyCanny(self, img, sigma=0.33):
		v = np.median(img)
		lower = int(max(0, (1.0 - sigma) * v))
		upper = int(min(255, (1.0 + sigma) * v))
		return cv2.Canny(img, lower, upper)
